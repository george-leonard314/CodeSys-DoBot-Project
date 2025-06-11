import multiprocessing
import threading
import time
from flask import Flask, render_template_string, request, redirect, url_for, flash
from serial.tools import list_ports
import pydobot
import DobotDllType as dType

app = Flask(__name__)
app.secret_key = 'very-secret-key'

HTML_INDEX = """
<!doctype html>
<html><head><meta charset="utf-8"><title>DoBot Control</title></head>
<body>
  <h1>DoBot Magician Control</h1>
  {% with msgs = get_flashed_messages() %}
    {% if msgs %}
      <ul>{% for m in msgs %}<li>{{m}}</li>{% endfor %}</ul>
    {% endif %}
  {% endwith %}
  <form action="{{url_for('start')}}" method="post">
    <button type="submit">Start Movement</button>
  </form>
  <form action="{{url_for('stop')}}" method="post">
    <button type="submit">Stop Movement</button>
  </form>
</body></html>
"""

robot_proc = None

def get_dobot_port():
    for p in list_ports.comports():
        if 'ACM' in p.device or 'USB' in p.device:
            return p.device
    raise RuntimeError("Could not find DoBot on an ACM/USB port")

def run_robot_sequence():
    """Runs in a separate process."""
    port = get_dobot_port()
    device = pydobot.Dobot(port='/dev/ttyACM0', verbose=False)
    try:
        init_pos    = (268.1,   0.0,   52.0,   0.0)
        middle_step = (215.7, 192.1,   41.2,   0.0)
        nfc_tag     = (176.0, 224.3, -115.6,   0.0)
        tag_on_belt = (267.6,   7.7,  -17.0,   0.0)

        device.move_to(*init_pos, wait=True)
        device.move_to(*middle_step, wait=True)
        device.move_to(*nfc_tag, wait=True)
        device.suck(True)
        device.move_to(*middle_step, wait=True)
        device.move_to(*init_pos, wait=True)
        device.move_to(*tag_on_belt, wait=True)
        device.suck(False)
        device.move_to(*init_pos, wait=True)

    finally:
        # always turn off suction and close
        try: device.suck(False)
        except: pass
        try: device.close()
        except: pass

@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

@app.route('/start', methods=['POST'])
def start():
    global robot_proc
    # If there's already a live process, we refuse to start again
    if robot_proc and robot_proc.is_alive():
        flash("Robot is already running.")
    else:
        # clean up any dead process handle
        robot_proc = multiprocessing.Process(target=run_robot_sequence, daemon=True)
        robot_proc.start()
        flash("Robot sequence started.")
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    global robot_proc

    # 1) Send a *physical* emergency-stop via Dobot DLL:
    try:
        api = dType.load()
        dType.ConnectDobot(api, get_dobot_port(), 115200)
        dType.SetArmEmergencyStop(api)      # immediate hardware kill
        dType.DisconnectDobot(api)
    except Exception as e:
        app.logger.exception("Failed to send hardware E-STOP")

    # 2) Terminate the Python process running the sequence
    if robot_proc and robot_proc.is_alive():
        robot_proc.terminate()
        robot_proc.join(timeout=1)
        flash("Stop command sent.")
    else:
        flash("No robot process was running.")

    robot_proc = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Note: On Linux you must protect the entry‐point for multiprocessing
    multiprocessing.freeze_support()
    app.run(host='0.0.0.0', port=5000, debug=True)
