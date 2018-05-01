from flask import Flask, render_template, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import socketio
import random
import json

from .utils import json_response, JSON_MIME_TYPE
from config import Config


async_mode = None

sio = socketio.Server(async_mode=async_mode)
app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Temp


@app.route('/')
def index():
    return render_template('fridge.html')


@sio.on('connect')
def connect(sid, environ):
    print(f'connected on {sid}')


@app.route('/testTemp')
def newTemp():
    temp = random.randrange(2, 10)
    sio.emit('new_temp', {'data': temp})
    resp = make_response('success', 200)
    return resp


@app.route('/api/v1/temps', methods=['GET'])
def get_temps():
    temps = [1, 1]  # TODO: query db
    return jsonify({'temps': temps})


@app.route('/api/v1/submit_temp', methods=['POST'])
def submit_temp():
    if request.content_type != JSON_MIME_TYPE:
        error = json.dumps({'error': 'Invalid Content Type'})
        return json_response(error, 400)

    data = request.json
    if not data.get('temp'):
        error = json.dumps({'error': 'Missing field (temp)'})
        return json_response(error, 400)

    temp = Temp(temperature=data['temp'])
    db.session.add(temp)
    db.session.commit()
    sio.emit('new_temp', {'data': data['temp']})
    return make_response(jsonify({'success': temp}), 201)


if __name__ == '__main__':
    if sio.async_mode == 'threading':
        # deploy with Werkzeug
        app.run(threaded=True)
    elif sio.async_mode == 'eventlet':
        # deploy with eventlet
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    elif sio.async_mode == 'gevent':
        # deploy with gevent
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
        if websocket:
            pywsgi.WSGIServer(('', 5000), app,
                              handler_class=WebSocketHandler).serve_forever()
        else:
            pywsgi.WSGIServer(('', 5000), app).serve_forever()
    elif sio.async_mode == 'gevent_uwsgi':
        print('Start the application through the uwsgi server. Example:')
        print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
              '--wsgi-file latency.py --callable app')
    else:
        print('Unknown async_mode: ' + sio.async_mode)
