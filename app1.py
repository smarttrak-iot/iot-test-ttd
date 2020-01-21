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
    rphaseVoltage = db.Column(db.Float(precision=2))
    yphaseVoltage = db.Column(db.Float(precision=2))
    bphaseVoltage = db.Column(db.Float(precision=2))
    rphaseCurrentcu = db.Column(db.Float(precision=2))
    yphaseCurrent = db.Column(db.Float(precision=2))
    bphaseCurrent = db.Column(db.Float(precision=2))
    neCurrent = db.Column(db.Float(precision=2))
    phrPower = db.Column(db.Float(precision=2))
    phrPowerFun = db.Column(db.Float(precision=2))
    phRePower = db.Column(db.Float(precision=2))
    ph3Power = db.Column(db.Float(precision=2))
    frequency = db.Column(db.Float(precision=2))
    rphasePF = db.Column(db.Float(precision=2))
    yphasePF = db.Column(db.Float(precision=2))
    bphasePF = db.Column(db.Float(precision=2))
    avgPF = db.Column(db.Float(precision=2))
    rPhaseAngle = db.Column(db.Float(precision=2))
    yPhaseAngle = db.Column(db.Float(precision=2))
    bPhaseAngle = db.Column(db.Float(precision=2))
    averageVoltage = db.Column(db.Float(precision=2))
    actFwdABS= db.Column(db.Float(precision=2))
    apfwdABS = db.Column(db.Float(precision=2))
    relagFwdABS= db.Column(db.Float(precision=2))
    releadFwdABS = db.Column(db.Float(precision=2))


    def __init__(self, devId,rphaseVoltage,yphaseVoltage,bphaseVoltage,rphaseCurrentcu,
                    yphaseCurrent,bphaseCurrent,neCurrent,phrPower,phrPowerFun,phRePower,
                    ph3Power,frequency,rphasePF,yphasePF,bphasePF,avgPF,rPhaseAngle,yPhaseAngle,
                    bPhaseAngle,averageVoltage,actFwdABS,apfwdABS,relagFwdABS,releadFwdABS):
        self.devId = devId
        self.rphaseVoltage = rphaseVoltage
        self.yphaseVoltage = yphaseVoltage
        self.bphaseVoltage = bphaseVoltage
        self.rphaseCurrentcu = rphaseCurrentcu
        self.yphaseCurrent = yphaseCurrent
        self.bphaseCurrent = bphaseCurrent
        self.neCurrent = neCurrent
        self.phrPower = phrPower
        self.phrPowerFun = phrPowerFun
        self.phRePower = phRePower
        self.ph3Power = ph3Power
        self.frequency = frequency
        self.rphasePF = rphasePF
        self.yphasePF = yphasePF
        self.bphasePF = bphasePF
        self.avgPF = avgPF
        self.rPhaseAngle = rPhaseAngle
        self.yPhaseAngle = yPhaseAngle
        self.bPhaseAngle = bPhaseAngle
        self.averageVoltage = averageVoltage
        self.actFwdABS = actFwdABS
        self.apfwdABS = apfwdABS
        self.relagFwdABS = relagFwdABS
        self.releadFwdABS = releadFwdABS

    def json(self):
        return {'devId': self.devId,'rphaseVoltage': self.rphaseVoltage,'yphaseVoltage': self.yphaseVoltage,'bphaseVoltage': self.bphaseVoltage,
                'rphaseCurrentcu': self.rphaseCurrentcu,'yphaseCurrent': self.yphaseCurrent,'bphaseCurrent': self.bphaseCurrent,'neCurrent': self.neCurrent,
                'phrPower': self.phrPower,'phrPowerFun': self.phrPowerFun,'phRePower': self.phRePower,'ph3Power': self.ph3Power,
                'frequency': self.frequency,'rphasePF': self.rphasePF,'yphasePF': self.yphasePF,'bphasePF': self.bphasePF,
                'avgPF': self.avgPF,'rPhaseAngle': self.rPhaseAngle,'yPhaseAngle': self.yPhaseAngle,'bPhaseAngle': self.bPhaseAngle,
                'averageVoltage': self.averageVoltage,'actFwdABS': self.actFwdABS,'apfwdABS': self.apfwdABS,'relagFwdABS': self.relagFwdABS,'releadFwdABS': self.releadFwdABS
                }

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
    parser.add_argument('rphaseVoltage',
        type=float
    )
    parser.add_argument('yphaseVoltage',
        type=float
    )
    parser.add_argument('bphaseVoltage',
        type=float
    )
    parser.add_argument('rphaseCurrentcu',
            type=float
    )
    parser.add_argument('yphaseCurrent',
            type=float
    )
    parser.add_argument('bphaseCurrent',
            type=float
    )
    parser.add_argument('neCurrent',
        type=float
    )
    parser.add_argument('phrPower',
        type=float
    )
    parser.add_argument('phrPowerFun',
        type=float
    )
    parser.add_argument('phRePower',
        type=float
    )
    parser.add_argument('ph3Power',
        type=float
    )
    parser.add_argument('frequency',
        type=float
    )
    parser.add_argument('rphasePF',
        type=float
    )
    parser.add_argument('yphasePF',
            type=float
    )
    parser.add_argument('bphasePF',
            type=float
    )
    parser.add_argument('avgPF',
            type=float
    )
    parser.add_argument('rPhaseAngle',
        type=float
    )
    parser.add_argument('yPhaseAngle',
        type=float
    )
    parser.add_argument('bPhaseAngle',
        type=float
    )
    parser.add_argument('averageVoltage',
            type=float
    )
    parser.add_argument('actFwdABS',
            type=float
    )
    parser.add_argument('apfwdABS',
            type=float
    )
    parser.add_argument('relagFwdABS',
        type=float
    )
    parser.add_argument('releadFwdABS',
        type=float
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

        device = DeviceModel(devId, data['rphaseVoltage'],data['yphaseVoltage'],data['bphaseVoltage'],data['rphaseCurrentcu'],data['yphaseCurrent'],
                                    data['bphaseCurrent'],data['neCurrent'],data['frequency'],data['phrPower'],data['phrPowerFun'],data['phRePower'],data['ph3Power'],
                                    data['rphasePF'],
                                    data['yphasePF'],data['bphasePF'],data['avgPF'],data['rPhaseAngle'],data['yPhaseAngle'],
                                    data['bPhaseAngle'],data['averageVoltage'],data['actFwdABS'],data['apfwdABS'],data['relagFwdABS'],
                                    data['releadFwdABS'])
        try:
            device.save_to_db()
        except:
            return {"message": "An error occurred inserting the device data."}, 500

        return device.json(), 201


    def put(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is None:
            device = DeviceModel(devId, data['rphaseVoltage'],data['yphaseVoltage'],data['bphaseVoltage'],data['rphaseCurrentcu'],data['yphaseCurrent'],
                                        data['bphaseCurrent'],data['neCurrent'],data['frequency'],data['phrPower'],data['phrPowerFun'],data['phRePower'],data['ph3Power'],
                                        data['rphasePF'],
                                        data['yphasePF'],data['bphasePF'],data['avgPF'],data['rPhaseAngle'],data['yPhaseAngle'],
                                        data['bPhaseAngle'],data['averageVoltage'],data['actFwdABS'],data['apfwdABS'],data['relagFwdABS'],
                                        data['releadFwdABS'])
        else:
            device.rphaseVoltage = data['rphaseVoltage']
            device.yphaseVoltage = data['yphaseVoltage']
            device.bphaseVoltage = data['bphaseVoltage']
            device.rphaseCurrentcu = data['rphaseCurrentcu']
            device.yphaseCurrent = data['yphaseCurrent']
            device.bphaseCurrent = data['bphaseCurrent']
            device.neCurrent = data['neCurrent']
            device.frequency = data['frequency']
            device.phrPower = data['phrPower']
            device.phrPowerFun = data['phrPowerFun']
            device.phRePower = data['phRePower']
            device.ph3Power = data['ph3Power']
            device.rphasePF = data['rphasePF']
            device.yphasePF = data['yphasePF']
            device.bphasePF = data['bphasePF']
            device.avgPF = data['avgPF']
            device.rPhaseAngle = data['rPhaseAngle']
            device.yPhaseAngle = data['yPhaseAngle']
            device.bPhaseAngle = data['bPhaseAngle']
            device.averageVoltage = data['averageVoltage']
            device.actFwdABS = data['actFwdABS']
            device.apfwdABS = data['apfwdABS']
            device.relagFwdABS = data['relagFwdABS']
            device.releadFwdABS = data['releadFwdABS']

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
    'DeviceID','rphaseVoltage','yphaseVoltage','bphaseVoltage','rphaseCurrentcu',
                    'yphaseCurrent','bphaseCurrent','neCurrent','frequency','phrPower','phrPowerFun','phRePower',
                    'ph3Power','rphasePF','yphasePF','bphasePF','avgPF','rPhaseAngle','yPhaseAngle',
                    'bPhaseAngle','averageVoltage','actFwdABS','apfwdABS','relagFwdABS','releadFwdABS'
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
    ])
)


