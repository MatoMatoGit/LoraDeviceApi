import base64
import cbor


class Decoder:

    def __init__(self):

        return

    def Base64ToAscii(self, input):
        return base64.b64decode(input.encode('ascii'))

    def ParseCbor(self, input):
        return cbor.loads(input)

