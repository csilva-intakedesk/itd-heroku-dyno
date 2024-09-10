"""
This module is the main entry point to check if a given geolocation coordinates
and state are part of a given PWS shape.
"""

import json
from flask import Flask, request
from . import bbox_text

app = Flask(__name__)

# This is the main entry point for the lambda function
@app.route('/', methods=['POST'])
def handler():
    """
    Main Lambda handler function.
    """

    event = request.get_json()

    # Process event to extract necessary data
    location_data = process_event(event)

    if not location_data:
        return generate_response(404,
               'Missing required parameters for returning the PWS.',
               event, True)

    # Perform a search operation based on lat, lng, and state
    lat, lng, state = location_data

    if not lat or not lng:
        return generate_response(404,
               'Missing required parameters for returning the PWS. Geocoordinates missing.',
               event, True)

    if not state:
        return generate_response(404,
               'Missing required parameters for returning the PWS. State missing.',
               event, True)

    search_result = search_pws(lat, lng, state)

    if not search_result:
        return generate_response(404,
               'Unable to find a location for the given Geocoordinates and state.',
               event, True)

    # Return structured response
    return generate_response(200, search_result, event, False)

def process_event(event):
    """
    Extract lat, lng, and state from the event.
    """

    try:
        # body = json.loads(event['body'])
        lat = event['lat']
        lng = event['lng']
        state = event['state']

        return lat, lng, state
    except KeyError:
        return None

def search_pws(lat, lng, state):
    """
    Perform a search operation based on location and state.
    Replace this with actual search logic.
    # Example usage
    # shapefile_path = "EPA_CWS_V1/EPA_CWS_V1.shp"
    # point = (-86.588136, 36.215407) # Example longitude and latitude 
    # for Atlanta, GA
    # point = (-86.577095, 36.218051) # 36.218051, -86.577095 NO
    # point = (-86.588136, 36.215407) # 36.215407, -86.588136 YES
    # state = "TN"
    # if is_point_in_shapefile(shapefile_path, point, state) == False:
    #    print("The point {} is NOT within the shapefile 
    # boundaries in state {}.".format(point, state))
    # shapefile_path = 'https://itd-epa.s3.amazonaws.com/EPA_CWS_V1/EPA_CWS_V1.shp'
    """

    shapefile_path = 'EPA_CWS_V1/EPA_CWS_V1.shp'
    point = (lng, lat)

    location = bbox_text.is_point_in_shapefile(shapefile_path, point, state)

    if not location:
        return False

    return location

def generate_response(status_code, message, event, error):
    """
    Generate a structured HTTP response.
    """

    if error:
        return {
            'statusCode': status_code,
            'body': json.dumps({
                'message': message,
                'event': event,
                'success': False,
                'data': []
            })
        }

    return {
        'statusCode': status_code,
        'body': {
            'data': [message],
            'success': True,
            'message': 'Success'
        }
    }
