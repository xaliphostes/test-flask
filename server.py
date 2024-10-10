from flask import Flask, jsonify, render_template, request
import subprocess
import shlex  # Pour une meilleure sécurité lors du parsing des commandes

app = Flask(__name__)

@app.after_request
def after_request(response):
    allowed_origins = ['http://localhost:5000', 'http://127.0.0.1:5000']
    origin = request.headers.get('Origin')
    if origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST', 'OPTIONS'])
def execute_command():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({'error': 'No command provided'}), 400

        command = data['command'].strip()
        
        # Liste des commandes autorisées (à adapter selon vos besoins)
        allowed_commands = ['ls', 'pwd', 'echo', 'date', 'du']
        
        # Vérification basique de sécurité
        command_base = shlex.split(command)[0]
        if command_base not in allowed_commands:
            return jsonify({'error': f'Command not allowed. Allowed commands: {", ".join(allowed_commands)}'}), 403

        # Exécution de la commande
        result = subprocess.check_output(command, shell=True, text=True)
        return jsonify({'output': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Command failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)