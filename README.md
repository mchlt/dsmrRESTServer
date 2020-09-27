# dsmrRESTServer
Threaded REST server to serve Dutch Meter System Requirements (DSMR) readings

I use a dsmr to usb cable (like this one: https://gadget-freakz.com/product/smart-meter-cable-p1-dutch-dsmr-cable/) with a Raspberry Pi to read the Smart Meter.

Because the Raspberry pi is not good at handling many read/write son its local filesystem (SD card) over long periods (the cards just fail eventually), I decided to simply make a very small server that just takes meter readings and publishes them as a REST service.  I can then take these readings from another server (or website, app, etc) and do with them what I need.

The serial process that takes the meter readings is blocking, so I made the server multi-threaded to make sure mutiple requests can be handled as quickly as possible.

Most of the work to take the meter readsings is done by the excellent https://github.com/ndokter/dsmr_parser module.

takeOneReading.py is provided for testing. It takes one reading and prints the json to screen. Use it to test all is set up properly before startinmg the server.

dsmrRESTServer.py is the server. run it for example like this:
```
nohup python3 dsmrRESTServer.py 2>&1 >/dev/null &
```

## example output
```
{
   "p1MessageHeader": {
      "value": "50",
      "unit": null
   },
   "p1MessageTimestamp": {
      "value": "2020-09-27T20:26:14+02:00",
      "unit": null
   },
   "equipmentIdentifier": {
      "value": "1234567890123456789012345678901234",
      "unit": null
   },
   "electricityUsedTariff1": {
      "value": 3466.018,
      "unit": "kWh"
   },
   "electricityUsedTariff2": {
      "value": 4076.197,
      "unit": "kWh"
   },
   "electricityDeliveredTariff1": {
      "value": 341.672,
      "unit": "kWh"
   },
   "electricityDeliveredTariff2": {
      "value": 757.504,
      "unit": "kWh"
   },
   "electricityActiveTariff": {
      "value": "0001",
      "unit": null
   },
   "currentElectricityUsage": {
      "value": 0.355,
      "unit": "kW"
   },
   "currentElectricityDelivery": {
      "value": 0.0,
      "unit": "kW"
   },
   "shortPowerFailureCount": {
      "value": 4,
      "unit": null
   },
   "longPowerFailureCount": {
      "value": 3,
      "unit": null
   },
   "powerEventFailureLog": {
      "buffer_length": 1,
      "buffer_type": "0-0:96.7.19",
      "buffer": [
         {
            "datetime": "2018-12-03T19:20:15+01:00",
            "value": 9884,
            "unit": "s"
         }
      ]
   },
   "voltageSagL1Count": {
      "value": 11,
      "unit": null
   },
   "voltageSagL2Count": {
      "value": 8,
      "unit": null
   },
   "voltageSagL3Count": {
      "value": 11,
      "unit": null
   },
   "voltageSwellL1Count": {
      "value": 1,
      "unit": null
   },
   "voltageSwellL2Count": {
      "value": 1,
      "unit": null
   },
   "voltageSwellL3Count": {
      "value": 1,
      "unit": null
   },
   "textMessage": {
      "value": null,
      "unit": null
   },
   "deviceType": {
      "value": 3,
      "unit": null
   },
   "instantaneousCurrentL1": {
      "value": 0.0,
      "unit": "A"
   },
   "instantaneousCurrentL2": {
      "value": 2.0,
      "unit": "A"
   },
   "instantaneousCurrentL3": {
      "value": 0.0,
      "unit": "A"
   },
   "instantaneousActivePowerL1Positive": {
      "value": 0.0,
      "unit": "kW"
   },
   "instantaneousActivePowerL2Positive": {
      "value": 0.346,
      "unit": "kW"
   },
   "instantaneousActivePowerL3Positive": {
      "value": 0.01,
      "unit": "kW"
   },
   "instantaneousActivePowerL1Negative": {
      "value": 0.0,
      "unit": "kW"
   },
   "instantaneousActivePowerL2Negative": {
      "value": 0.0,
      "unit": "kW"
   },
   "instantaneousActivePowerL3Negative": {
      "value": 0.0,
      "unit": "kW"
   },
   "equipmentIdentifierGas": {
      "value": "4730303332353635353135323133393137",
      "unit": null
   },
   "hourlyGasMeterReading": {
      "datetime": "2020-09-27T20:25:04+02:00",
      "value": 3297.485,
      "unit": "m3"
   }
}
```
