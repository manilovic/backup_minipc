from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def buscar_btdigg():
    script_path = "/home/minipc/acestream-server/btdig_server.py"
    python_path = "/home/minipc/acestreamserver-env/bin/python3"
    env = os.environ.copy()
    env["DISPLAY"] = ":0"  # Asegúrate de que el display es correcto

    try:
        subprocess.Popen([python_path, script_path], cwd="/home/minipc/acestream-server")
        return "Servidor btdigg_server.py lanzado correctamente"
    except Exception as e:
        return f"Error al lanzar el servidor: {e}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

