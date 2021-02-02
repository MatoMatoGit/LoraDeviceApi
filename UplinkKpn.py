from flask import make_response, abort
# from kafka import KafkaProducer
import json
import threading
from Decode import Decoder
from datetime import date
from datetime import datetime


Channels = {'raw': [], 'data': []}
Callbacks = []
#Producer = KafkaProducer()
Decoder = Decoder()

NETWORK_KPN = "kpn"


def SetOutputChannels(channels):
    global Channels
    Channels = channels


def Process(uplink_msg):

    try:
        print(uplink_msg)
        metadata = uplink_msg[0]
        print(metadata)
        payload_obj = uplink_msg[1]
        payload = payload_obj.get("vs", None)
        port = uplink_msg[2].get("v", None)

        dev_id = metadata.get("bn", None)
        # url = uplink_msg.get("downlink_url", None)
        # metadata = uplink_msg.get("metadata", None)
        time = metadata.get("bt", None)
        print(payload_obj)
        print(port)
    except KeyError:
        return make_response("Uplink message is malformed.", 400)

    print("Payload (raw): {}".format(payload))
    #
    # payload = Decoder.Decode(payload)
    #
    data = json.dumps({"network": NETWORK_KPN, "dev_id": dev_id, "rssi": 0,
                       "snr": 0, "time": time, "data": payload})
    #
    # print("Payload (decoded): {}".format(payload))
    print("Serial: {}".format(dev_id))
    print("Time: {}".format(time))

    #
    # for cb in Callbacks:
    #     cb(url)
    #
    try:

        today = date.today()
        time = datetime.now().strftime("%H:%M:%S")
        timestamp = ("{}-{}-{}T{}Z".format(today.year,
                                           today.month,
                                           today.day,
                                           time))
        file_path = "./uplink_data/lora_uplink_" + timestamp
        file = open(file_path, 'w')

        file.write(data)
        file.close()
    except OSError:
        print("Failed to create a file.")
        return make_response("Uplink message could not be stored", 500)
    #
    # for channel in Channels['raw']:
    #     print("Sending raw on channel: {}".format(channel))
    #     Producer.send(channel, str(uplink_msg).encode('utf-8'))
    #
    # for channel in Channels['data']:
    #     print("Sending data on channel: {}".format(channel))
    #     Producer.send(channel, data.encode('utf-8'))

    # TODO: Return 500 if data cannot be processed.

    return make_response("Uplink message successfully stored", 201)
