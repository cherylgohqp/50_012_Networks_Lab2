from flask import Flask, request
import json
from flask_httpauth import HTTPBasicAuth
from functools import wraps

app = Flask(__name__)
auth = HTTPBasicAuth()
data_loaded = None

#user_data = {
 #   "staff" : "superman"
#}

with open('data.json') as data_file:
    data_loaded = json.load(data_file)

def numRooms():
        listOfRooms = []
        for key, value in data_loaded.items():
            listOfRooms.append(key)
        return(listOfRooms)

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

#def authenticate():
 #   message = {'message': "Authenticate."}
  #  resp = str(message)

   # resp.status_code = 401
    #resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    #return resp

#def requires_auth(f):
 #   @wraps(f)
  #  def decorated(*args, **kwargs):
   #     auth = request.authorization
    #    if not auth:
     #       return authenticate()

      #  elif not check_auth(auth.username, auth.password):
       #     return authenticate()
        #return f(*args, **kwargs)

    #return decorated

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
        if roomid in data_loaded:
            information = list(data_loaded[roomid])
            return "You are searching for room number: " + roomid + "\n" + "Location: " + information[0] + "\n" + "Capacity: " + information[1] + "\nType: " + information[2] + '\n'
        else:
            return "The room number you are searching for does not exist!!\n"
@app.route('/room/create', methods=['GET'])
#@requires_auth
def api_createroom():
    with open("create_room.html") as ui:
        return ui.read()

@app.route('/successful',methods=['POST'])
def api_successfulcreation():
    formData = request.form
    print(formData)

    roomID = formData.get('RoomID')
    floorLevel = formData.get('Level')
    capacity = formData.get('Capacity')
    roomType = formData.get('RoomType')

    information = []
    information.append('Level ' + floorLevel)
    information.append(capacity)
    information.append(roomType)

    data_loaded[roomID] =  information

    with open('data.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data_loaded,
                          indent=4,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(str_)
   # print (information)
   # print (floorLevel)
   # print(capacity)
   # print(roomType)
   # print (data_loaded)
    return "Room added to database!"

@app.route('/room/deletion', methods=['GET'])
#@requires_auth
def api_deleteroom():
    with open("delete_room.html") as ui:
        return ui.read()


@app.route('/deleted',methods=['DELETE','POST']) #added post here so this api can be called lel if not it will show method not available etc.
def api_successfuldeletion():
    formData = request.form
    print(formData)

    deleteID = formData.get('RoomID')

    for element in data_loaded:
        del element[deleteID]

    return "Room has been deleted from database!"

if __name__ == '__main__':
    app.run(port=5000) #run in cmd curl http://localhost:5000
