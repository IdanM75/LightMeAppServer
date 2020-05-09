from __future__ import division, unicode_literals
from flask import Flask, jsonify, request
import json
import math
import datetime

google_accounts_data = {'111497711458820230553': {"lat": 32.0853, "lng": 34.7818, "has_lighter": True, 'time': datetime.datetime.now()},
                        '111497711458820230554': {"lat": 32.0843, "lng": 34.7828, "has_lighter": True, 'time': datetime.datetime.now()},
                        '111497711458820230558': {"lat": 32.0848, "lng": 34.7823, "has_lighter": False, 'time': datetime.datetime.now()},
                        '111497711458820230559': {"lat": 32.0851, "lng": 34.7826, "has_lighter": True, 'time': datetime.datetime.now()},
                        '103384306394092203955': {"lat": 32.0953, "lng": 34.7718, "has_lighter": True, 'time': datetime.datetime.now()},
                        '111497711458820230556': {"lat": 32.1853, "lng": 34.6818, "has_lighter": True, 'time': datetime.datetime.now()},
                        '111497711458820230557': {"lat": 32.0858, "lng": 34.7813, "has_lighter": True, 'time': datetime.datetime.now()}
                        }

profiles_data = {}
users_data = {
    '111497711458820230553': {"google_account_name": "aaa", 'phone_num': '972525787016', 'is_run_in_background': False},
    '111497711458820230554': {"google_account_name": "bbb", 'phone_num': '972525787016', 'is_run_in_background': False},
    '111497711458820230558': {"google_account_name": "ccc", 'phone_num': '972525787016', 'is_run_in_background': False},
    '111497711458820230559': {"google_account_name": "ddd", 'phone_num': '972525787016', 'is_run_in_background': False},
    '103384306394092203955': {"google_account_name": "eee", 'phone_num': '972525787016', 'is_run_in_background': False},
    '111497711458820230556': {"google_account_name": "fff", 'phone_num': '972525787016', 'is_run_in_background': False},
    '111497711458820230557': {"google_account_name": "ggg", 'phone_num': '972525787016', 'is_run_in_background': False}
}


def distance_between_locations(lat1, lon1, lat2, lon2):
    # d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))
    # distance_km = 6371 * d
    # return distance_km

    R = 6373.0

    lat1_tr = math.radians(lat1)
    lon1_tr = math.radians(lon1)
    lat2_tr = math.radians(lat2)
    lon2_tr = math.radians(lon2)

    dlon = lon2_tr - lon1_tr
    dlat = lat2_tr - lat1_tr

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_tr) * math.cos(lat2_tr) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance * 1000


app = Flask("Light Me App")


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/get_lighters_latlng")
def get_lighters_latlng():
    response = {"lighters_latlng": []}
    my_google_account_id = request.args.get('googleAccountId')
    if my_google_account_id not in google_accounts_data:
        return jsonify(response)

    my_user_lat = google_accounts_data[my_google_account_id]['lat']
    my_user_lng = google_accounts_data[my_google_account_id]['lng']

    for google_account_id in google_accounts_data:
        user_lat = google_accounts_data[google_account_id]['lat']
        user_lng = google_accounts_data[google_account_id]['lng']
        time = google_accounts_data[google_account_id]['time']
        time_string = (str(time.ctime().split(' ')[4]))
        user_has_lighter = google_accounts_data[google_account_id]['has_lighter']
        distance_between = distance_between_locations(my_user_lat, my_user_lng, user_lat, user_lng)
        if distance_between <= 400 and google_account_id != my_google_account_id and user_has_lighter:
            if google_account_id not in users_data:
                response['lighters_latlng'].append({"user_id": google_account_id, "lat": user_lat, "lng": user_lng,
                                                    'name': 'error', 'phone': 'error', 'time': time_string})
            else:
                response['lighters_latlng'].append({"user_id": google_account_id, "lat": user_lat, "lng": user_lng,
                                                    'name': users_data[google_account_id]['google_account_name'],
                                                    'phone': users_data[google_account_id]['phone_num'],
                                                    'time': time_string})

    return jsonify(response)


@app.route("/my_location", methods=["POST"])
def my_location():
    request_json = request.get_json()
    google_accounts_data[request_json['googleAccountId']] = {'lat': request_json['lat'],
                                                             'lng': request_json['lng'],
                                                             'has_lighter': request_json['hasLighter'],
                                                             'time': datetime.datetime.now()}
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# @app.route("/user_data", methods=["POST"])
# def user_data():
#     request_json = request.get_json()
#     google_account_id = request_json['googleAccountId']
#     email = request_json['email']
#     name = request_json['name']
#     photo = request_json['photo']
#     users_data[google_account_id] = {'email': email,
#                                      'name': name,
#                                      'photo': photo}
#     if google_account_id in users_phones:
#         return jsonify({"phone": users_phones[google_account_id]})
#     else:
#         return jsonify({"phone": "-1"})


@app.route("/initialize_profile", methods=["POST"])
def initialize_profile():
    request_json = request.get_json()
    account_id = request_json['googleAccountId']
    is_run_in_background = request_json['isRunInBackground']
    phone_num = request_json['phoneNum']
    google_account_name = request_json['googleAccountName']
    if account_id not in users_data:
        users_data[account_id] = {}
    users_data[account_id]['is_run_in_background'] = is_run_in_background
    users_data[account_id]['phone_num'] = phone_num
    users_data[account_id]['google_account_name'] = google_account_name
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# ToDO last time that the user connected


# @app.route("/get_user_data")
# def get_user_data():
#     google_account_id = request.args.get('googleAccountId')
#     if google_account_id not in users_data:
#         return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
#     return jsonify(users_data[google_account_id])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
