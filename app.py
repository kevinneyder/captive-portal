from flask import Flask, request, redirect, render_template, make_response
import socket
from datetime import datetime
import os
import re

app = Flask(__name__)

# Configuración
HOST_IP = "192.168.0.187"  # Tu IP fija
PORT = 80  # Puerto 80 es esencial para móviles

# Ruta principal - Portal cautivo
@app.route('/')
def portal():
    client_mac = request.args.get('id', '')
    redir_url = request.args.get('redir', 'https://google.com')
    
    # Guardar parámetros para diagnóstico
    with open('access.log', 'a') as log:
        log.write(f"{datetime.now()} - MAC: {client_mac}, Redir: {redir_url}, User-Agent: {request.headers.get('User-Agent')}\n")
    
    # Manejo especial para dispositivos iOS
    if 'captive.apple.com' in redir_url:
        return render_template('ios_redirect.html', 
                              portal_url=f"http://{HOST_IP}/index?id={client_mac}&redir={redir_url}")
    
    return redirect(f'/index?id={client_mac}&redir={redir_url}')

# Página de encuesta
@app.route('/index')
def encuesta():
    client_mac = request.args.get('id', '')
    redir_url = request.args.get('redir', 'https://google.com')
    return render_template('index.html', client_mac=client_mac, redir_url=redir_url)

# Procesar encuesta
@app.route('/procesar', methods=['POST'])
def procesar():
    # ... (tu lógica de procesamiento existente)
    # Después de procesar, redirigir a la página de éxito
    return redirect(f'/success?redir={request.form["redir_url"]}')

# Página de éxito
@app.route('/success')
def exito():
    redir_url = request.args.get('redir', 'https://google.com')
    return render_template('success.html', redir_url=redir_url)

# --- Manejadores para dispositivos móviles ---
@app.route('/library/test/success.html')
def ios_success():
    """Manejador para iOS"""
    return make_response("<!DOCTYPE html><html><body>Success</body></html>", 200)

@app.route('/generate_204')
def android_204():
    """Manejador para Android"""
    return '', 204

@app.route('/ncsi.txt')
def windows_detect():
    """Manejador para Windows"""
    return "Microsoft NCSI", 200

@app.route('/hotspot-detect.html')
def hotspot_detect():
    """Redirección genérica para portales cautivos"""
    return redirect('/', 302)

if __name__ == '__main__':
    print(f"* Portal cautivo iniciado en http://{HOST_IP}:{PORT}")
    app.run(host='0.0.0.0', port=PORT)

@app.route('/debug')
def debug():
    return {
        "base_dir": base_dir,
        "template_dir": template_dir,
        "static_dir": static_dir,
        "templates_exist": os.path.exists(template_dir),
        "templates_files": os.listdir(template_dir) if os.path.exists(template_dir) else [],
        "static_files": os.listdir(static_dir) if os.path.exists(static_dir) else []
    }