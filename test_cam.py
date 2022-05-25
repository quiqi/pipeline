import sys
import asyncio
from bleak import BleakClient

# 设备蓝牙地址
ADDRESS = "8C:CE:4E:A5:C2:E6"

# 设备蓝牙UUID
UART_RX_Heart_UUID = "00002a37-0000-1000-8000-0085f9b34fb"


# 发送开门数据
openDoor_send = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# 接收返回数据
openDoor_recive = [0x00, 0x00, 0x00, 0x00, 0x00, 0x0]

async def main(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")
        while client.is_connected:
            while paired == True:
                print("send data")
                await client.write_gatt_char(UART_RX_CHAR_UUID,bytes(openDoor_send))
                await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
                await asyncio.sleep(1.0)
            print('Paired False')
        print('Disconnected')

def print_hex(bytes):
    l = [hex(int(i)) for i in bytes]
    # print(" ".join(l))
    return(" ".join(l))

def handle_rx(_: int, data: bytearray):
    print("received:", print_hex(data))
    print("expect:", print_hex(openDoor_recive))
    hex_callback = print_hex(data)
    if hex_callback == print_hex(openDoor_recive):
        print('Data verification succeeded')
    else:
        print('Data verification failed')

async def main(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")
        while client.is_connected:
            while paired == True:
                print("send data")
                await client.write_gatt_char(UART_RX_CHAR_UUID,bytes(openDoor_send))
                await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
                await asyncio.sleep(1.0)
            print('Paired False')
        print('Disconnected')


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))

