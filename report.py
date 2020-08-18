from flask import make_response, abort
from pynats import NATSClient
import json
import threading

client = NATSClient("nats://127.0.0.1:4222")
Channels = {'data': [], 'meta': []}

def SetOutputChannels(channels):
    Channels = channels


def Process(report):

    print(report)
    print("Payload: {}".format(report.get("payload_raw", None)))
    print("Serial: {}".format(report.get("hardware_serial", None)))
    metadata = report.get("metadata", None)
    data = json.dumps(report)
    print("Time: {}".format(metadata.get("time", None)))


    client.connect()

    for channel in Channels['data']:
        client.publish(channel, payload=data)

    for channel in Channels['meta']:
        client.publish(channel, payload=metadata)

    client.close()

    return make_response("Sensor report successfully processed", 201)