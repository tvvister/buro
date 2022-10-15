import datetime
import re
import socket
import time


class Storage:
    channels = {i: {'STATe': 'OFF',
                    'VOLTage': 0.0,
                    'CURRent': 0.0,
                    'POWEr': 0.0}
                for i in range(1, 5)}


def server_program():
    vSource = Storage()

    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        try:
            if data:
                print('{} command: {}'.format(datetime.datetime.utcnow(), data))

                # handling SOURce command
                # :SOURce4:CURRent 23423.3
                regex = re.search(
                    '^:([a-zA-Z]+)(\d+):([a-zA-Z]+)\s(.*)$', data)
                if regex:
                    if regex.group(1) == 'SOURce':
                        channel = int(regex.group(2))
                        indicator = regex.group(3)
                        if indicator in vSource.channels.get(channel, {}):
                            vSource.channels[channel][indicator] = float(
                                regex.group(4))
                            data = 'Success'

                # handling OUTPut command
                # :OUTPut4:STATe ON
                regex = re.search('^:OUTPut(\d+):STATe\s(ON|OFF)$', data)
                if regex:
                    channel = int(regex.group(1))
                    vSource.channels.get(channel, {})['STATe'] = regex.group(2)
                    data = 'Success'

                # handling MEASure command
                # :MEASure4:CURRent?
                regex = re.search('^:MEASure(\d+):([a-zA-Z]+)\?$', data)
                if regex:
                    channel = int(regex.group(1))
                    indicator = regex.group(2)
                    channel_ent = vSource.channels.get(channel, {})
                    if indicator in channel_ent:
                        is_enabled = channel_ent['STATe'] == 'ON'
                        resp = (datetime.datetime.utcnow(),
                                channel_ent[indicator] if is_enabled else 0.0)
                        data = repr(resp)
                # conn.send((data + '\n' + repr(vSource.channels)).encode())
                conn.send(data.encode())
        except Exception:
            conn.send('Error...'.encode())
            raise

    conn.close()


if __name__ == '__main__':
    server_program()
