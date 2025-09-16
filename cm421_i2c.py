# v1.1 增加寄存器设置和CM421函数
import time
from smbus3 import SMBus, i2c_msg
cm421_addr = 0x30
flash_addr = 0x54
#CM421寄存器
CM421_REG_DEVICE_RESET=0x0018
CM421_REG_CHIP_ENABLE=0x0020

CM421_REG_ACC_OUT_X=0x9B8E
CM421_REG_ACC_OUT_Y=0x9B92
CM421_REG_ACC_RAW_X=0x9B8C
CM421_REG_ACC_RAW_Y=0x9B90
CM421_REG_ACTIVE=0x9B2A
CM421_REG_CONTROL_MODE=0x9B2C
CM421_REG_DATA_READ_START=0x9DFE
CM421_REG_FEATURE_MODE=0x99BC
CM421_REG_FSYNC_ENABLE=0x9812
CM421_REG_FSYNC_LOOP_DELAY=0x9812
CM421_REG_FSYNC_OFFSET_X0=0x97FC
CM421_REG_FSYNC_OFFSET_X1=0x97FE
CM421_REG_FSYNC_OFFSET_X2=0x9800
CM421_REG_FSYNC_OFFSET_X3=0x9802
CM421_REG_FSYNC_OFFSET_Y0=0x9804
CM421_REG_FSYNC_OFFSET_Y1=0x9806
CM421_REG_FSYNC_OFFSET_Y2=0x9808
CM421_REG_FSYNC_OFFSET_Y3=0x980A
CM421_REG_FSYNC_START_OFFSET=0x980C
CM421_REG_FSYNC_END_OFFSET=0x980E
CM421_REG_FSTNC_TRIGGERS_REQUIRED=0x9810
CM421_REG_BUILD_CONFIG_ID=0x9B06
CM421_REG_FW_BUILD_DATE=0x9B18 #4bytes
CM421_REG_FW_BUILD_TIME=0x9B1C #4bytes
CM421_REG_FW_UID_H=0x9B04
CM421_REG_FW_UID_L=0x9B02
CM421_REG_FW_VERSION_MAJOR=0x9B08
CM421_REG_FW_VERSION_MINOR=0x9B0A
CM421_REG_FW_VERSION_PATCH=0x9B0C
CM421_REG_GYRO_FILTER_OUT_RZ=0x9b82
CM421_REG_GYRO_FILTER_OUT_X=0x9B86
CM421_REG_GYRO_FILTER_OUT_Y=0x9B8A
CM421_REG_GYRO_FILTER_UPDATE=0x9B30
CM421_REG_GYRO_FILTER_SCALING=0x9B30
CM421_REG_GYRO_GAIN_POL_RZ=0x9EFC

