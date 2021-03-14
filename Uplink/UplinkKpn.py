from flask import make_response, abort
from Decode import Decoder

Decoder = Decoder()
Uplink = None

NETWORK_KPN = "kpn"


def SetUplink(uplink):
    global Uplink
    Uplink = uplink


def Process(uplink_msg):

    try:
        print(uplink_msg)
        metadata = uplink_msg[0]
        print(metadata)
        payload_obj = uplink_msg[1]
        payload = payload_obj.get("vs", None)
        port = uplink_msg[2].get("v", None)
        dev_id = metadata.get("bn", None) # Formatted as 'urn:dev:DEVEUI:0059AC00001B0808:'
        dev_id = dev_id.split(':')[-2]  # Get the second to last part of the DEVEUI
        time = metadata.get("bt", None)
        print(payload_obj)
        print(port)
    except (KeyError, AttributeError):
        return make_response("Uplink message is malformed.", 400)

    print("Payload (raw): {}".format(payload))
    payload_b = bytearray()
    payload_b.extend(map(ord, payload))
    print("Payload (hex): {}".format(payload_b))
    payload = Decoder.ParseCbor(payload_b)

    try:
        Uplink.Send(raw=uplink_msg, network=NETWORK_KPN, dev_id=dev_id, rssi=0, payload=payload)
    except:
        print("Failed to create a file.")
        return make_response("Uplink message could not be stored", 500)

    # try:
    #
    #     today = date.today()
    #     time = datetime.now().strftime("%H:%M:%S")
    #     timestamp = ("{}-{}-{}T{}Z".format(today.year,
    #                                        today.month,
    #                                        today.day,
    #                                        time))
    #     file_path = "./uplink_data/lora_uplink_" + timestamp
    #     file = open(file_path, 'w')
    #
    #     file.write(data)
    #     file.close()
    # except OSError:
    #     print("Failed to create a file.")
    #     return make_response("Uplink message could not be stored", 500)


    # TODO: Return 500 if data cannot be processed.

    return make_response("Uplink message successfully stored", 201)
