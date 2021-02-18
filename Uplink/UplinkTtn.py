from flask import make_response, abort
from Decode import Decoder

Decoder = Decoder()
Uplink = None

NETWORK_TTN = "ttn"


def SetUplink(uplink):
    global Uplink
    Uplink = uplink


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

    payload = Decoder.ParseCbor(Decoder.Base64ToAscii(payload))

    print("SNR: {}".format(snr))

    try:
        Uplink.Send(raw=uplink_msg, network=NETWORK_TTN, dev_id=dev_id, rssi=rssi, payload=payload)
    except:
        print("Failed to create a file.")
        return make_response("Uplink message could not be stored", 500)

    # try:
    #
    #     file_path = "./uplink_data/lora_uplink_" + str(time)
    #     file = open(file_path, 'w')
    #
    #     file.write(data)
    #     file.close()
    # except OSError:
    #     print("Failed to create a file.")
    #     return make_response("Uplink message could not be stored", 500)

    # TODO: Return 500 if data cannot be processed.

    return make_response("Uplink message successfully stored", 201)
