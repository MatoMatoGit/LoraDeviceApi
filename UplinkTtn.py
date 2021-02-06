from flask import make_response, abort
#from kafka import KafkaProducer
import json
import threading
from Decode import Decoder


Channels = {'raw': [], 'data': []}
Callbacks = []
#Producer = KafkaProducer()
Decoder = Decoder()

NETWORK_TTN = "ttn"


def SetOutputChannels(channels):
    global Channels
    Channels = channels


def Process(uplink_msg):

    try:
        print(uplink_msg)
        payload = uplink_msg.get("payload_raw", None)
        dev_id = uplink_msg.get("hardware_serial", None)
        url = uplink_msg.get("downlink_url", None)
        metadata = uplink_msg.get("metadata", None)
        time = metadata.get("time", None)

        gateway = metadata.get("gateways", None)[0]
        rssi = gateway["rssi"]
        snr = gateway["snr"]
        print("Payload (raw): {}".format(payload))
    except (KeyError, AttributeError):
        return make_response("Uplink message is malformed.", 400)

    payload = Decoder.Decode(payload)

    data = json.dumps({"network": NETWORK_TTN, "dev_id": dev_id, "rssi": rssi, "snr": snr, "time": time, "data": payload})

    print("Payload (decoded): {}".format(payload))
    print("Serial: {}".format(dev_id))
    print("Time: {}".format(time))
    print("RSSI: {}".format(rssi))
    print("SNR: {}".format(snr))

    for cb in Callbacks:
        cb(url)

    try:

        file_path = "./uplink_data/lora_uplink_" + str(time)
        file = open(file_path, 'w')

        file.write(data)
        file.close()
    except:
        print("Failed to create a file.")
        return make_response("Uplink message could not be stored", 500)

    for channel in Channels['raw']:
        print("Sending raw on channel: {}".format(channel))
        #Producer.send(channel, str(uplink_msg).encode('utf-8'))

    for channel in Channels['data']:
        print("Sending data on channel: {}".format(channel))
        #Producer.send(channel, data.encode('utf-8'))

    # TODO: Return 500 if data cannot be processed.

        return make_response("Uplink message successfully stored", 201)
