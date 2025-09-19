from smbus3 import SMBus
import time

def scan_i2c_bus(bus_id=1):
    print(f"正在扫描 I2C 总线 {bus_id} ...")
    devices = []
    with SMBus(bus_id) as bus:
        for address in range(0x03, 0x78):
            try:
                bus.read_byte(address)  # 比 write_quick 更兼容
                devices.append(hex(address))
            except OSError:
                pass

        bus.close()
    return devices

if __name__ == "__main__":
    detected_devices = scan_i2c_bus(0)  # Pi 5 默认 I2C0
    if detected_devices:
        print(f"检测到的 I2C 设备地址: {', '.join(detected_devices)}")
    else:
        print("未检测到任何 I2C 设备。")
