from driver_core.driver import DriverIml
from driver_core.virtual_device import VirtualDevice


from rest_api.rest_api_server import RestAPIServer


if __name__ == '__main__':
    device = VirtualDevice()
    driver = DriverIml(device)
    server = RestAPIServer(driver)
    server.start()