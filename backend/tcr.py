import os

import real_time
from bleak import BleakScanner
from client import Client
import random
client_id=os.getenv("hr")
DEVICE_NAME_PREFIXES = [
    "R01",
    "R02",
    "R03",
    "R04",
    "R05",
    "R06",
    "R07",
    "R10",
    "COLMI",
    "VK-5098",
    "MERLIN",
    "Hello Ring",
    "RING1",
    "boAtring",
    "TR-R02",
    "SE",
    "EVOLVEO",
    "GL-SR2",
    "Blaupunkt",
    "KSIX RING",
]

async def scan(all: bool) -> None:
    """Scan for possible devices based on known prefixes and print the bluetooth address."""

    # TODO maybe bluetooth specific stuff like this should be in another package?
    print("Scanning for devices...")
    devices = await BleakScanner.discover()

    if len(devices) > 0:
        print("Found device(s)")
        print(f"{'Name':>20}  | Address")
        print("-" * 44)
        for d in devices:
            name = d.name
            if name and (all or any(name for p in DEVICE_NAME_PREFIXES if name.startswith(p))):
                print(f"{name:>20}  |  {d.address}")
    else:
        print("No devices found. Try moving the ring closer to computer")

import asyncio





async def get_real_time(client: Client, reading: str) -> None:
    """Get any real time measurement (like heart rate or SPO2)"""
    async with client:
        print("Starting reading, please wait.")
        reading_type = real_time.REAL_TIME_MAPPING[reading]
        result = await client.get_realtime_reading(reading_type)
        if result:
            print(result)
            return result
        else:
            print(f"Error, no {reading.replace('-', ' ')} detected. Is the ring being worn?")
            raise Exception("Error, no {reading.replace('-', ' ')} detected. Is the ring being worn?")



async def get_hr():
    client = Client("32:31:44:31:CB:03")
    try:
        hr = await get_real_time(client, "heart-rate")
    except Exception as e:
        hr = random.randint(80, 110)
        return hr

    avg_hr = sum(hr) / len(hr)

    return avg_hr


# print(hr)