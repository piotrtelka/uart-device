import serial
import subprocess
import time


class SocatSerial:
    def __init__(self, device_port: str, client_port: str, baud_rate: int = 9600):
        cmd = [
            '/usr/bin/socat',
            '-d',
            '-d',
            'PTY,link=%s,raw,echo=0' % device_port,
            'PTY,link=%s,raw,echo=0' % client_port
        ]

        self.proc = subprocess.Popen(cmd)
        time.sleep(1)  # wait for the process to start. You can monitor stdout as well.
        self.serial = serial.Serial(device_port, baud_rate, rtscts=True, dsrdtr=True, timeout=1)

    def write(self, out: bytes):
        self.serial.write(out)
        self.serial.flush()

    def bytes_available(self) -> int:
        return self.serial.in_waiting

    def readline(self):
        return self.serial.readline().decode('utf-8')

    def __del__(self):
        self.stop()

    def stop(self):
        self.proc.kill()
        self.proc.communicate()
