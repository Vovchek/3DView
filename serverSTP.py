from flask import Flask, request, send_file
from flask_cors import CORS
import os
import shutil
import subprocess
import tempfile
import threading
import time

FREECAD_CMD = r"C:\Program Files\FreeCAD 1.0\bin\FreeCADCmd.exe"

app = Flask(__name__)
CORS(app)

def wait_for_stable_file(file_path, timeout=10, poll_interval=0.5):
    """Wait for file size to stop changing (file has finished writing)."""
    waited = 0
    last_size = -1
    while waited < timeout:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == last_size:
                return True
            last_size = current_size
        time.sleep(poll_interval)
        waited += poll_interval
    return False

def delayed_cleanup(path, delay=5):
    time.sleep(delay)
    try:
        shutil.rmtree(path)
        print(f"[CLEANUP] Removed temp dir: {path}")
    except Exception as e:
        print(f"[CLEANUP] Failed to delete temp dir: {e}")

@app.route('/convert', methods=['POST'])
def convert_step_to_stl():
    tmpdir = tempfile.mkdtemp()
    try:
        step_path = os.path.join(tmpdir, 'input.step')
        stl_path = os.path.join(tmpdir, 'output.stl')

        file = request.files['file']
        file.save(step_path)

        subprocess.run([FREECAD_CMD, 'convert_script.py', step_path, stl_path], check=True)

        stable = wait_for_stable_file(stl_path)
        if not stable:
            return 'STL not ready or timed out', 500

        print(f"[SERVER] STL ready. Size: {os.path.getsize(stl_path)} bytes")

        # Delayed cleanup thread
        threading.Thread(target=delayed_cleanup, args=(tmpdir,), daemon=True).start()

        return send_file(stl_path, mimetype='application/sla', as_attachment=False)

    except Exception as e:
        print(f"[ERROR] Conversion failed: {e}")
        shutil.rmtree(tmpdir, ignore_errors=True)
        return 'Conversion failed', 500

if __name__ == '__main__':
    app.run(debug=True)
