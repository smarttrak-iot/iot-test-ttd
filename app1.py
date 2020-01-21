import os
import pathlib

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, request,render_template
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq

import pandas as pd


server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = 'smarttrak'
api = Api(server)
db = SQLAlchemy()

db.init_app(server)

@server.before_first_request
def create_tables():
    db.create_all()

class DeviceModel(db.Model):
    __tablename__ = 'devices'

    devId = db.Column(db.String(20), primary_key=True)
    power = db.Column(db.Float(precision=2))
    voltage = db.Column(db.Float(precision=2))
    current = db.Column(db.Float(precision=2))

    def __init__(self, devId,power,voltage,current):
        self.devId = devId
        self.power = power
        self.voltage = voltage
        self.current = current

    def json(self):
        return {'devId': self.devId,'power': self.power,'voltage': self.voltage,'current': self.current}

    @classmethod
    def find_by_name(cls, devId):
        return cls.query.filter_by(devId=devId).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Device(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('power',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('voltage',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('current',
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )


    def get(self, devId):
        device = DeviceModel.find_by_name(devId)
        if device:
            return device.json()
        return {'message': 'Device not found'}, 404

    def post(self, devId):
        if DeviceModel.find_by_name(devId):
            return {'message': "A Device with devId '{}' already exists.".format(devId)}, 400

        data = Device.parser.parse_args()

        device = DeviceModel(devId, data['power'],data['voltage'],data['current'])

        try:
            device.save_to_db()
        except:
            return {"message": "An error occurred inserting the device data."}, 500

        return device.json(), 201


    def put(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is None:
            device = DeviceModel(devId, data['power'],data['voltage'],data['current'])
        else:
            device.power = data['power']
            device.voltage = data['voltage']
            device.current = data['current']

        device.save_to_db()

        return device.json()


class DeviceList(Resource):
    def get(self):
        return {'devices': [x.json() for x in DeviceModel.query.all()]}



#@server.route('/')
#def index():
    #devices = DeviceModel.query.all()
    #return render_template('index.html',devices=devices)

api.add_resource(Device, '/device/<string:devId>')
api.add_resource(DeviceList, '/devices')

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

params = [
    'DeviceID','Power','Voltage','Current'
]

app = dash.Dash(
    __name__,
    server=server,
    #routes_pathname_prefix='/dash/'
    #meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.layout = html.Div(
    html.Div([
        html.H4('Substation Data Live Feed'),
        html.Table(id="live-update-text"),
        dcc.Input(
            id='devId',
            value='devPower', # in milliseconds
        )
    ])
)


@app.callback(Output("live-update-text", 'children'),
              [Input('live-update-text', 'className')])
def update_output_div(input_value):
    devices = DeviceModel.query.all()
    return [
        html.Table(
            [html.Tr([html.Th('DeviceID')] + [html.Th('Power')] + [html.Th('Voltage')] + [html.Th('Current')])] +
            [html.Tr([html.Td(dev.devId)] + [html.Td(dev.power)] + [html.Td(dev.voltage)] + [html.Td(dev.current)])]
        )
        for dev in devices
        ]






if __name__ == '__main__':
    app.run_server(debug=True)
