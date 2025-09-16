import cm421_i2c
import time
from smbus3 import SMBus, i2c_msg
import math
aw_addr=0x6f
cm421_i2c.bus=bus = SMBus(0) 
def flash_read(offset_addr,length):
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0x0001,0x00)
    time.sleep(0.1)
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0x007f,0xA4)
    time.sleep(0.1)
    cm421_i2c.I2C_A16V16_write_2byte_LSB(aw_addr,0xfd00,offset_addr)
    time.sleep(0.1)
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0xfd02, math.ceil(length / 4))
    time.sleep(0.1)
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0xfd84,0x01)
    time.sleep(0.01)
    data=cm421_i2c.I2C_A16V8_read_bytes(aw_addr,0xfd04,length)
    # print(data)
    return data
def flash_erase(offset_addr,block_num):
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0x0001,0x00)
    time.sleep(0.1)
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0x007f,0xA4)
    time.sleep(0.1)
    cm421_i2c.I2C_A16V16_write_2byte_LSB(aw_addr,0xfd00,offset_addr)
    time.sleep(0.1)
    cm421_i2c.I2C_A16V16_write_2byte_LSB(aw_addr,0xfd02,block_num)
    cm421_i2c.I2C_A16V8_write_byte(aw_addr,0xfd84,0x03)
    time.sleep(0.01*block_num)
def flash_write(offset_addr, data_list):
    # 1. OIS off
    msg = i2c_msg.write(0x6F, [0x00, 0x01, 0x00])  
    bus.i2c_rdwr(msg)
    time.sleep(0.1)
    # 2. Unlock registers
    msg = i2c_msg.write(0x6F, [0x00, 0x7F, 0xA4])
    bus.i2c_rdwr(msg)
    time.sleep(0.1)
    # 3. Write offset address
    msg = i2c_msg.write(0x6F, [0xFD, 0x00, (offset_addr >> 8) & 0xFF, offset_addr & 0xFF])
    bus.i2c_rdwr(msg)
    print("写入偏移地址:", offset_addr)
    # 4. Number of data written (单位 word, 1 word = 4 byte)
    num_words = math.ceil(len((data_list))/4) 
    msg = i2c_msg.write(0x6F, [0xFD, 0x02,num_words & 0xFF, (num_words >> 8) & 0xFF])
    bus.i2c_rdwr(msg)
    time.sleep(0.1)
    # 5. Write data（支持超过 32 字节）
    msg = i2c_msg.write(0x6F, [0xFD, 0x04] + data_list)
    bus.i2c_rdwr(msg)

    

    # 6. Flash write instruction
    msg = i2c_msg.write(0x6F, [0xFD, 0x84, 0x02])
    bus.i2c_rdwr(msg)

    # 7. Delay（1 block 10ms）
    time.sleep(0.01 * num_words)
  
    # cm421_i2c.I2C_A16V8_write_byte(aw_addr,0xfd84,0x02)
    

