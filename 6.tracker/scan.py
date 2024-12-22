from bleak import BleakScanner
import asyncio

def on_advertisement(device, advertisement_data):
    if device.address.startswith("EC:3F"):
        print(f"Device {device} found with advertisement data: {advertisement_data}")

async def run():
    scanner = BleakScanner(on_advertisement)
    await scanner.start()
    while True:
        await asyncio.sleep(3)

asyncio.run(run())