CM421_REG_GYRO_GAIN_RZ=0x9EE2
CM421_REG_GYRO_GAIN_X=0x9EE4
CM421_REG_GYRO_GAIN_Y=0X9EE6
CM421_REG_GYRO_LIB_VER=0x9E00
CM421_REG_GYRO_OFFS_CAL_STATUS=0x9EE0
CM421_REG_GYRO_OFFSET_RZ=0x9EE8
CM421_REG_GYRO_OFFSET_X=0x9EEA
CM421_REG_GYRO_OFFSET_Y=0x9EEC
CM421_REG_GYRO_ORIENTATION_SEL=0x9EFA
CM421_REG_GYRO_RAW_RZ=0x9B80
CM421_REG_GYRO_RAW_X=0x9B84
CM421_REG_GYRO_RAW_Y=0x9B88
CM421_REG_IMU_SENSOE_SEL=0x9E18
CM421_REG_MCUACTIVE=0x0024
CM421_REG_OPEN_SHORT_DETECTION=0x9988
CM421_REG_POSITION_ESTIMATE_RZ=0x99CC
CM421_REG_POSITION_ESTIMATE_X=0x99CE
CM421_REG_POSITION_ESTIMATE_Y=0x99D0
CM421_REG_POSITION_RZ=0x99C4
CM421_REG_POSITION_X=0x99C6
CM421_REG_POSITION_Y=0x99C8
CM421_REG_RESISTANCE0=0x97F4
CM421_REG_RESISTANCE1=0x97F6
CM421_REG_RESISTANCE2=0x97F8
CM421_REG_RESISTANCE3=0x97FA
CM421_REG_RZ_LOWER_COEFFICIENT0=0x9F50 #4bytes
CM421_REG_RZ_LOWER_COEFFICIENT1=0x9F4C #4bytes
CM421_REG_RZ_MID_COEFFICIENT0=0x9F50 #4bytes
CM421_REG_RZ_MID_COEFFICIENT1=0x9F54 #4bytes
CM421_REG_RZ_UPPER_COEFFICIENT0=0x9F58 #4bytes
CM421_REG_RZ_UPPER_COEFFICIENT1=0x9F5C #4bytes
CM421_REG_TEMPERATURE_MODEL_OFFSET=0x97CC
CM421_REG_THERMISTOR=0x99D4
CM421_REG_TOPCODE_STATUS=0X9B28
CM421_REG_TRIGGER_ON_RISING=0x9B40
CM421_REG_VSYNC_TRIGGER_COUNT=0x9B42
CM421_REG_VSYNC_TRIGGER_MODE=0x9B40
CM421_REG_X_LOWER_COEFFICIENT0=0x9F18 #4bytes
CM421_REG_X_LOWER_COEFFICIENT1=0x9F1C #4bytes
CM421_REG_X_MID_COEFFICIENT0=0x9F20 #4bytes
CM421_REG_X_MID_COEFFICIENT1=0x9F24 #4bytes
CM421_REG_X_UPPER_COEFFICIENT0=0x9F28 #4bytes
CM421_REG_X_UPPER_COEFFICIENT1=0x9F2C #4bytes
CM421_REG_Y_LOWER_COEFFICIENT0=0x9F30 #4bytes
CM421_REG_Y_LOWER_COEFFICIENT1=0x9F34 #4bytes
CM421_REG_Y_MID_COEFFICIENT0=0x9F38 #4bytes
CM421_REG_Y_MID_COEFFICIENT1=0x9F3C #4bytes
CM421_REG_Y_UPPER_COEFFICIENT0=0x9F40 #4bytes
CM421_REG_Y_UPPER_COEFFICIENT1=0x9F44 #4bytes


# 创建并保存 I2C 总线对象
try:
    bus = SMBus(0)  # 打开 I2C 总线
except IOError as e:
    print(f"打开 I2C 总线失败: {e}")
    exit(1)  # 如果打开总线失败，退出程序

cm421_addr = 0x30
flash_addr = 0x54

def cm421_write_2byte(reg, write_data):
    try:
        Reg_MSB = (reg >> 8) & 0xFF
        Reg_LSB = reg & 0xFF
        write_data_MSB = (write_data >> 8) & 0xFF
        write_data_LSB = write_data & 0xFF
        msg = i2c_msg.write(cm421_addr, [Reg_MSB, Reg_LSB, write_data_MSB, write_data_LSB])
        bus.i2c_rdwr(msg)
    except IOError as e:
        print(f"写入数据失败: {e}")

def cm421_read_2byte(reg):
    try:
        Reg_MSB = (reg >> 8) & 0xFF
        Reg_LSB = reg & 0xFF
        write_msg = i2c_msg.write(cm421_addr, [Reg_MSB, Reg_LSB])
        read_msg = i2c_msg.read(cm421_addr, 2)
        bus.i2c_rdwr(write_msg, read_msg)
        data = list(read_msg)
        reg_value = '0x{:02x}{:02x}'.format(data[0], data[1])
        return reg_value
    except IOError as e:
        print(f"读取数据失败: {e}")
        return None

