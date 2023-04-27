'''
CS 5920 Project
Homomorphic Encryption: What Is It and How Can It Help Secure Healthcare Systems
Spring 2023 - Date: 04/26/2023
Student: Carlos E. Torres
'''
from flask import Flask, request, jsonify
from flask import render_template
import he_enc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    result = he_enc.encrypt_send(int(data['weight']), int(data['height']))
    return jsonify(result)