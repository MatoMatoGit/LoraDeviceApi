from kafka import KafkaProducer
import json
from datetime import datetime

UPLINK_CHANNEL_RAW = "raw"
UPLINK_CHANNEL_DATA = "data"


class Uplink:

    def __init__(self, channels):
        self.Producer = KafkaProducer()
        self.Channels = {UPLINK_CHANNEL_RAW: channels[UPLINK_CHANNEL_RAW],
                         UPLINK_CHANNEL_DATA: channels[UPLINK_CHANNEL_DATA]}
        return

    def Send(self, raw, network, dev_id, rssi, payload):
        time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        print("Payload (decoded): {}".format(payload))
        print("Device: {}".format(dev_id))
        print("Time: {}".format(time))
        print("RSSI: {}".format(rssi))

        data = json.dumps({"network": network,
                           "dev_id": dev_id,
                           "rssi": rssi,
                           "time": time,
                           "data": payload
                           })

        for channel in self.Channels[UPLINK_CHANNEL_RAW]:
            print("Sending raw on channel: {}".format(channel))
            self.Producer.send(channel, str(raw).encode('utf-8'))

        for channel in self.Channels[UPLINK_CHANNEL_DATA]:
            print("Sending data on channel: {}".format(channel))
            self.Producer.send(channel, data.encode('utf-8'))

        return


