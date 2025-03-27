import asyncio
import logging
from .protocol import BestjoyProtocol

_LOGGER = logging.getLogger(__name__)

class BestjoyClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._reader = None
        self._writer = None
        self._lock = asyncio.Lock()
        self._heartbeat_task = None       # 心跳任务句柄
        self._reconnect_attempts = 0       # 重连尝试次数
        self._max_reconnect_retries = 5    # 最大重试次数
        self._base_reconnect_delay = 1.0   # 基础重连延迟（秒）
        self._max_reconnect_delay = 60.0   # 最大重连延迟（秒）

    async def async_test_connection(self) -> bool:
        """测试设备连接"""
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
        """建立正式连接并启动心跳"""
        async with self._lock:
            if not self._writer or self._writer.is_closing():
                self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
                # 启动心跳任务
                self._heartbeat_task = asyncio.create_task(self._start_heartbeat())

    async def _start_heartbeat(self):
        """心跳包发送任务"""
        _LOGGER.debug("Heartbeat task started")
        try:
            while self._writer and not self._writer.is_closing():
                try:
                    # 发送空包（示例使用 0x00 作为心跳包）
                    self._writer.write(b'\x00')
                    await self._writer.drain()
                    _LOGGER.debug("Heartbeat sent")
                except Exception as e:
                    _LOGGER.error(f"Heartbeat send failed: {str(e)}")
                    await self.async_reconnect()
                    break  # 重连后由新连接启动心跳

                # 60秒间隔（可配置）
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            _LOGGER.debug("Heartbeat task cancelled")
        finally:
            self._heartbeat_task = None

    async def async_send_command(self, call):
        """处理服务调用"""
        command_data = call.data.get("data") if isinstance(call.data, dict) else call.data

        if not isinstance(command_data, str) or len(command_data) % 2 != 0:
            _LOGGER.error(f"无效指令格式: {command_data}")
            return
        
        packet = BestjoyProtocol.build_packet(command_data)
        async with self._lock:
            try:
                self._writer.write(packet)
                await asyncio.wait_for(self._writer.drain(), timeout=5)
                _LOGGER.debug(f"Sent: {packet.hex()}")
            except Exception as e:
                _LOGGER.error(f"Send failed: {str(e)}")
                await self.async_reconnect()

    async def async_reconnect(self):
        """带指数退避的智能重连"""
        await self._async_close()
        
        while self._reconnect_attempts < self._max_reconnect_retries:
            try:
                _LOGGER.warning(f"Reconnecting attempt {self._reconnect_attempts + 1}/{self._max_reconnect_retries}")
                await self.async_connect()
                self._reconnect_attempts = 0  # 重置计数器
                return
            except Exception as e:
                self._reconnect_attempts += 1
                delay = min(
                    self._base_reconnect_delay * (2 ** (self._reconnect_attempts - 1)),
                    self._max_reconnect_delay
                )
                _LOGGER.error(f"Reconnect failed: {str(e)}, retrying in {delay}s")
                await asyncio.sleep(delay)
        
        _LOGGER.error("Max reconnect attempts reached")
        raise ConnectionError("Connection lost after multiple retries")

    async def _async_close(self):
        """安全关闭连接"""
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception as e:
                _LOGGER.debug(f"Connection closure error: {str(e)}")
            finally:
                self._writer = None
                self._reader = None