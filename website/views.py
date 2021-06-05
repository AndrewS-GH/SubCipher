from flask import Blueprint, render_template, request, flash, jsonify, make_response
from . import cipher

views = Blueprint('views', __name__)

cipherObj = None  # object for all methods relating to cipher

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("index.html")

@views.route('/sendCT', methods = ['GET', 'POST'])
def getCT():
    if request.method == "POST":
        cipherObj = cipher.Cipher(request.get_json())
        keyVals = cipherObj.getKey()
        print(keyVals)
        results = {
            "key": cipherObj.getKey(),
            "orig": cipherObj.getOrig()
        }
        return jsonify(results)