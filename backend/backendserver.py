# import compare_face_cloud
from flask import Flask, request, redirect, session, url_for, Response, json, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask.json import jsonify
from pymongo import MongoClient
from flask_cors import CORS
from google.cloud import datastore
from google.cloud import vision
from google.cloud import storage
import os
import facereglib
# import faceutils


with open('credentials.json', 'r') as f:
    creds = json.load(f)

mongostr = creds["mongostr"]
client = MongoClient(mongostr)

db = client["recoin"]


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def uploadtogcp(filename):
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('gc.json')

    # Make an authenticated API request
    ##buckets = list(storage_client.list_buckets())
    ##print(buckets)

    bucketname = "hackybucket"
    # filename = sys.argv[2]


    bucket = storage_client.get_bucket(bucketname)

    destination_blob_name = "current.jpg"
    source_file_name = filename

    blob = bucket.blob(destination_blob_name)
    blob.cache_control = "no-cache"

    blob.upload_from_filename(source_file_name)
    blob.make_public()
    blob.cache_control = "no-cache"

    print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


@app.route("/register", methods=["POST"])
def register():

    request_json = request.get_json()
    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    db =  client['recoin']

    col = db.users
    results = []
    maxid = 0
    for x in col.find():
        id = x["uid"]
        maxid +=1
    id = str(maxid+1)

    payload = {}
    if request_json:
        for x in col.find():
            if x['email'] == request_json['email']:
                retjson = {}

                # retjson['dish'] = userid
                retjson['mongoresult'] = "user already exists"
                # retjson['id'] = id

                return json.dumps(retjson)



        payload["uid"] = id
        payload["name"] = request_json['name']
        payload["email"] = request_json['email']
        payload["password"] = request_json['password']
        payload["username"] =  request_json['username']
        payload["coinsbal"] = 0

                
        result=col.insert_one(payload)

        retjson = {}

        # retjson['dish'] = userid
        retjson['result'] = "successfully added"
        retjson['id'] = id
        retjson['name'] = request_json['name']

        return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr




@app.route("/login", methods=["POST"])
def login():
    request_json = request.get_json()
    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    
    db = client['recoin']
    col = db.users
    results = []
    maxid = 0
    for x in col.find():
        id = x["uid"]
        maxid +=1
    id = str(maxid+1)
    retjson = {}
    
    payload = {}
    if request_json:
        for x in col.find():
            if x['email'] == request_json['email']:
                if x['password'] == request_json['password']:

                    

                    # retjson['dish'] = userid
                    retjson['result'] = "success"
                    retjson['id'] = x['id']
                    retjson['name'] = x['name']
 
                    
                    return json.dumps(retjson)



       
        retjson['result'] = "login fail"

        return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr




@app.route("/getcoins", methods=["POST"])
def getcoins():
    request_json = request.get_json()
    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    
    db = client['recoin']
    col = db.users
    results = []
    maxid = 0
    for x in col.find():
        id = x["uid"]
        maxid +=1
    id = str(maxid+1)
    retjson = {}
    
    payload = {}
    if request_json:
        for x in col.find():
            if x['email'] == request_json['email']:
                if x['password'] == request_json['password']:

                    

                    # retjson['dish'] = userid
                    retjson['result'] = "success"
                    retjson['id'] = x['id']
                    retjson['name'] = x['name']
                    retjson['coins'] = coinbal
                    
 
                    
                    return json.dumps(retjson)



       
        retjson['result'] = "login fail"

        return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr






@app.route("/file_upload", methods=["POST"])
def fileupload():

    if 'file' not in request.files:
          return "No file part"
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      return "No selected file"
    if file and allowed_file(file.filename):
        # UPLOAD_FOLDER = "./uploads"
        UPLOAD_FOLDER = "uploads"
  
        filename = secure_filename(file.filename)
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.save(filename)
        # uploadtogcp(os.path.join(UPLOAD_FOLDER, filename))
        uploadtogcp(os.path.join(filename))
        return 'https://storage.googleapis.com/hackybucket/current.jpg' 
    
    return 'file not uploaded successfully', 400








@app.route("/dummyJson", methods=['GET', 'POST'])
def dummyJson():

    print(request)

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()
 

    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["request"] = res 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp




@app.route("/dummy", methods=['GET', 'POST'])
def dummy():

    ##res = request.json

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

@app.route("/api", methods=["GET"])
def index():
    if request.method == "GET":
        return {"hello": "world"}
    else:
        return {"error": 400}


if __name__ == "__main__":
    # app.run(debug=True, host = 'localhost', port = 8003)
    app.run(debug=True, host = '45.79.199.42', port = 8003)
