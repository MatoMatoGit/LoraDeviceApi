from flask import make_response, abort
from kafka import KafkaProducer
import json
import threading
from Decode import Decoder


Channels = {'data': [], 'meta': [], 'url': []}
Callbacks = []
Producer = KafkaProducer()
Decoder = Decoder()

def SetOutputChannels(channels):
    Channels = channels

def AddUrlCallback(callback):
	Callbacks.add(callback)

def RemoveUrlCallback(callback):
	Callbacks.remove(callback)

def Process(report):

    print(report)
    payload = report.get("payload_raw", None)
    dev_id = report.get("hardware_serial", None)
    url = report.get("downlink_url", None)
    metadata = report.get("metadata", None)
    time = metadata.get("time", None)

    gateway = metadata.get("gateways", None)[0]
    rssi = gateway["rssi"]
    snr = gateway["snr"]

    print("Payload (raw): {}".format(payload))

    payload = Decoder.Decode(payload)

    data = json.dumps({"dev_id": dev_id, "rssi": rssi, "snr": snr, "time": time, "data": payload})

    print("Payload (decoded): {}".format(payload))
    print("Serial: {}".format(dev_id))
    print("Time: {}".format(time))
    print("RSSI: {}".format(rssi))
    print("SNR: {}".format(snr))

    for cb in Callbacks:
        cb(url)

    Producer.send('test.topic', data.encode('utf-8'))

    try:

        file_path = "./lora_uplink_" + str(time)
        file = open(file_path, 'w')

        file.write(data)
        file.close()
    except:
        print("Failed to create a file.")

    #
    # client.connect()
    #
    # for channel in Channels['data']:
    #     client.publish(channel, payload=data)
    #
    # for channel in Channels['meta']:
    #     client.publish(channel, payload=metadata)
    #
    # client.close()

    return make_response("Sensor report successfully processed", 201)
