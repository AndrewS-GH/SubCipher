from flask import Blueprint, render_template, request, flash, jsonify, make_response
from . import cipher

views = Blueprint('views', __name__)

cipherObj = None  # object for all methods relating to cipher

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views.route('/sendCT', methods = ['GET', 'POST'])
def sendCT():
    if request.method == "POST":
        global cipherObj
        cipherObj = cipher.Cipher(request.get_json())
        keyVals = cipherObj.getKey()
        results = {
            "key": cipherObj.getKey(),
            "orig": cipherObj.getOrig()
        }
        return jsonify(results)

@views.route('/modKey', methods = ['GET', 'POST'])
def modKey():
    if request.method == "POST":
        result = request.get_json()
        firstCol = result["first"].split()
        secondCol = result["second"].split()
        keyDict = {}
        for i in range(len(firstCol)):
            keyDict[firstCol[i]] = secondCol[i]
        cipherObj.modifyKey(keyDict)        

    return jsonify(cipherObj.getCipher())

@views.route('/swapByFreq', methods = ['POST', 'GET'])
def swapByFreq():
    if request.method == "POST":
        cipherObj.swapByFreq()
        results = {
            "key": cipherObj.getKey(),
            "plaintext": cipherObj.getCipher()
        }
        return jsonify(results)

@views.route('/genSS', methods = ['POST', 'GET'])
def genSS():
    if request.method == "POST":
        result=request.get_json()
        dictList = []
        for key, value in cipherObj.getCommSS(int(result)).items():
            temp = [key,value]
            dictList.append(temp)

        return jsonify(dictList)

@views.route('/genWord', methods = ['POST', 'GET'])
def genWord():
    if request.method == "POST":
        result=request.get_json()
        dictList = []
        for key, value in cipherObj.getCommWords(int(result)).items():
            temp = [key,value]
            dictList.append(temp)

        return jsonify(dictList)

@views.route('/dupSS', methods = ['POST', 'GET'])
def dupSS():
    if request.method == "POST":
        dictList = []
        for key, value in cipherObj.getDupSS().items():
            temp = [key,value]
            dictList.append(temp)

        return jsonify(dictList)

@views.route('/resetCipher', methods = ['POST', 'GET'])
def resetCipher():
    if request.method == "POST":
        cipherObj.reset()
        return ""
