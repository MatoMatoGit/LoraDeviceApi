from flask import render_template
import connexion
import UplinkTtn
import sys

try:
    ca_file = sys.argv[1]
    priv_key_file = sys.argv[2]
    ssl_context = (ca_file, priv_key_file)
except:
    ssl_context = 'adhoc'

# Create the application instance
app = connexion.App(__name__, specification_dir='./config')

# Read the api.yml file to configure the endpoints
app.add_api('api.yml')

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
    UplinkTtn.SetOutputChannels({'raw': ['uplink.raw'], 'data': ['uplink.data']})
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=ssl_context)
