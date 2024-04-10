import random
from logging import info
from re import match
from time import sleep
from numpy import float16


def is_start(command: str) -> bool:
    return command == '$0\n'


def is_stop(command: str) -> bool:
    return command == '$1\n'


def is_configure(command: str) -> bool:
    return match(r'^\$2,\d+,(?:true|false)\n$', command) is not None


class UARTDevice:
    def __init__(self, serial):
        self.serial = serial
        self.is_working = True
        self.is_writing = True
        self.frequency = 10
        self.debug = True
        self.last_messages = []
        self.last_commands = []

    def work(self):
        while self.is_working:
            if self.serial.bytes_available() > 0:
                self.__process_command(self.serial.readline())
            if self.is_writing:
                self.__write_message()
            sleep(1.0 / self.frequency)

    def state(self):
        return {
            'is_writing': self.is_writing,
            'frequency': self.frequency,
            'debug': self.debug,
            'last_messages': self.last_messages,
            'last_commands': self.last_commands
        }

    def stop(self):
        self.is_working = False

    def __write_message(self):
        value1 = float16(random.uniform(0, 1000))
        value2 = float16(random.uniform(0, 1000))
        value3 = float16(random.uniform(0, 1000))
        message = f'${value1},{value2},{value3}\n'
        self.serial.write(message.encode('utf-8'))
        self.__add_last_message(message)

    def __process_command(self, command: str):
        if command is None:
            return
        elif is_start(command):
            info('Got start command')
            self.is_writing = True
            self.serial.write(b'$0,ok\n')
        elif is_stop(command):
            info('Got stop command')
            self.is_writing = False
            self.serial.write(b'$1,ok\n')
        elif is_configure(command):
            info('Got configure command')
            result = self.__configure(command)
            self.serial.write(f'$2,{result}\n'.encode('utf-8'))
        else:
            self.serial.write(b'$3,invalid command\n')

        self.__add_last_command(command)

    def __configure(self, command: str):
        values = [value.rstrip('\n') for value in command.strip().split(',')]

        frequency = int(values[1])

        if frequency < 1 or frequency > 100:
            return 'frequency should be within range [1, 100]'

        self.frequency = int(values[1])
        self.debug = values[2] == 'true'

        return 'ok'

    def __add_last_message(self, message: str):
        if len(self.last_messages) >= 10:
            self.last_messages.pop(0)

        self.last_messages.append(message)

    def __add_last_command(self, command: str):
        if len(self.last_commands) >= 10:
            self.last_commands.pop(0)

        self.last_commands.append(command)