def cm421_Sequential_write(reg, data_list):
    try:
        i2c_data_transfer = []
        Reg_MSB = (reg >> 8) & 0xFF
        i2c_data_transfer.append(Reg_MSB)
        Reg_LSB = reg & 0xFF
        i2c_data_transfer.append(Reg_LSB)
        for i in data_list:
            data_MSB = (i >> 8) & 0xFF
            i2c_data_transfer.append(data_MSB)
            data_LSB = i & 0xFF
            i2c_data_transfer.append(data_LSB)
        msg = i2c_msg.write(cm421_addr, i2c_data_transfer)
        bus.i2c_rdwr(msg)
    except IOError as e:
        print(f"顺序写入数据失败: {e}")

def cm421_Sequential_read(reg, number):
    try:
        data_out = []
        Reg_MSB = (reg >> 8) & 0xFF
        Reg_LSB = reg & 0xFF
        write_msg = i2c_msg.write(cm421_addr, [Reg_MSB, Reg_LSB])
        read_msg = i2c_msg.read(cm421_addr, 2 * number)
        bus.i2c_rdwr(write_msg, read_msg)
        data_read = list(read_msg)
        length = len(data_read)
        for i in range(int(length * 0.5)):
            reg_value = '0x{:02x}{:02x}'.format(data_read[2 * i], data_read[2 * i + 1])
            data_out.append(reg_value)
        return data_out
    except IOError as e:
        print(f"顺序读取数据失败: {e}")
        return []

def I2C_A16V8_write_byte(address, reg, data):
    """
    向16位寄存器地址写入1字节数据。
    :param address: 设备地址
    :param reg: 寄存器地址 (16位)
    :param data: 要写入的数据 (8位)
    """
    try:
        reg_msb = (reg >> 8) & 0xFF  # 寄存器地址高8位
        reg_lsb = reg & 0xFF          # 寄存器地址低8位
        bus.write_i2c_block_data(address, reg_msb, [reg_lsb, data])
    except IOError as e:
        print(f"写入字节数据失败: {e}")

def I2C_A16V8_read_byte(address, reg):
    """
    从16位寄存器地址读取1字节数据。
    :param address: 设备地址
    :param reg: 寄存器地址 (16位)
    :return: 读取的数据 (8位)
    """
    try:
        reg_msb = (reg >> 8) & 0xFF  # 寄存器地址高8位
        reg_lsb = reg & 0xFF          # 寄存器地址低8位
        bus.write_i2c_block_data(address, reg_msb, [reg_lsb])
        data = bus.read_byte(address)
        return f"0x{data:02X}"
    except IOError as e:
        print(f"读取字节数据失败: {e}")
        return None

def I2C_A16V8_write_bytes(address, reg, data_list):
    """
    向16位寄存器地址开始的连续地址写入多个字节数据。
    :param address: 设备地址
    :param reg: 起始寄存器地址 (16位)
    :param data_list: 要写入的数据列表 (每个数据为8位)
    """
    try:
        reg_msb = (reg >> 8) & 0xFF  # 寄存器地址高8位
        reg_lsb = reg & 0xFF          # 寄存器地址低8位
        bus.write_i2c_block_data(address, reg_msb, [reg_lsb] + data_list)
    except IOError as e:
        print(f"写入多个字节数据失败: {e}")

def I2C_A16V8_read_bytes(address, reg, length):
    """
    从16位寄存器地址开始的连续地址读取多个字节数据。
    :param address: 设备地址
    :param reg: 起始寄存器地址 (16位)
    :param length: 要读取的字节数
    :return: 读取的数据列表
    """
    try:
        reg_msb = (reg >> 8) & 0xFF  # 寄存器地址高8位
        reg_lsb = reg & 0xFF          # 寄存器地址低8位
        bus.write_i2c_block_data(address, reg_msb, [reg_lsb])
        read = i2c_msg.read(address, length)
        bus.i2c_rdwr(read)
        return [f"0x{byte:02X}" for byte in list(read)]
    except IOError as e:
        print(f"读取多个字节数据失败: {e}")
        return []

def I2C_A16V16_write_2byte(address,reg, write_data):
    try:
        Reg_MSB = (reg >> 8) & 0xFF
        Reg_LSB = reg & 0xFF
        write_data_MSB = (write_data >> 8) & 0xFF
        write_data_LSB = write_data & 0xFF
        msg = i2c_msg.write(address, [Reg_MSB, Reg_LSB, write_data_MSB, write_data_LSB])
        bus.i2c_rdwr(msg)
    except IOError as e:
        print(f"写入数据失败: {e}")
