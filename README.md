# LoRa Network Gateway service

The LoraNetworkGateway-service is responsible for receiving data 
from and sending data to LoRa devices which are connected to a LoRaWAN network. 
Currently two LoRaWAN networks are supported:
- The Things Network (TTN)
- KPN LoRa network (KPN)

The service interfaces with other services using JSON message over Kafka.

## Configuration

**todo: insert config table**

## Output channels

This service has the following output channels:
- raw: The raw received uplink message is published. The raw uplink message will look
different for each of the supported networks.
- data: A JSON message with a consistent format which contains the message payload.
Format:

**todo: insert JSON format**

## API

The LoraNetworkGateway API is implemented using Connexion and Flask. Data is transferred in JSON over HTTP(S).
Base-endpoint: _/lora-network-gateway/v1/_

The API has interactive documentation powered by Swagger. The documentation can be found on the following end-point:
_/lora-network-gateway/ui_


### Uplink

Data is received from the LoRaWAN network on the Uplink end-points using the POST method.
- TTN: _uplink/ttn_
- KPN: _uplink/kpn_



