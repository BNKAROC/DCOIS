import cm824_basic
import time
import flash_load
import cm421_i2c
# cm824_basic.cml_cm8x4_erase_user_eeprom()
flag = 0x01
map_version = 0x02
calbration_parameter = [-1.4455E-01,1.2678E-01,-1.0090E-03,9.2523E-06]
data_load = flash_load.generate_dataload(flag, map_version, calbration_parameter)
# # print("数据加载:",len(data_load))
# # print("16进制格式输出:", [f'0x{byte:02X}' for byte in data_load])
if len(data_load) %4!= 0:
    print(f"数据长度 cha{len(data_load)%4} ，正在填充0xFF...")

    for i in range(0, 4-len(data_load)%4):
        data_load.append(0xff)
        print(f"填充数据: 0xFF, 当前数据长度: {len(data_load)}")
    print(f"填充数据: 0xFF, 当前数据长度: {len(data_load)}")
    print("数据长度正确，可以进行写入。")
# 写入数据到 EEPROM
print(f"写入数据长度: {len(data_load)}")
# cm824_basic.cml_cm8x4_set_user_eeprom(0x0000, len(data_load), data_load, {})
# cm824_basic.cml_cm8x4_erase_user_eeprom()
print(data_load)
# 读取数据以验证写入
time.sleep(1)
DATA=cm421_i2c.I2C_A16V8_read_bytes(cm824_basic.EEPROM_DEVICE_ID, 0x0000, 28)
print(f"EEPROM 数据: {DATA}")