def I2C_A16V16_write_2byte_LSB(address,reg, write_data):
    try:
        Reg_MSB = (reg >> 8) & 0xFF
        Reg_LSB = reg & 0xFF
        write_data_MSB = (write_data >> 8) & 0xFF
        write_data_LSB = write_data & 0xFF
        msg = i2c_msg.write(address, [Reg_MSB, Reg_LSB, write_data_LSB, write_data_MSB])
        bus.i2c_rdwr(msg)
    except IOError as e:
        print(f"写入数据失败: {e}")

def i2c_A8V8_write(I2C_ADDRESS, address, data):
    """
    I2C 写操作（8位地址 + 8位数据）
    :param address: 8位寄存器地址
    :param data: 8位写入数据
    """
    try:
        msg = i2c_msg.write(I2C_ADDRESS, [address, data])
        bus.i2c_rdwr(msg)
        time.sleep(0.01)  # 短暂延时，确保设备处理完成
    except IOError as e:
        print(f"I2C 写入操作失败: {e}")

def i2c_A8V8_read(I2C_ADDRESS, address):
    """
    I2C 读操作（8位地址 + 8位数据）
    :param address: 8位寄存器地址
    :return: 读取的8位数据
    """
    try:
        write_msg = i2c_msg.write(I2C_ADDRESS, [address])
        read_msg = i2c_msg.read(I2C_ADDRESS, 1)
        bus.i2c_rdwr(write_msg, read_msg)
        return list(read_msg)[0]
    except IOError as e:
        print(f"I2C 读取操作失败: {e}")
        return None

def i2c_write_block(I2C_ADDRESS, start_address, data_list):
    """
    I2C 连续写操作（从起始地址开始写入多个8位数据）
    :param start_address: 起始8位寄存器地址
    :param data_list: 要写入的数据列表
    """
    try:
        msg = i2c_msg.write(I2C_ADDRESS, [start_address] + data_list)
        bus.i2c_rdwr(msg)
        time.sleep(0.01)
    except IOError as e:
        print(f"I2C 连续写入操作失败: {e}")

def i2c_read_block(I2C_ADDRESS, start_address, length):
    """
    I2C 连续读操作（从起始地址开始读取多个8位数据）
    :param start_address: 起始8位寄存器地址
    :param length: 读取长度
    :return: 读取的8位数据列表
    """
    try:
        write_msg = i2c_msg.write(I2C_ADDRESS, [start_address])
        read_msg = i2c_msg.read(I2C_ADDRESS, length)
        bus.i2c_rdwr(write_msg, read_msg)
        return list(read_msg)
    except IOError as e:
        print(f"I2C 连续读取操作失败: {e}")
        return []

def close_bus():
    try:
        bus.close()  # 关闭 I2C 总线
    except IOError as e:
        print(f"关闭 I2C 总线失败: {e}")
#CM421函数
def cm421_reset():
  time.sleep(0.01)
  cm421_write_2byte(0x0018,0x0001)
  time.sleep(0.004)
  cm421_write_2byte(0x0024,0x0001)
  time.sleep(0.01)
def cm421_mcu_on():
    cm421_write_2byte(0x0024,0x0001)
    time.sleep(0.01)
def cm421_Servo_on():
    cm421_write_2byte(0x9b2c,0x0001)
    time.sleep(0.01)
    cm421_write_2byte(0x9b2a,0x0002)
    time.sleep(0.01)
    a=cm421_read_2byte(0x9b28)
    if r"0x1002"==a:
        print("cm421 Servo on success")
    else:
        print("cm421 Servo on failed")
    time.sleep(0.2)
def cm421_OIS_ON():
    cm421_write_2byte(0x9b2c,0x0001)
    time.sleep(0.01)
    cm421_write_2byte(0x9b2a,0x0001)
    time.sleep(0.01)
    if cm421_read_2byte(0x9b28) == r"0x1001": 
        print("cm421 OIS on success")
    else:
        print("cm421 OIS on failed")
    time.sleep(0.02)
