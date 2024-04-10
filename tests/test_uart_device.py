import serial

from app.socat_serial import SocatSerial
from app.uart_device import UARTDevice
from threading import Thread


class UARTDeviceThreaded:
    def __init__(self):
        self.device_port = './test_device_port'
        self.client_port = './test_client_port'
        self.baud_rate = 9600

        self.serial = SocatSerial(self.device_port, self.client_port, self.baud_rate)
        self.device = UARTDevice(self.serial)
        self.thread = Thread(target=lambda: self.device.work())
        self.thread.start()

    def stop(self):
        self.device.stop()
        self.thread.join()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __enter__(self):
        return self


def get_serial(device: UARTDeviceThreaded):
    return serial.Serial(device.client_port, device.baud_rate, rtscts=True, dsrdtr=True, timeout=1)


def stop_command():
    return b'$1\n'


def start_command():
    return b'$0\n'


def configure_command(frequency: int, debug: bool):
    return f'$2,{frequency},{debug}\n'.lower().encode('utf-8')


def test_start_stop_device():
    device = UARTDeviceThreaded()
    device.stop()


def test_receive_any_message():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        message = client_serial.readline().decode('utf-8')

        assert message.endswith('\n')
        assert message.startswith('$')


def test_stop_command():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        client_serial.write(stop_command())
        response = client_serial.readline().decode('utf-8')

        assert response == '$1,ok\n'
        assert not device.device.is_writing
        assert client_serial.in_waiting == 0


def test_start_command():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        client_serial.write(start_command())
        response = client_serial.readline().decode('utf-8')

        assert response == '$0,ok\n'
        assert device.device.is_writing


def test_stop_start():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        client_serial.write(stop_command())
        response = client_serial.readline().decode('utf-8')

        assert response == '$1,ok\n'
        assert not device.device.is_writing
        assert client_serial.in_waiting == 0

        client_serial.write(start_command())
        response = client_serial.readline().decode('utf-8')

        assert response == '$0,ok\n'
        assert device.device.is_writing

        message = client_serial.readline().decode('utf-8')

        assert message.endswith('\n')
        assert message.startswith('$')


def test_configure():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        client_serial.write(configure_command(100, False))

        response = client_serial.readline().decode('utf-8')

        assert response == '$2,ok\n'
        assert device.device.frequency == 100
        assert not device.device.debug


def test_invalid_configure():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        client_serial.write(configure_command(-2, False))

        response = client_serial.readline().decode('utf-8')

        assert response != '$2,ok\n'
        assert device.device.frequency != -2


def test_invalid_command():
    with UARTDeviceThreaded() as device:
        client_serial = get_serial(device)

        client_serial.write(b'invalid command\n')

        response = client_serial.readline().decode('utf-8')
        assert response == '$3,invalid command\n'
