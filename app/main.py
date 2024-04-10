from threading import Thread

from app.socat_serial import SocatSerial
from app.uart_device import UARTDevice

from os import getenv, kill, getpid
from logging import info, basicConfig, INFO
from signal import SIGINT
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

load_dotenv()
device_port = getenv('DEVICE_PORT', './tty_device')
client_port = getenv('CLIENT_PORT', './tty_client')
baud_rate = int(getenv('BAUD_RATE', '115000'))

basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=INFO)
app = FastAPI()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse('/docs')


@app.get("/device")
def device():
    return app.device.state()


@app.on_event("startup")
def startup_event():
    info('Starting virtual UART device')
    info('SIGINT to stop')
    info(f'DEVICE_PORT: {device_port}')
    info(f'CLIENT_PORT: {client_port}')
    info(f'BAUD_RATE: {baud_rate}')

    def worker():
        try:
            app.device.work()
        except:
            kill(getpid(), SIGINT)

    serial = SocatSerial(device_port, client_port, baud_rate)
    app.device = UARTDevice(serial)

    app.worker_thread = Thread(target=worker)
    app.worker_thread.start()


@app.on_event("shutdown")
def app_shutdown():
    info('Stopping worker thread')
    app.device.stop()
    app.worker_thread.join()
    info('Virtual UART device stopped')

