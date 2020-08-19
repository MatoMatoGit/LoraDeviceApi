from flask import make_response, abort
from pynats import NATSClient
import json
import threading

client = NATSClient("nats://127.0.0.1:4222")
Channels = {'data': [], 'meta': [], 'url': []}
Callbacks = []

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
	url = report.get("downlink_serial", None)
    metadata = report.get("metadata", None)
	time = metadata.get("time", None)

    data = json.dumps({"dev_id": dev_id, "time": time, "data": payload})

    print("Payload: {}".format(payload))
    print("Serial: {}".format(dev_id))
    print("Time: {}".format(time))

	for cb in Callbacks:
		cb(url)

    client.connect()

    for channel in Channels['data']:
        client.publish(channel, payload=data)

    for channel in Channels['meta']:
        client.publish(channel, payload=metadata)
	
    client.close()

    return make_response("Sensor report successfully processed", 201)
