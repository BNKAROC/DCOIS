import struct
import datetime
import flash_load
import AW86008
import time
from smbus3 import SMBus, i2c_msg
import FIT

# 移除错误的导入语句，添加正确的 openpyxl 导入
# try:
#     from openpyxl import Workbook
#     import openpyxl
#     print("openpyxl 库导入成功。")
# except ImportError:
#     print("未找到 openpyxl 库，请运行 'pip install openpyxl' 安装。")
#     raise


# AW86008.flash_erase(0x0000,3)
# time.sleep(0.1)
# flag = 0x01
# map_version = 0x02
# # 设置日期和标志的十六进制值
# calbration_parameter = [1.5895,0.0088,0.0002,4e-07,1.5942,0.0114,0.0002,5e-07]
# data_load = flash_load.generate_dataload(flag, map_version, calbration_parameter)
# # AW86008.flash_write(0x0000, data_load)
# print("数据加载:", data_load)

# print("16进制格式输出:", [f'0x{byte:02X}' for byte in data_load])
# # ...existing code...
# hex_str = ",".join([f"0x{byte:02X}" for byte in data_load])
# with open("data_load_hex.txt", "w") as f:
#     f.write(hex_str)
# print("16进制格式已写入 data_load_hex.txt")
# # ...existing code...
# # 读取数据进行验证
# time.sleep(0.1)
file_path = r"/home/OISAE/Desktop/BNKA/dcois/ASKP/ASKP-64.txt"
coefficients = FIT.fit_coefficients(file_path)
# print("拟合系数:", coefficients)
dataload=flash_load.generate_dataload(0x01, 0x02, coefficients)
print("数据加载:", dataload)
print("16进制格式输出:", ",".join([f"0x{byte:02X}" for byte in dataload]))
time.sleep(0.1)
# AW86008.flash_write(0x0000, dataload)
# time.sleep(1)
# read_back_data = AW86008.flash_read(0x0000, len(dataload))
# print("读取回的数据:", read_back_data)