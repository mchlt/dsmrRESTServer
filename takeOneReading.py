#!/usr/bin/env python3

import json
from re import sub
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
from dsmr_parser.objects import CosemObject, MBusObject, Telegram
from dsmr_parser.parsers import TelegramParser

serial_reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings=SERIAL_SETTINGS_V5,
    telegram_specification=telegram_specifications.V4
)

# function to convert string to camelCase
def camelCase(string):
  string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
  return string[0].lower() + string[1:]

new_dsmr_json={}

if __name__ == '__main__':
    telegram = next(serial_reader.read_as_object())
    dsmr_json = json.loads(telegram.to_json())
    for key in dsmr_json.keys():
        new_key = camelCase(key)
        new_dsmr_json[new_key] = dsmr_json[key]
    print(json.dumps(new_dsmr_json,indent=3))


