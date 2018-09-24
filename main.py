#Completed by: Kenneth Chua and Cheryl Goh

from flask import Flask, request, jsonify, abort
import json
from flask_httpauth import HTTPBasicAuth
from functools import wraps
import re
app = Flask(__name__)
auth = HTTPBasicAuth()
data_loaded = None

#user_data = {
 #   "staff" : "superman"
#}

def numRooms():
	listOfRooms = []
	with open('data.json') as data_file:
		# import pdb;pdb.set_trace()
		data_loaded = json.load(data_file)
	for key, value in data_loaded.items():
		listOfRooms.append(key)
	print(listOfRooms)
	return(listOfRooms)

def check_auth(username, password):
	return username == 'admin' and password == 'secret'

def authenticate():
	message = {'message': "Authenticate."}
	resp = jsonify(message)

	resp.status_code = 401
	resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
	
	return resp

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth: 
			return authenticate()

		elif not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)

	return decorated

@app.route('/')
def roomInfoService():
	#if request.authorization and request.authorization.username == "staff" and request.authorization.password == 'superman':

	return 'This is SUTD Room Information Services! \n'

@app.route('/room', methods=['GET']) #produces a list of rooms available
def api_getrooms():
	if request.method == 'GET':
		return "List of rooms available:\n" + str(numRooms()) + '\n'

@app.route('/room/<roomid>', methods=['GET']) #gets the room information
def api_room(roomid):
	if request.method == 'GET':
		with open('data.json') as data_file:
			# import pdb;pdb.set_trace()
			data_loaded = json.load(data_file)
		if roomid in data_loaded:
			information = list(data_loaded[roomid])
			building = roomid[0]
			return "You are searching for room number: " + roomid + "\n" + "Building: " + building + "\n" + "Level: " + information[0] + "\n" + "Capacity: " + information[1] + "\nType: " + information[2] + '\n'
		else:
			return "The room number you are searching for does not exist!!\n"
@app.route('/room/create', methods=['GET'])
@requires_auth
def api_createroom():
	with open("create_room.html") as ui:
		return ui.read()

@app.route('/successful',methods=['POST'])
def api_successfulcreation():
	with open('data.json') as data_file:
		# import pdb;pdb.set_trace()
		data_loaded = json.load(data_file)
	formData = request.form
	print(formData)
	information = []
	merge_loaded = data_loaded

	if formData.get('selectFiles') is not '':
		json_uploadfile = request.files['selectFiles']
		json_loaded = json.load(json_uploadfile)
		merge_loaded = {**data_loaded,**json_loaded}

	roomID = formData.get('RoomID')
	floorLevel = formData.get('Level')
	capacity = formData.get('Capacity')
	roomType = formData.get('RoomType')



	if roomID != "" or floorLevel != "" or capacity != "" or roomType != "":
		information.append('Level' + floorLevel)
		information.append(capacity)
		information.append(roomType)

		data_loaded[roomID] =  information

	with open('data.json', 'w', encoding='utf8') as outfile:
		str_ = json.dumps(merge_loaded,
						  indent=4,
						  separators=(',', ': '), ensure_ascii=False)
		outfile.write(str_)
   # print (information)
   # print (floorLevel)
   # print(capacity)
   # print(roomType)
   # print (data_loaded)
	if formData.get('RoomID') is '' and formData.get('selectFiles') is '':
		return "You have not added any information!"
			
	return "Room added to database!"

@app.route('/room/deletion', methods=['GET'])
@requires_auth
def api_deleteroom():
	with open("delete_room.html") as ui:
		return ui.read()


@app.route('/deleted',methods=['DELETE','POST'])
def api_successfuldeletion():
	with open('data.json') as data_file:
		# import pdb;pdb.set_trace()
		data_loaded = json.load(data_file)
	formData = request.form
	print(formData)

	deleteID = formData.get('DeleteID')
	print ("deleteID ", deleteID)
	print ("data_loaded ", data_loaded)


	if deleteID not in data_loaded:
		return "The room you want to delete does not exist!\n"
	else:
		del data_loaded[deleteID]
		with open('data.json', 'w', encoding='utf8') as outfile:
			str_ = json.dumps(data_loaded,
							  indent=4,
							  separators=(',', ': '), ensure_ascii=False)
			outfile.write(str_)
		return "Room has been deleted from database!\n"

if __name__ == '__main__':
	app.run(port=5000) #run in cmd curl http://localhost:5000
