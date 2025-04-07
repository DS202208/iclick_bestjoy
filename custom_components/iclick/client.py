import asyncio
import logging
import random
from .protocol import BestjoyProtocol

_LOGGER = logging.getLogger(__name__)

class BestjoyClient:
    def __init__(self, host: str, port: int, hub_id: int): 
        self.host = host
        self.port = port
        self.hub_id = hub_id
        # 连接相关资源
        self._reader = None
        self._writer = None
        self._transport = None
        self._connection_ready = False  # 新增连接状态标志
        # 异步控制
        self._lock = asyncio.Lock()
        self._heartbeat_task = None
        # 重连策略
        self._reconnect_attempts = 0
        self._max_retries = 5          # 最大自动重试次数
        self._base_reconnect_delay = 1.0
        self._max_reconnect_delay = 60.0

    async def async_test_connection(self) -> bool:
        """测试连接（深度重置版）"""
        await self._hard_reset()  # 先执行硬重置
        try:
            async with self._lock:
                self._reader, self._writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port),
                    timeout=5
                )
                return True
        except Exception as e:
            _LOGGER.error(f"Connection test failed: {str(e)}")
            return False
        finally:
            await self._async_close()

    async def async_connect(self):
        """增强版连接方法"""
        async with self._lock:
            if self._connection_ready: 
                return
                
            try:
                # 等待网关初始化完成
                await asyncio.sleep(5)
                # 建立新连接
                self._reader, self._writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port),
                    timeout=10
                )
                # 启动心跳任务
                self._heartbeat_task = asyncio.create_task(
                    self._start_heartbeat(), 
                    name=f"iclick_heartbeat_{self.host}"  # 增加主机标识
                )
                self._connection_ready = True
                _LOGGER.info("Connection established")
            except Exception as e:
                _LOGGER.error(f"Connection failed: {str(e)}")
                await self._trigger_recovery()

    async def _start_heartbeat(self):
        """智能心跳任务"""
        try:
            while self._connection_ready:
                try:
                    self._writer.write(b'\x00')
                    await self._writer.drain()
                    await asyncio.sleep(60)
                except Exception as e:
                    _LOGGER.error(f"Heartbeat error: {str(e)}")
                    await self._trigger_recovery()
                    break
        except asyncio.CancelledError:
            _LOGGER.debug("Heartbeat cancelled")

    async def async_send_command(self, data: str):  # 改为直接接收data字符串
        """发送指令（自动处理协议封装）"""
        for attempt in range(3):
            if not self._connection_ready:
                _LOGGER.warning(f"Hub {self.hub_id} 连接未就绪（尝试 {attempt+1}/3）")
                await self.async_reconnect()
                continue
            try:
                packet = BestjoyProtocol.build_packet(data)
                async with self._lock:
                    self._writer.write(packet)
                    await asyncio.wait_for(self._writer.drain(), timeout=5)
                    return
            except Exception as e:
                _LOGGER.error(f"Hub {self.hub_id} 发送失败：{str(e)}")
                await self._trigger_recovery()
        _LOGGER.error(f"Hub {self.hub_id} 所有发送尝试均失败")
        await self._hard_reset()

    async def async_reconnect(self):
        """增强版重连逻辑"""
        self._connection_ready = False
        await self._async_close()
        
        while self._reconnect_attempts < self._max_retries:
            delay = self._calc_retry_delay()
            _LOGGER.warning(f"Reconnect attempt {self._reconnect_attempts+1}/{self._max_retries}")
            
            try:
                await asyncio.sleep(delay)
                await self.async_connect()
                if self._connection_ready:
                    self._reconnect_attempts = 0
                    return
            except Exception as e:
                self._reconnect_attempts += 1
                _LOGGER.error(f"Reconnect error: {str(e)}")
                
        await self._hard_reset()  # 达到最大重试次数触发硬重置

    def _calc_retry_delay(self) -> float:
        """计算退避时间（含随机抖动）"""
        base_delay = min(
            self._base_reconnect_delay * (2 ** self._reconnect_attempts),
            self._max_reconnect_delay
        )
        return base_delay + random.uniform(0, 2)

    async def _trigger_recovery(self):
        """启动恢复流程"""
        self._connection_ready = False
        if self._reconnect_attempts >= self._max_retries:
            await self._hard_reset()
        else:
            await self.async_reconnect()

    async def _hard_reset(self):
        """深度重置（模拟重启效果）"""
        _LOGGER.warning("Performing hard reset")
        await self._async_close()
        # 清理所有残留任务
        for task in asyncio.all_tasks():
            if task.get_name().startswith("iclick"):
                task.cancel()
        # 重置所有状态
        self._reconnect_attempts = 0
        self._connection_ready = False
        await asyncio.sleep(1)  # 等待资源释放
        await self.async_connect()

    async def _async_close(self):
        """原子化关闭操作"""
        # 关闭心跳任务
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            finally:
                self._heartbeat_task = None
                
        # 关闭网络连接
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception as e:
                _LOGGER.debug(f"Close error: {str(e)}")
            finally:
                self._writer = None
                self._reader = None
                
        if self._transport:
            self._transport.close()
            try:
                await self._transport.wait_closed()
            except Exception:
                pass
            finally:
                self._transport = None