from gevent import monkey
monkey.patch_all()

import logging
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
sio = SocketIO(app, async_mode='gevent')

@app.route('/editor/<case_id>')
def editor(case_id):
    return render_template('editor.html', case_id=case_id)

@sio.on('publish_to_case')
def handle_publish(data):
    case_id = data.get('case_id')
    finding_data = data.get('finding')
    logging.info(f"Nachrichte für Raum '{case_id}' erhalten.")
    if case_id and finding_data:
        logging.info(f"Schnelle Nachricht für Raum '{case_id}' erhalten: {finding_data.get('title')}")
        sio.emit('add_finding', finding_data, room=case_id)

@sio.on('join_case')
def handle_join_case(data):
    case_id = data.get('case_id')
    if case_id:
        join_room(case_id)
        logging.info(f"Browser {request.sid} ist dem Raum '{case_id}' beigetreten.")

if __name__ == '__main__':
    logging.info("Server startet im schnellen gevent-Modus auf http://localhost:5000")
    sio.run(app, host='0.0.0.0', port=5000)