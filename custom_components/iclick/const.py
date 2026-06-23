"""const.py of an iClick Gateway."""
DOMAIN = "iclick"
DEFAULT_PORT = 9999
TIMEOUT = 10

CONF_HOST = "host"
CONF_PORT = "port"
CONF_ACCOUNT = "account"      # 新增账号配置
CONF_PASSWORD = "password"    # 新增密码配置
CONF_MAC = "mac"              # 新增MAC配置
CONF_AREA = "area"            # 新增区域配置

DATA_IP_INFO = "ip_info"            # 网关IP信息
DATA_DEVICE_DATA = "device_data"            # 设备信息
DATA_DEVICE_DATA_MAP = "device_map"            # 设备信息
DATA_IP_DEVICE_CLIENT = "ip_client"            # IP设备Client
DATA_DEVICE_INFO_NAME = "device_name"          # 设备名称

ERROR_INVALID_IP = "invalid_ip"
ERROR_CONNECTION_FAILED = "connection_failed"
ERROR_AUTH_FAILED = "auth_failed"  # 新增认证错误
ERROR_DEVICE_DATA = "device_data_error"  # 新增设备数据错误

HEARTBEAT_INTERVAL = 60
MAX_RECONNECT_RETRIES = 5
BASE_RECONNECT_DELAY = 1.0
MAX_RECONNECT_DELAY = 60.0

API_URL = "https://www.dzbxk.com/yzk/mcp_gateway.ashx"  # 新增API URL