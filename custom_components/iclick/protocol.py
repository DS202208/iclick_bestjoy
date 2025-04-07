class BestjoyProtocol:
    @staticmethod
    def generate_crc(data: bytes) -> int:
        return sum(data) & 0xFF

    @classmethod
    def build_packet(cls, data: str):
        """修复header未定义问题"""
        # 输入验证
        if not isinstance(data, str):
            raise TypeError("The data must be a hexadecimal string")
        
        # 清理输入
        data = data.strip().upper().replace(" ", "")
        
        # 验证十六进制格式
        if not data:
            raise ValueError("Data cannot be none")
        if len(data) % 2 != 0:
            raise ValueError("Data length must be even")
        if not all(c in "0123456789ABCDEF" for c in data):
            raise ValueError("Contains illegal hexadecimal characters")

        # 协议头必须在数据转换前定义
        header = bytes([0x55, 0xFF, 0x80])  # 正确位置
        data_bytes = bytes.fromhex(data)
        length = len(data_bytes).to_bytes(2, byteorder='big')
        
        # 构建协议包
        payload = header + length + data_bytes
        crc = cls.generate_crc(payload)
        return payload + bytes([crc])