import base64
import cbor


class Decoder:

    def __init__(self):

        return

    def Base64ToAscii(self, input):
        return base64.b64decode(input.encode('ascii'))

    def CborToJson(self, input):
        return cbor.loads(input)

    def Decode(self, input):
        return self.CborToJson(self.Base64ToAscii(input))
