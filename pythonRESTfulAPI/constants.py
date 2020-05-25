boats = "boats"
slips = "slips"

url = "https://dickinsj-assign-3.uc.r.appspot.com/"

#attribute list for each type
boatAtt = ["name", "type", "length"]
slipAtt = ["number"]


#error messages
badRequest = {"Error": "The request object is missing at least one of the required attributes"}
badSlipRequest = {"Error": "The request object is missing the required number"}
notFound = {"Error": "No boat with this boat_id exists"}
slipNotFound = {"Error": "No slip with this slip_id exists"}
notFoundBS = {"Error": "The specified boat and/or slip don\u2019t exist"}
notEmpty = {"Error": "The slip is not empty"}
boatNotHere = {"Error": "No boat with this boat_id is at the slip with this slip_id"}


#checks to see if all attributes are in request
#false if one is missing, true if all are within request
def invalidBoatRequest(request):
    for att in boatAtt:
        if att not in request:
            return True
    return False

def invalidSlipRequest(request):
	for att in slipAtt:
		if att not in request:
			return True
	return False

#adds id and self web URL to object
def addTags(results):
    for e in results:
        e["id"] = str(e.key.id)
        e["self"] = url + "boats/" + str(e.key.id)