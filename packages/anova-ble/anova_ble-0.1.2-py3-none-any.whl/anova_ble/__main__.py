import time
import bleak
from . import AnovaBLEPrecisionCooker, _LOGGER
import asyncio

import logging
logging.basicConfig(level=logging.INFO)

async def discover():
    "Look for an Anova sous-vide machine"
    devs = await bleak.BleakScanner.discover()

    for dev in devs:
        print(dev)
        if dev.name == "Anova":
            return dev

async def main():
    ble_dev = await discover()
    _LOGGER.debug(ble_dev)
    anova = AnovaBLEPrecisionCooker(ble_device=ble_dev)
    
    time.sleep(1)
    _LOGGER.info(await anova.update_state())
    time.sleep(3)

    await asyncio.gather(
        anova.start(),
        anova.update_state()
    )

    await anova.stop()

if __name__ == "__main__":
    asyncio.run(main())