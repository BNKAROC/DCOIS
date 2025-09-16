from smbus3 import SMBus, i2c_msg
import time

# 使用 I2C 总线号 1（大多数树莓派的默认设置）
bus = SMBus(1)

# I2C 地址的范围通常是 0x03 到 0x77
def scan_i2c_bus():
    print("正在扫描 I2C 总线...")
    devices = []
    for address in range(0x03, 0x78):
        try:
            # 尝试向设备发送空消息，若无异常，则该地址存在从机
            bus.write_quick(address)
            devices.append(hex(address))
        except OSError:
            # 如果抛出 OSError 说明该地址没有设备
            pass
    return devices

if __name__ == "__main__":
    detected_devices = scan_i2c_bus()
    if detected_devices:
        print(f"检测到的 I2C 设备地址: {', '.join(detected_devices)}")
    else:
        print("未检测到任何 I2C 设备。")
