import asyncio
from bleak import BleakClient, BleakScanner

address = "2C:CF:67:06:9A:38"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def main():
    async with BleakClient(address) as client:
        print("Connected:", client.is_connected)

        data = bytes ([100, 0, 0, 0, 0])  
        await client.write_gatt_char(CHAR_UUID, data, response=True)
        print("Wrote:", list(data))

asyncio.run(main())



