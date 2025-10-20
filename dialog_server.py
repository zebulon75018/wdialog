#!/usr/bin/env python3
"""
Serveur Flask pour afficher les boîtes de dialogue web
Compatible avec wdialog.py
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import socket
import threading
import json
import queue
import uuid
import sys
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dialog-web-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# File d'attente pour les requêtes de dialog
dialog_requests = {}
dialog_responses = {}

# Configuration
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 5901

@app.route('/')
def index():
    """Page principale avec l'interface de dialog"""
    return render_template('dialog_interface.html')

@socketio.on('connect')
def handle_connect():
    """Gestion de la connexion WebSocket"""
    print(f"Client connecté: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Gestion de la déconnexion"""
    print(f"Client déconnecté: {request.sid}")

@socketio.on('dialog_response')
def handle_dialog_response(data):
    """Réception de la réponse d'un dialog depuis le client web"""
    dialog_id = data.get('dialog_id')
    response = data.get('response')
    
    if dialog_id in dialog_responses:
        dialog_responses[dialog_id].put(response)

def find_free_port(start_port, max_attempts=10):
    """Trouve un port libre à partir du port de départ"""
    for port in range(start_port, start_port + max_attempts):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_socket.bind((SOCKET_HOST, port))
            test_socket.close()
            return port
        except OSError:
            continue
    return None

def socket_server_thread():
    """Thread pour gérer les connexions socket depuis wdialog.py"""
    global SOCKET_PORT
    
    # Trouver un port libre si le port par défaut est occupé
    original_port = SOCKET_PORT
    free_port = find_free_port(SOCKET_PORT)
    
    if free_port is None:
        print(f"ERREUR: Impossible de trouver un port libre entre {SOCKET_PORT} et {SOCKET_PORT + 10}")
        print("Veuillez libérer un de ces ports ou modifier la configuration.")
        return
    
    if free_port != original_port:
        print(f"ATTENTION: Le port {original_port} est occupé, utilisation du port {free_port} à la place")
        SOCKET_PORT = free_port
    
    server = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SOCKET_HOST, SOCKET_PORT))
        server.listen(5)
        print(f"✓ Serveur socket en écoute sur {SOCKET_HOST}:{SOCKET_PORT}")
        
        while True:
            try:
                client, address = server.accept()
                print(f"Connexion socket depuis {address}")
                threading.Thread(target=handle_socket_client, args=(client,), daemon=True).start()
            except Exception as e:
                print(f"Erreur lors de l'acceptation d'une connexion: {e}")
                
    except OSError as e:
        print(f"ERREUR SOCKET: {e}")
        print(f"Le port {SOCKET_PORT} est peut-être déjà utilisé.")
        print("\nPour vérifier quel processus utilise ce port, exécutez:")
        print(f"  lsof -i :{SOCKET_PORT}")
        print("ou")
        print(f"  netstat -tulpn | grep {SOCKET_PORT}")
    except Exception as e:
        print(f"Erreur socket serveur: {e}")
    finally:
        if server:
            server.close()

def handle_socket_client(client_socket):
    """Gestion d'un client socket (wdialog.py)"""
    try:
        # Réception de la requête
        data = b''
        client_socket.settimeout(30)  # Timeout de 30 secondes
        
        while True:
            try:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b'\n\n' in data:
                    break
            except socket.timeout:
                print("Timeout lors de la réception des données")
                break
        
        if not data:
            return
        
        request_data = json.loads(data.decode('utf-8'))
        dialog_id = str(uuid.uuid4())
        
        # Créer une file d'attente pour la réponse
        response_queue = queue.Queue()
        dialog_responses[dialog_id] = response_queue
        
        # Ajouter l'ID au dialog
        request_data['dialog_id'] = dialog_id
        
        # Envoyer la requête aux clients web via WebSocket
        socketio.emit('show_dialog', request_data)
        
        # Attendre la réponse (timeout de 300 secondes)
        try:
            response = response_queue.get(timeout=300)
            
            # Envoyer la réponse au client
            response_json = json.dumps(response) + '\n'
            client_socket.sendall(response_json.encode('utf-8'))
        except queue.Empty:
            # Timeout
            error_response = {'exit_code': 255, 'output': ''}
            client_socket.sendall(json.dumps(error_response).encode('utf-8'))
        
        # Nettoyer
        if dialog_id in dialog_responses:
            del dialog_responses[dialog_id]
            
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
    except Exception as e:
        print(f"Erreur lors du traitement du client socket: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            client_socket.close()
        except:
            pass

# Démarrer le serveur socket dans un thread séparé
socket_thread = threading.Thread(target=socket_server_thread, daemon=True)
socket_thread.start()

# Attendre un peu que le thread du socket démarre
time.sleep(1)

if __name__ == '__main__':
    print("=" * 50)
    print("Démarrage du serveur Dialog Web...")
    print("=" * 50)
    print(f"Interface web    : http://localhost:5000")
    print(f"Socket serveur   : {SOCKET_HOST}:{SOCKET_PORT}")
    print("=" * 50)
    print("\nPour utiliser wdialog.py, assurez-vous que:")
    print("1. Cette fenêtre reste ouverte")
    print("2. Vous ouvrez http://localhost:5000 dans votre navigateur")
    print("3. Le navigateur reste ouvert pendant l'utilisation")
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 50)
    print()
    
    try:
        socketio.run(app, host='0.0.0.0', port=5900, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n\nArrêt du serveur...")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur lors du démarrage du serveur Flask: {e}")
        sys.exit(1)
