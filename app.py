from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run/<script_name>', methods=['POST'])
def run_script(script_name):
    try:
        result = subprocess.run(['python', f'src/{script_name}.py'], capture_output=True, text=True)
        return jsonify({"stdout": result.stdout, "stderr": result.stderr}), result.returncode
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
