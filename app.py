from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image
import csv
import pandas as pd
from PIL import Image
import base64
import io
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from IPython.display import HTML


app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')

app.config.from_pyfile('config.py')
account = app.config['ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container = app.config['CONTAINER'] # Container name
allowed_ext = app.config['ALLOWED_EXTENSIONS'] # List of accepted extensions

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

@app.route('/', methods = ["GET","POST"])
def hello_world():
    photo_name = 'm-1.jpg'
    image = Image.open(photo_name)
    data=io.BytesIO()
    image.save(data,"JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("Name.html",photo_name=encoded_img_data.decode('UTF-8'))

@app.route('/user', methods = ["POST"])
def user():
    df = pd.read_csv("data-1.csv",on_bad_lines='skip')
    name = request.form["name"]
    for i in df["name"]:
        if i !=name:
            next
        elif i ==name:
            pdict = zip(df.name,df.picture)
            pdict=dict(pdict)
            state = df[df["name"]==i]["class"].values[0]
            print("{}'s class is {}".format(i,state)) 
            photo_name = pdict[i]
            image = Image.open(photo_name)
            data=io.BytesIO()
            image.save(data,"JPEG")
            encoded_img_data = base64.b64encode(data.getvalue())
            return render_template('user.html',user=name,state=state,photo_name=encoded_img_data.decode('utf-8')) 
        return render_template('not_found.html')
 
if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8000, debug = True)
