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
    rphvol = db.Column(db.Float(precision=2))
    yphvol = db.Column(db.Float(precision=2))
    bphvol = db.Column(db.Float(precision=2))
    rphcu = db.Column(db.Float(precision=2))
    yphcu = db.Column(db.Float(precision=2))
    bphcu = db.Column(db.Float(precision=2))
    necu = db.Column(db.Float(precision=2))
    phrpwr = db.Column(db.Float(precision=2))
    phrpwrfun = db.Column(db.Float(precision=2))
    phrepwr = db.Column(db.Float(precision=2))
    ph3pwr = db.Column(db.Float(precision=2))
    freq = db.Column(db.Float(precision=2))
    rphpf = db.Column(db.Float(precision=2))
    yphpf = db.Column(db.Float(precision=2))
    bphpf = db.Column(db.Float(precision=2))
    avgpf = db.Column(db.Float(precision=2))
    rphang = db.Column(db.Float(precision=2))
    yphang = db.Column(db.Float(precision=2))
    bphang = db.Column(db.Float(precision=2))
    avgvol = db.Column(db.Float(precision=2))
    actfwdABS= db.Column(db.Float(precision=2))
    apfwdABS = db.Column(db.Float(precision=2))
    relagfwdABS= db.Column(db.Float(precision=2))
    releadfwdABS = db.Column(db.Float(precision=2))


    def __init__(self, devId,rphvol,yphvol,bphvol,rphcu,
                    yphcu,bphcu,necu,phrpwr,phrpwrfun,phrepwr,
                    ph3pwr,freq,rphpf,yphpf,bphpf,avgpf,rphang,yphang,
                    bphang,avgvol,actfwdABS,apfwdABS,relagfwdABS,releadfwdABS):
        self.devId = devId
        self.rphvol = rphvol
        self.yphvol = yphvol
        self.bphvol = bphvol
        self.rphcu = rphcu
        self.yphcu = yphcu
        self.bphcu = bphcu
        self.necu = necu
        self.phrpwr = phrpwr
        self.phrpwrfun = phrpwrfun
        self.phrepwr = phrepwr
        self.ph3pwr = ph3pwr
        self.freq = freq
        self.rphpf = rphpf
        self.yphpf = yphpf
        self.bphpf = bphpf
        self.avgpf = avgpf
        self.rphang = rphang
        self.yphang = yphang
        self.bphang = bphang
        self.avgvol = avgvol
        self.actfwdABS = actfwdABS
        self.apfwdABS = apfwdABS
        self.relagfwdABS = relagfwdABS
        self.releadfwdABS = releadfwdABS

    def json(self):
        return {'devId': self.devId,'rphvol': self.rphvol,'yphvol': self.yphvol,'bphvol': self.bphvol,
                'rphcu': self.rphcu,'yphcu': self.yphcu,'bphcu': self.bphcu,'necu': self.necu,
                'phrpwr': self.phrpwr,'phrpwrfun': self.phrpwrfun,'phrepwr': self.phrepwr,'ph3pwr': self.ph3pwr,
                'freq': self.freq,'rphpf': self.rphpf,'yphpf': self.yphpf,'bphpf': self.bphpf,
                'avgpf': self.avgpf,'rphang': self.rphang,'yphang': self.yphang,'bphang': self.bphang,
                'avgvol': self.avgvol,'actfwdABS': self.actfwdABS,'apfwdABS': self.apfwdABS,'relagfwdABS': self.relagfwdABS,'releadfwdABS': self.releadfwdABS
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
    parser.add_argument('rphvol',
        type=float
    )
    parser.add_argument('yphvol',
        type=float
    )
    parser.add_argument('bphvol',
        type=float
    )
    parser.add_argument('rphcu',
            type=float
    )
    parser.add_argument('yphcu',
            type=float
    )
    parser.add_argument('bphcu',
            type=float
    )
    parser.add_argument('necu',
        type=float
    )
    parser.add_argument('phrpwr',
        type=float
    )
    parser.add_argument('phrpwrfun',
        type=float
    )
    parser.add_argument('phrepwr',
        type=float
    )
    parser.add_argument('ph3pwr',
        type=float
    )
    parser.add_argument('freq',
        type=float
    )
    parser.add_argument('rphpf',
        type=float
    )
    parser.add_argument('yphpf',
            type=float
    )
    parser.add_argument('bphpf',
            type=float
    )
    parser.add_argument('avgpf',
            type=float
    )
    parser.add_argument('rphang',
        type=float
    )
    parser.add_argument('yphang',
        type=float
    )
    parser.add_argument('bphang',
        type=float
    )
    parser.add_argument('avgvol',
            type=float
    )
    parser.add_argument('actfwdABS',
            type=float
    )
    parser.add_argument('apfwdABS',
            type=float
    )
    parser.add_argument('relagfwdABS',
        type=float
    )
    parser.add_argument('releadfwdABS',
        type=float
    )


    def get(self, devId):
        device = DeviceModel.find_by_name(devId)
        if device:
            return device.json()
        return {'message': 'Device not found'}, 404

    def post(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is None:
            device = DeviceModel(devId, data['rphvol'],data['yphvol'],data['bphvol'],data['rphcu'],data['yphcu'],
                                        data['bphcu'],data['necu'],data['freq'],data['phrpwr'],data['phrpwrfun'],data['phrepwr'],data['ph3pwr'],
                                        data['rphpf'],
                                        data['yphpf'],data['bphpf'],data['avgpf'],data['rphang'],data['yphang'],
                                        data['bphang'],data['avgvol'],data['actfwdABS'],data['apfwdABS'],data['relagfwdABS'],
                                        data['releadfwdABS'])
        else:
            device.rphvol = data['rphvol']
            device.yphvol = data['yphvol']
            device.bphvol = data['bphvol']
            device.rphcu = data['rphcu']
            device.yphcu = data['yphcu']
            device.bphcu = data['bphcu']
            device.necu = data['necu']
            device.freq = data['freq']
            device.phrpwr = data['phrpwr']
            device.phrpwrfun = data['phrpwrfun']
            device.phrepwr = data['phrepwr']
            device.ph3pwr = data['ph3pwr']
            device.rphpf = data['rphpf']
            device.yphpf = data['yphpf']
            device.bphpf = data['bphpf']
            device.avgpf = data['avgpf']
            device.rphang = data['rphang']
            device.yphang = data['yphang']
            device.bphang = data['bphang']
            device.avgvol = data['avgvol']
            device.actfwdABS = data['actfwdABS']
            device.apfwdABS = data['apfwdABS']
            device.relagfwdABS = data['relagfwdABS']
            device.releadfwdABS = data['releadfwdABS']

        #data = Device.parser.parse_args()

        #device = DeviceModel(devId, data['rphvol'],data['yphvol'],data['bphvol'],data['rphcu'],data['yphcu'],
        #                            data['bphcu'],data['necu'],data['freq'],data['phrpwr'],data['phrpwrfun'],data['phrepwr'],data['ph3pwr'],
        #                            data['rphpf'],
        #                            data['yphpf'],data['bphpf'],data['avgpf'],data['rphang'],data['yphang'],
        #                            data['bphang'],data['avgvol'],data['actfwdABS'],data['apfwdABS'],data['relagfwdABS'],
        #                            data['releadfwdABS'])


        try:
            device.save_to_db()
        except:
            return {"message": "An error occurred inserting the device data."}, 500

        return device.json(), 201


    def put(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is None:
            device = DeviceModel(devId, data['rphvol'],data['yphvol'],data['bphvol'],data['rphcu'],data['yphcu'],
                                        data['bphcu'],data['necu'],data['freq'],data['phrpwr'],data['phrpwrfun'],data['phrepwr'],data['ph3pwr'],
                                        data['rphpf'],
                                        data['yphpf'],data['bphpf'],data['avgpf'],data['rphang'],data['yphang'],
                                        data['bphang'],data['avgvol'],data['actfwdABS'],data['apfwdABS'],data['relagfwdABS'],
                                        data['releadfwdABS'])
        else:
            device.rphvol = data['rphvol']
            device.yphvol = data['yphvol']
            device.bphvol = data['bphvol']
            device.rphcu = data['rphcu']
            device.yphcu = data['yphcu']
            device.bphcu = data['bphcu']
            device.necu = data['necu']
            device.freq = data['freq']
            device.phrpwr = data['phrpwr']
            device.phrpwrfun = data['phrpwrfun']
            device.phrepwr = data['phrepwr']
            device.ph3pwr = data['ph3pwr']
            device.rphpf = data['rphpf']
            device.yphpf = data['yphpf']
            device.bphpf = data['bphpf']
            device.avgpf = data['avgpf']
            device.rphang = data['rphang']
            device.yphang = data['yphang']
            device.bphang = data['bphang']
            device.avgvol = data['avgvol']
            device.actfwdABS = data['actfwdABS']
            device.apfwdABS = data['apfwdABS']
            device.relagfwdABS = data['relagfwdABS']
            device.releadfwdABS = data['releadfwdABS']

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
    'DeviceID','rphvol','yphvol','bphvol','rphcu',
                    'yphcu','bphcu','necu','freq','phrpwr','phrpwrfun','phrepwr',
                    'ph3pwr','rphpf','yphpf','bphpf','avgpf','rphang','yphang',
                    'bphang','avgvol','actfwdABS','apfwdABS','relagfwdABS','releadfwdABS'
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
            [html.Tr([html.Th('Dev')] + [html.Th('rphV')] + [html.Th('yphV')] + [html.Th('bphV')] +
                     [html.Th('rphI')] + [html.Th('yphI')] + [html.Th('bphI')] +
                     [html.Th('neI')] + [html.Th('freq')] + [html.Th('phrP')] + [html.Th('phrPfn')] + [html.Th('phrepwr')] + [html.Th('ph3P')] + [html.Th('rphpf')] +
                     [html.Th('yphpf')] + [html.Th('bphpf')] + [html.Th('Apf')] + [html.Th('rphAn')] +
                     [html.Th('yphAn')] + [html.Th('bphAn')] + [html.Th('AvgV')] + [html.Th('|actfwd|')] +
                     [html.Th('|apfwd|')] + [html.Th('|rg|')] + [html.Th('|rd|')])] +
            [html.Tr([html.Td(dev.devId)] + [html.Td(dev.rphvol)] + [html.Td(dev.yphvol)] + [html.Td(dev.bphvol)] +
                     [html.Td(dev.rphcu)] + [html.Td(dev.yphcu)] + [html.Td(dev.bphcu)] +
                     [html.Td(dev.necu)] + [html.Td(dev.freq)] + [html.Td(dev.phrpwr)] + [html.Td(dev.phrpwrfun)] + [html.Td(dev.phrepwr)] + [html.Td(dev.ph3pwr)] + [html.Td(dev.rphpf)] +
                     [html.Td(dev.yphpf)] + [html.Td(dev.bphpf)] + [html.Td(dev.avgpf)] + [html.Td(dev.rphang)] +
                     [html.Td(dev.yphang)] + [html.Td(dev.bphang)] + [html.Td(dev.avgvol)] + [html.Td(dev.actfwdABS)] +
                     [html.Td(dev.apfwdABS)] + [html.Td(dev.relagfwdABS)] + [html.Td(dev.releadfwdABS)])]
        )
        for dev in devices
        ]






if __name__ == '__main__':
    app.run_server(debug=True)