@app.callback(Output("live-update-text", 'children'),
              [Input('live-update-text', 'className')])
def update_output_div(input_value):
    devices = DeviceModel.query.all()
    return [
        html.Table(
            [html.Tr([html.Th('DeviceID')] + [html.Th('rphaseVoltage')] + [html.Th('yphaseVoltage')] + [html.Th('bphaseVoltage')] +
                     [html.Th('rphaseCurrentcu')] + [html.Th('yphaseCurrent')] + [html.Th('yphaseVoltage')] + [html.Th('bphaseCurrent')] +
                     [html.Th('neCurrent')] + [html.Th('frequency')] + [html.Th('rphaseCurrentcu')] + [html.Th('rphasePF')] +
                     [html.Th('yphasePF')] + [html.Th('bphasePF')] + [html.Th('avgPF')] + [html.Th('rPhaseAngle')] +
                     [html.Th('yPhaseAngle')] + [html.Th('bPhaseAngle')] + [html.Th('averageVoltage')] + [html.Th('actFwdABS')] +
                     [html.Th('apfwdABS')] + [html.Th('apfwdABS')] + [html.Th('relagFwdABS')] + [html.Th('releadFwdABS')])] +
            [html.Tr([html.Td(dev.devId)] + [html.Td(dev.rphaseVoltage)] + [html.Td(dev.yphaseVoltage)] + [html.Td(dev.bphaseVoltage)] +
                     [html.Td(dev.rphaseCurrentcu)] + [html.Td(dev.yphaseCurrent)] + [html.Td(dev.yphaseVoltage)] + [html.Td(dev.bphaseCurrent)] +
                     [html.Td(dev.neCurrent)] + [html.Td(dev.frequency)] + [html.Td(dev.rphaseCurrentcu)] + [html.Td(dev.rphasePF)] +
                     [html.Td(dev.yphasePF)] + [html.Td(dev.bphasePF)] + [html.Td(dev.avgPF)] + [html.Td(dev.rPhaseAngle)] +
                     [html.Td(dev.yPhaseAngle)] + [html.Td(dev.bPhaseAngle)] + [html.Td(dev.averageVoltage)] + [html.Td(dev.actFwdABS)] +
                     [html.Td(dev.apfwdABS)] + [html.Td(dev.apfwdABS)] + [html.Td(dev.relagFwdABS)] + [html.Td(dev.releadFwdABS)])]
        )
        for dev in devices
        ]






if __name__ == '__main__':
    app.run_server(debug=True)
