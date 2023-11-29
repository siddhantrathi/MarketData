from flask import Flask, jsonify, request

import json
from add_data import add_data
from fao import fao_participation_oi, processed_fao_participation_oi
from bhavcopy import index_future_and_option_data, top_5_strikes


app = Flask(__name__)


@app.route('/fetch_fao_participation_oi', methods=['GET'])
def return_fao_participation_oi():
    if (request.method == 'GET'):
        args = request.args
        data = fao_participation_oi(args.get("date", default="", type=str))
        response = jsonify({'response': data})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route('/fetch_processed_fao_participation_oi', methods=['GET'])
def return_processed_fao_participation_oi():
    if (request.method == 'GET'):
        args = request.args
        data = processed_fao_participation_oi(
            args.get("date", default="", type=str))
        response = jsonify({'response': data})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route('/fetch_index_future_and_option_data', methods=['GET'])
def return_index_future_and_option_data():
    if (request.method == 'GET'):
        args = request.args
        data = index_future_and_option_data(
            args.get("date", default="", type=str))
        response = jsonify({'response': data})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route('/top_5_strikes', methods=['GET'])
def return_top_5_strikes():
    if (request.method == 'GET'):
        args = request.args
        data = top_5_strikes(args.get("date", default="", type=str), args.get(
            "option_typ", default="", type=str), expiry=args.get("expiry", default="", type=str))
        response = jsonify({'response': data})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route('/add_data', methods=['GET'])
def return_add_data():
    if (request.method == 'GET'):
        args = request.args
        data = add_data()
        response = jsonify({'response': data})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
