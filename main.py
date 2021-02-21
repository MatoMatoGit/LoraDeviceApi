from flask import render_template
import connexion
from Uplink import Uplink
from Uplink import UplinkTtn
from Uplink import UplinkKpn
import sys
import json

cfg = open(sys.argv[1], 'r')

Config = json.loads(cfg.read())

cfg.close()

if Config["tls"] is True:
    try:
        ssl_context = (Config["ca_path"], Config["priv_key_path"])
    except:
        ssl_context = 'adhoc'

# Create the application instance
app = connexion.App(__name__, specification_dir=Config["api_spec_dir"])

# Add APIs
for api in Config["apis"]:
    print("Adding API: {}".format(api))
    app.add_api(api)


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    UplinkInstance = Uplink.Uplink({'raw': Config["channels"]["raw"], 'data': Config["channels"]["data"]})
    UplinkTtn.SetUplink(UplinkInstance)
    UplinkKpn.SetUplink(UplinkInstance)
    if Config["tls"] is True:
        app.run(host='0.0.0.0', port=Config["port"], debug=True, ssl_context=ssl_context)
    else:
        app.run(host='0.0.0.0', port=Config["port"], debug=True)
