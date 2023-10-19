import logging
import os
import signal
import sys
import ipaddress

from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
import json
from SBKodiak.KodiakControl import KodiakControlClass, KodiakWrapper
from SBKodiak.KodiakMDNsLocate import find_kodiak_ip_addresses
from SBFlask.tests.frigged_server_responses import *

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app, resources={r"/kodiak/port/discover": {"origins": "http://192.168.1.160"},
#                      r"/kodiak/locate": {"origins": "http://192.168.1.160"},
#                      r"/kodiak/port": {"origins": "http://192.168.1.160"},
#                      r"/kodiak/remove": {"origins": "http://192.168.1.160"},
#                      r"/kodiak/start": {"origins": "http://192.168.1.160"},
#                      r"/kodiak/stop": {"origins": "http://192.168.1.160"},
#                      r"/kodiak/status": {"origins": "http://192.168.1.160"}})

stop_kodiak = True

# Kodiak Controller object
KodiakController = KodiakControlClass()

# Fake the responses
frigg_responses = False
frigg_responses_port_counter = 0


def check_valid_ip(ip_addr):
    try:
        ip = ipaddress.ip_address(ip_addr)
        return True
    except ValueError:
        return False
    except:
        return False


@app.route(f"/kodiak/port/discover", methods=['POST'])
def kodiak_endpoint_discover():
    """
    Discover endpoint.

    The function will first try to get the login credentials.

    This endpoint will start the discovery of the Kodiak Module against the SB ports
    After posting to the endpoint, the client should then send a 'get' request to the /kodiak/port to discover the port.

    :return: JSON - With an appropriate success / error message.
    """
    global KodiakController
    global frigg_responses

    response = {}

    if request.method == 'POST':
        if not request.content_type:
            response['Error'] = 'Request not of type JSON'
            return json.dumps(response, indent=4)
        if 'application/json' not in request.content_type:
            response['Error'] = 'Request not of type JSON'
            return json.dumps(response, indent=4)

        data = request.get_json()
        if not isinstance(data, dict):
            response['Error'] = 'Request not of correct JSON format'
            return json.dumps(response, indent=4)

        if 'ipaddress' not in data:
            response['Error'] = 'Missing IP address'
        elif not check_valid_ip(data['ipaddress']):
            response['Error'] = 'Badly formatted IP address'
        elif 'key' not in data:
            response['Error'] = "Missing API key"
        else:
            ipaddress = data['ipaddress']
            key = data['key']

            # If we're faking it, just do to here
            if frigg_responses:
                response['Success'] = 'Started auto discovery'
                return json.dumps(response, indent=4)


            # Create a wrapper and attempt to start the auto locate
            kw = KodiakWrapper(ipaddress, None, None, key)
            started = KodiakController.start_auto_locate_port(kw)

            # If there's an error starting the discovery, add the error message
            if not started:
                response['Error'] = 'Failed to start Kodiak capture!'
            else:
                response['Success'] = 'Started auto discovery'

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/locate", methods=['GET'])
def kodiak_endpoint_locate():
    """
    Get endpoint for scanning MDNs for Kodiak Ipaddresses.

    This function will attempt to get the port the Kodiak is attached to

    :return: JSON - With an appropriate success / error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    if request.method == 'GET':
        try:
            if frigg_responses:
                response['Success'] = ['192.168.1.2', '192.168.1.3']
                return json.dumps(response, indent=4)

            # call to MDNS scan function which will return a list of discovered IPAddresses
            ip_address_list = find_kodiak_ip_addresses()
            logging.debug(f"List of found ip's : {ip_address_list}")
            response['Success'] = str(ip_address_list)
        except Exception as err:
            response['Error'] = "Error whilst starting MDNS discovery!"

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/port", methods=['GET'])
def kodiak_endpoint_port():
    """
    Get port endpoint.

    This function will attempt to get the port the Kodiak is attached to

    :return: JSON - With an appropriate success / error message.
    """
    global KodiakController
    global frigg_responses
    global frigg_responses_port_counter
    response = {}

    if request.method == 'GET':
        if not request.args:
            response['Error'] = 'Request missing args'
            return json.dumps(response, indent=4)

        if 'ipaddress' not in request.args:
            response['Error'] = 'Request missing ipaddress argument'
            return json.dumps(response, indent=4)

        ipaddress = request.args.get('ipaddress')

        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        if frigg_responses:
            # If we're faking the responses, make sure we only do 1 port at a time, so we can test other ports work too
            response['Success'] = '0' + str(frigg_responses_port_counter)
            frigg_responses_port_counter += 1
            if frigg_responses_port_counter > 4:
                frigg_responses_port_counter = 0

            return json.dumps(response, indent=4)

        # Get the items from the database
        query_response = KodiakController.db.get_kodiak_db(ipaddress)

        # if the response is missing then add an appropriate error message
        if not query_response:
            response['Error'] = "Missing Kodiak credentials, have you logged in?"

        else:
            # Create a wrapper and attempt to start the auto locate
            port_response = query_response[7]

            if port_response:
                response['Success'] = port_response
            else:
                # If there wasn't a return from the locate_kodiak_port function then no port was found
                response['Error'] = "Could not find port containing Kodiak Module!"

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/status", methods=['GET'])
def kodiak_endpoint_get_status():
    """
    Get kodiak status for a given IP address.

    This function will attempt to get the status of the kodiak from the supplied IP

    :return: JSON - With an appropriate success / error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    if request.method == 'GET':

        if not request.args:
            response['Error'] = 'Request missing args'
            return json.dumps(response, indent=4)

        if 'ipaddress' not in request.args:
            response['Error'] = 'Request missing ipaddress argument'
            return json.dumps(response, indent=4)

        ipaddress = request.args.get('ipaddress')

        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're just testing as the rest of this function will be tested elsewhere
        if frigg_responses:
            response['Success'] = status_response_good
            return json.dumps(response, indent=4)

        # Get the items from the database
        my_response = KodiakController.db.get_kodiak_db(ipaddress)
        kw = KodiakWrapper(my_response[0], None, None, my_response[3])
        query_response = KodiakController.get_module_status(kw)

        response["Success"] = query_response

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/remove", methods=['POST'])
def kodiak_endpoint_remove():
    """
    Function to remove kodiak from the underlying database

    :return: JSON - With an appropriate success / error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    # Checking if request is of type 'POST'
    if request.method == 'POST':

        if not request.args:
            response['Error'] = 'Request missing args'
            return json.dumps(response, indent=4)

        if 'ipaddress' not in request.args:
            response['Error'] = 'Request missing ipaddress argument'
            return json.dumps(response, indent=4)

        ipaddress = request.args.get('ipaddress')

        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        if frigg_responses:
            response['Success'] = 'Removed Successfully'
            return json.dumps(response, indent=4)

        response['Success'] = 'Removed Successfully'

        return json.dumps(response, indent=4)

# @app.route(f"/server/shutdown")
# def server_endpoint_shutdown():
#     """
#     Shutdown server endpoint
#
#     Will shut down this running flask server.
#
#     :return: JSON - stating server is about to be shutdown
#     """
#
#     def shutdown_server():
#         app.
#
#     try:
#         response = {'Success': 'Shutting down server'}
#         return json.dumps(response, indent=4)
#     finally:
#         shutdown_server()


@app.route(f"/kodiak/start", methods=['POST'])
def kodiak_endpoint_start():
    global KodiakController

    response = {}

    # Checking if request is of type 'POST'
    if request.method == 'POST':

        # Checking the request is JSON
        if not request.content_type:
            response['Error'] = 'Request not of type JSON'
            return json.dumps(response, indent=4)

        # Checking the JSON is actual json.
        if 'application/json' not in request.content_type:
            response['Error'] = 'Request not of type JSON'
            return json.dumps(response, indent=4)

        data = request.get_json()

        if not isinstance(data, dict):
            response['Error'] = 'Request not of correct JSON format'
            return json.dumps(response, indent=4)

        if 'ipaddress' not in data:
            response['Error'] = 'Missing IP address'
            return json.dumps(response, indent=4)

        if 'key' not in data:
            response['Error'] = "Missing API key"
            return json.dumps(response, indent=4)

        ipaddress = data['ipaddress']

        # Checking the IP address is of the valid format
        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're doing testing as rest of function can be tested independently elsewhere
        if frigg_responses:
            response['Success'] = 'Successfully started kodiak stream'
            return json.dumps(response, indent=4)

        # Get the items from the database
        query_response = KodiakController.db.get_kodiak_db(ipaddress)

        # if the response is missing then add an appropriate error message
        if not query_response:
            response['Error'] = "Could not locate this IP address, is this definitely connected?"

        else:
            # Create a wrapper and attempt to start the auto locate
            kw = KodiakWrapper(query_response[0], query_response[1], query_response[2], query_response[3])

            # Need to lock the device before we can start streaming to it.
            KodiakController.lock(kw, 'SB_LOCK')
            started = KodiakController.start(kw, trigger=False)

            if started:
                response['Success'] = 'Successfully started kodiak stream'
            else:
                response['Error'] = started


        # else:
        #     response['Error'] = 'Missing IP address argument from post request'

        return json.dumps(response, indent=4)



@app.route(f"/kodiak/stop", methods=['POST'])
def kodiak_endpoint_stop():
    global KodiakController

    response = {}

    # Checking if request is of type 'POST'
    if request.method == 'POST':
        # Checking the request is JSON
        if not request.content_type:
            response['Error'] = 'Request not of type JSON'
            return json.dumps(response, indent=4)

        # Checking the JSON is actual json.
        if 'application/json' not in request.content_type:
            response['Error'] = 'Request not of type JSON'
            return json.dumps(response, indent=4)

        data = request.get_json()

        if not isinstance(data, dict):
            response['Error'] = 'Request not of correct JSON format'
            return json.dumps(response, indent=4)

        if 'ipaddress' not in data:
            response['Error'] = 'Missing IP address'
            return json.dumps(response, indent=4)

        if 'key' not in data:
            response['Error'] = "Missing API key"
            return json.dumps(response, indent=4)

        ipaddress = data['ipaddress']

        # Checking the IP address is of the valid format
        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're doing testing as rest of function can be tested independently elsewhere
        if frigg_responses:
            response['Success'] = 'Successfully stopped kodiak stream'
            return json.dumps(response, indent=4)

        # Get the items from the database
        query_response = KodiakController.db.get_kodiak_db(ipaddress)

        # if the response is missing then add an appropriate error message
        if not query_response:
            response['Error'] = "Could not locate this IP address, is this definitely connected?"

        else:
            # Create a wrapper and attempt to start the auto locate
            kw = KodiakWrapper(query_response[0], query_response[1], query_response[2], query_response[3])

            # call function to stop device from streaming
            started = KodiakController.stop(kw)

            if started:
                response['Success'] = 'Successfully stopped kodiak stream'
            else:
                response['Error'] = started

        return json.dumps(response, indent=4)


def shutdown_application():
    """
    This function is a standalone way to kill the application

    It is called both via the endpoint @ :4201/shutdown or via the cli 'python -m SBFlask.run shutdown'

    :return: N/A
    """
    os.kill(os.getpid(), signal.SIGINT)


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """
    This endpoint is used to terminate / kill the running flask server process.

    There will be no response to the server as a result of this.

    :return: N/A
    """
    shutdown_application()


def create_app():
    app.run(port=4201, host='0.0.0.0')


def set_frigg_responses(frigg):
    global frigg_responses
    frigg_responses = frigg


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) > 0:
        main_arg = args[0]
        if 'test' in main_arg:
            set_frigg_responses(True)

    create_app()
