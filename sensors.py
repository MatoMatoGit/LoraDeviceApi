from flask import make_response, abort
import json

def get_all():
    return

def get_types(dev_id):
    response = { 'sensor_types': ['temp', 'moist'] }

    return make_response(json.dumps(response), 200)

def get_values(dev_id, sensor_type):
    return