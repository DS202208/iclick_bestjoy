class BestjoyProtocol:
    @staticmethod
    def generate_crc(data: bytes) -> int:
        return sum(data) & 0xFF

    @classmethod
    def build_packet(cls, data: str):
        """修复header未定义问题"""
        # 输入验证
        if not isinstance(data, str):
            raise TypeError("指令必须为字符串类型")
        
        # 清理输入
        data = data.strip().upper().replace(" ", "")
        
        # 验证十六进制格式
        if not data:
            raise ValueError("指令不能为空")
        if len(data) % 2 != 0:
            raise ValueError("指令长度必须为偶数")
        if not all(c in "0123456789ABCDEF" for c in data):
            raise ValueError("包含非法十六进制字符")

        # 协议头必须在数据转换前定义
        header = bytes([0x55, 0xFF, 0x80])  # 正确位置
        data_bytes = bytes.fromhex(data)
        length = len(data_bytes).to_bytes(2, byteorder='big')
        
        # 构建协议包
        payload = header + length + data_bytes
        crc = cls.generate_crc(payload)
        return payload + bytes([crc])