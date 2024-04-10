# UART-DEVICE

uart-device emulates serial device using `socat` command. It is used for development purposes to test uart-server.
It feeds random data to uart-server and emulates logic of all the required commands.

## Preparation:

1. install socat: `sudo apt-get install socat`
2. create virtual environment: `python -m venv .venv`
3. activate virtual environment: `source .venv/bin/activate`
4. install requirements: `python -m pip install -r requirements.txt`
5. create .env file: `cp .env.example .env`

## Running the device:

1. run `./startup.sh`. It automatically runs the device and creates virtual port.

## Configuration:

uart-device can be configured using env vars or .env file. List of supported variables:

- `DEVICE_PORT` - path to uart-device port. Defaults to `../device_port`
- `CLIENT_PORT` - path to uart-client port. Defaults to `../client_port`
- `BAUD_RATE` - ports baud rate. Defaults to `115000`
- `HOST` - API host. Defaults to `localhost`
- `PORT` - API port. Defaults to `8080`

## API:

uart-device exposes single endpoint `GET /device` that returns info about uart-device state.

#### example response:
```json
{
  "is_writing": true,
  "frequency": 10,
  "debug": true,
  "last_messages": [
    "$267.25,184.25,746.5\n",
    "$895.0,329.0,417.0\n",
    "$316.5,473.0,690.0\n",
    "$571.5,416.5,319.5\n",
    "$705.5,781.0,285.25\n",
    "$450.5,705.5,211.875\n",
    "$499.0,733.0,963.5\n",
    "$643.0,333.0,633.0\n",
    "$2.443359375,24.453125,836.0\n",
    "$257.5,628.5,195.125\n"
  ],
  "last_commands": []
}
```

## Swagger:

Interactive Swagger UI is available under `/` and `/docs`


## Tests:

To run tests use `pytest` in the root directory of the project.
