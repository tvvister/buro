import asyncio
from concurrent.futures import ThreadPoolExecutor
from driver import DriverIml
from virtual_device import VirtualDevice

def call(driver):
    asyncio.run(driver.start_log())

def main():
    device = VirtualDevice()
    driver = DriverIml(device)

    with ThreadPoolExecutor() as executor:
        executor.submit(call, driver)
        value = 0

        while (True):
            asyncio.run(asyncio.sleep(3))
            asyncio.run(driver.start_channel(2, value, value+1))
            value += 1


if __name__ == '__main__':

    main()
