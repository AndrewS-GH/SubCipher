from flask import Blueprint, render_template, request, flash, jsonify, make_response
from .cipher import Cipher

views = Blueprint('views', __name__)

cipher = None  # object for all methods relating to cipher

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views.route('/sendCT', methods = ['GET', 'POST'])
def sendCT():
    if request.method == "POST":
        global cipher
        cipher = Cipher(request.get_json())
        results = {
            "key": cipher.get_key(as_str=True),
            "orig": cipher.get_original()
        }
        return jsonify(results)

@views.route('/modKey', methods = ['GET', 'POST'])
def modKey():
    if request.method == "POST":
        result = request.get_json()
        firstCol = result["first"].split()
        secondCol = result["second"].split()
        key = dict(zip(firstCol, secondCol))

        cipher.modify_key_from_dict(key)

    return jsonify(cipher.get_cipher())

@views.route('/swapByFreq', methods = ['POST', 'GET'])
def swapByFreq():
    if request.method == "POST":
        cipher.swap_by_frequency()
        results = {
            "key": cipher.get_key(as_str=True),
            "plaintext": cipher.get_cipher()
        }
        return jsonify(results)

@views.route('/genSS', methods = ['POST', 'GET'])
def genSS():
    if request.method == "POST":
        result = request.get_json()
        common_ss = list(cipher.get_common_substrings(int(result)).items())

        return jsonify(common_ss)

@views.route('/genWord', methods = ['POST', 'GET'])
def genWord():
    if request.method == "POST":
        result = request.get_json()
        common_words = list(cipher.get_common_words(int(result)).items())
        
        return jsonify(common_words)

@views.route('/dupSS', methods = ['POST', 'GET'])
def dupSS():
    if request.method == "POST":
        duplicate_ss = list(cipher.get_duplicate_substrings().items())
        return jsonify(duplicate_ss)


@views.route('/resetCipher', methods = ['POST', 'GET'])
def resetCipher():
    if request.method == "POST":
        cipher.reset()
        return ""
