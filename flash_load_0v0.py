import struct
import datetime
# 移除错误的导入语句，添加正确的 openpyxl 导入
# try:
#     from openpyxl import Workbook
#     import openpyxl
#     print("openpyxl 库导入成功。")
# except ImportError:
#     print("未找到 openpyxl 库，请运行 'pip install openpyxl' 安装。")
#     raise

def float_to_ieee754_hex(value: float) -> str:
    """
    将一个十进制浮点数转换为 IEEE754 单精度（32-bit）十六进制表示。
    """
    packed = struct.pack('>f', value)         # 打包为 4 字节大端 float
    hex_str = ''.join(f'{byte:02X}' for byte in packed)  # 每字节转16进制
    return hex_str
def calbration_parameter_float_to_hex(calbration_parameter):
    hex_values = []
    for val in calbration_parameter:
        hex_str = float_to_ieee754_hex(val)
        bytes_int = [int('0x' + hex_str[i:i+2], 16) for i in range(0, 8, 2)]
        hex_values.extend(bytes_int)
    return hex_values
def get_current_date_hex_list():
    today = datetime.date.today()
    year = int(str(today.year), 16)
    month = int(str(today.month), 16)
    day = int(str(today.day), 16)
    hex_list = [year >> 8, year & 0xFF, month, day]
    return [int(f'0x{val:02X}', 16) for val in hex_list]
def check_sum(data):
    # data 共38字节，去掉前2字节，后面每4字节组成一个数
    nums = []
    for i in range(2, 38, 4):
        num = (data[i] << 24) | (data[i+1] << 16) | (data[i+2] << 8) | data[i+3]
        nums.append(num)
    total = sum(nums) & 0xFFFFFFFF
    return [
        (total >> 24) & 0xFF,
        (total >> 16) & 0xFF,
        (total >> 8) & 0xFF,
        total & 0xFF
    ]


def generate_dataload(flag, map_version, calbration_parameter):
    data_load = []
    calbration_data=calbration_parameter_float_to_hex(calbration_parameter)
    # print(f'校准参数十六进制: {calbration_data}')
    data_load.append(flag)
    data_load.append(map_version)
    data_load.extend(calbration_data)
    # get_current_date_hex_list()
    data_load.extend(get_current_date_hex_list())
    data_load.extend(check_sum(data_load))
    # print([f'0x{byte:02X}' for byte in data_load])
    return data_load
# calbration_parameter = [-1.4455E-01,1.2678E-01,-1.0090E-03,9.2523E-06]
# flag = 0x01
# map_version = 0x02
# data_load = generate_dataload(flag, map_version, calbration_parameter)
# print("数据加载:", data_load)
# print("16进制格式输出:", [f'0x{byte:02X}' for byte in data_load])