def cm421_read_resistance():

   
    resistance0_4=cm421_Sequential_read(0x97fc,4)
    if resistance0_4:
       resistance0_4_int = []
       for item in resistance0_4:
        try:
            # 将十六进制字符串转换为整数
            resistance0_4_int.append(int(item, 16))
        except ValueError:
            print(f"无法将值 {item} 转换为整数，请检查返回数据格式。")
    #    print("转换后的整数值:", resistance0_4_int)
    else:
        print("未成功读取数据，请检查通信是否正常。")
   
    return resistance0_4_int
    
def read_txt_file(file_path):
    """
    读取Txt文件内容并返回
    :param file_path: Txt文件路径
    :return: 文件内容字符串，如果文件不存在或读取失败则返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
    return None
def process_hex_content(content):
    """
    直接处理content字符串，将每行2位16进制数转换为0x格式并每4字节组成一个word
    :param content: 包含16进制数据的字符串（每行一个2位16进制数）
    :return: 转换后的word列表
    """
    # 按行分割内容并过滤空行
    lines = [line.strip() for line in content.split('\n') if line.strip()]

    # 转换为0x格式并验证
    hex_values = []
    for i, line in enumerate(lines, 1):
        if len(line) != 2:
            print(f"警告：第{i}行 '{line}' 不是2位字符，已跳过")
            continue
        try:
            # 转换为0x格式（小写）
            hex_values.append(f"0x{line.lower()}")
        except ValueError:
            print(f"警告：第{i}行 '{line}' 不是有效的16进制数，已跳过")

    # 每4个字节组成一个word
    words = []
    for i in range(0, len(hex_values), 4):
        # 取4个元素，不足时用0x00填充
        chunk = hex_values[i:i+4] + ['0x00']*(4 - len(hex_values[i:i+4]))
        # 格式化为{0x.., 0x.., 0x.., 0x..}形式
        word_str = f"{{{', '.join(chunk)}}}"
        words.append(word_str)

    return words
# def FW_download_program():
#     cm421_write_2byte(0x0024,0x0000)
#     cm421_write_2byte(0x0220,0xc0d4)
#     cm421_write_2byte(0x3000,0x0000)
#     for i in range(16):
#       addr = 0x8000 + i * 0x0800
#       print(addr)
#       cm421_write_2byte(0x3008, addr)
#       cm421_write_2byte(0x300C, 0x0002) 
#     cm421_write_2byte(0x3028, 0x8000)
#     cm421_write_2byte(0x304C, 0x2000)

#     cm421_write_2byte(0x3048, 0x8000)
#     cm421_write_2byte(0x304C, 0x2000)

#     # 启动校验
#     cm421_write_2byte(0x3050, 0x0001)

# # 读取结果
#     cs1 = cm421_read_2byte(0x3054)
#     cs2 = cm421_read_2byte(0x3058)
#     checksum_result = (cs1 << 16) | cs2

#     # 比较校验值
#     print("Expected checksum: 0x%08X" % checksum_expected)
#     print("Device   checksum: 0x%08X" % checksum_result)
#     if checksum_result != checksum_expected:
#         print("❌ Checksum mismatch!")
#     else:
#         print("✅ Checksum OK!")

#     # 复位
#     write_2byte(0x0018, 0x0001)
#     time.sleep(0.01)   




# # 使用示例
# if __name__ == "__main__":
#     txt_path = input("请输入Txt文件路径: ")
#     content = read_txt_file(txt_path)
#     if content:
#         print("文件内容如下:\n")
#         print(content)
#     print(process_hex_content(content))  


# cm421_reset()
# # #cm421_mcu_on()
# cm421_Servo_on()
# time.sleep(0.1)
# cm421_OIS_ON()
# time.sleep(0.1)
# print(cm421_read_2byte(0x9b28))
# time.sleep(0.1)
# a=cm421_read_resistance()
# print(a)
# close_bus()
A=I2C_A16V8_read_byte(0X6F,0xF924)
print(A)