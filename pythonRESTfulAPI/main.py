from google.cloud import datastore
from flask import Flask, request
import json
import constants
import os

app = Flask(__name__)
client = datastore.Client()
if os.getenv('PORT') == None:
    PORT = 8081
else:
    PORT = os.getenv('PORT')


#*************Main Page*************
@app.route('/')
def index():
    return "Please navigate to /boats to use this API"\



#*************/boats*************
#
#   Post:   create a new boat
#   Get:    returns all boats
#
#********************************
@app.route('/boats', methods=['POST', 'GET'])
def boats_get_post():

    if request.method == 'POST':
        content = request.get_json()
        if constants.invalidBoatRequest(content):
            return (json.dumps(constants.badRequest), 400)
        new_boat = datastore.entity.Entity(key=client.key(constants.boats))
        new_boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
        client.put(new_boat)
        new_boat.update({"id": str(new_boat.key.id), "self": constants.url + "/boats/" + str(new_boat.key.id)})
        return (json.dumps(new_boat), 201)

    elif request.method == "GET":
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        constants.addTags(results)
        return json.dumps(results)

    else:
        return 'Method not recognized, please use either GET or POST'


#*************/boats/<id>*************
#
#   Patch:      patches boat
#   Delete:     deletes this boat
#   Get:        returns this boat
#
#*************************************
@app.route('/boats/<id>', methods=['PATCH', 'DELETE', 'GET'])
def boat_get_put_delete(id):

    boat_key = client.key(constants.boats, int(id))
    boat = client.get(key=boat_key)
    if boat == None:
        return (json.dumps(constants.notFound), 404)

    if request.method == 'PATCH':
        content = request.get_json()
        if constants.invalidBoatRequest(content):
            return (json.dumps(constants.badRequest), 400)
        boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
        client.put(boat)
        boat.update({"id": id, "self": constants.url + "/boats/" + id})
        return (json.dumps(boat), 200)

    elif request.method == 'DELETE':
        #check to find if this boat is in a slip
        #if it is, set slip's 'current_boat' to null first
        query = client.query(kind=constants.slips)
        query.add_filter('current_boat', '=', id)
        results = list(query.fetch())
        if results:
            slip_key = client.key(constants.slips, results[0].key.id)
            slip = client.get(key=slip_key)
            slip.update({"current_boat": None})
            client.put(slip)
        client.delete(boat_key)
        return ('',204)

    elif request.method == 'GET':
        boat.update({"id": id, "self": constants.url + "/boats/" + id})
        return json.dumps(boat)

    else:
        return 'Method not recognized, please use PATCH, DELETE, or GET'




#*************/slips**********************************************
#
#   Post:   create a new slip
#   Get:    returns all slips
#
#   Note: New slips start with null in their 'current_boat' field
#*****************************************************************
@app.route('/slips', methods=['POST', 'GET'])
def slips_get_post():

    if request.method == 'POST':
        content = request.get_json()
        if constants.invalidSlipRequest(content):
            return (json.dumps(constants.badSlipRequest), 400)
        new_slip = datastore.entity.Entity(key=client.key(constants.slips))
        new_slip.update({"number": content["number"], "current_boat": None})
        client.put(new_slip)
        new_slip.update({"id": str(new_slip.key.id), "self": constants.url + "/slips/" + str(new_slip.key.id)})
        return (json.dumps(new_slip), 201)

    elif request.method == "GET":
        query = client.query(kind=constants.slips)
        results = list(query.fetch())
        constants.addTags(results)
        return json.dumps(results)

    else:
        return 'Method not recognized, please use either GET or POST'


#*************/slips/<id>*****************************************
#
#   Delete:     deletes this slip
#   Get:        returns this slip
#
#*****************************************************************
@app.route('/slips/<id>', methods=['DELETE', 'GET'])
def slip_get_delete(id):

    slip_key = client.key(constants.slips, int(id))
    slip = client.get(key=slip_key)
    if slip == None:
        return (json.dumps(constants.slipNotFound), 404)

    if request.method == 'DELETE':
        client.delete(slip_key)
        return ('',204)

    elif request.method == 'GET':
        slip.update({"id": id, "self": constants.url + "/slips/" + id})
        return json.dumps(slip)

    else:
        return 'Method not recognized, please use DELETE, or GET'





#*************/slips/<slip id>/<boat id>**************************
#
#   Put:    Puts this boat into this slip's 'current_boat' field
#   Delete: Removes boat from slip, resets 'current_boat' to null
#
#*****************************************************************
@app.route('/slips/<sid>/<bid>', methods=['PUT', 'DELETE'])
def slip_boat_put_delete(sid, bid):
    
    #get slip
    slip_key = client.key(constants.slips, int(sid))
    slip = client.get(key=slip_key)
    #get boat
    boat_key = client.key(constants.boats, int(bid))
    boat = client.get(key=boat_key)


    if request.method == 'PUT':

        #check if either is null
        if slip == None or boat == None:
            return (json.dumps(constants.notFoundBS), 404)    

        #ensure slip is open
        if slip["current_boat"] != None:
            return (json.dumps(constants.notEmpty), 403)

        slip.update({"current_boat": bid})
        client.put(slip)
        return ('', 204)

    elif request.method == 'DELETE':
        #ensure slip is not null
        if slip == None:
            return (json.dumps(constants.boatNotHere), 404)
        #ensure this boat is in this slip
        if slip["current_boat"] != bid:
            return (json.dumps(constants.boatNotHere), 404)
    
        slip.update({"current_boat": None})
        client.put(slip)
        return ('', 204)

    else:
        return 'Method not recognized, please use PUT or DELETE'
1


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT, debug=True)
