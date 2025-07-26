from flask import Flask, request, redirect, render_template, make_response
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/guest/s/default/')
def unifi_redirect():
    # Capturar parámetros de UniFi
    ap_mac = request.args.get('ap', '')
    client_mac = request.args.get('id', '')
    timestamp = request.args.get('t', '')
    redirect_url = request.args.get('url', '')
    ssid = request.args.get('ssid', '')
    
    # Construir nueva URL para tu portal
    portal_url = f"/?ap_mac={ap_mac}&client_mac={urllib.parse.quote(client_mac)}" \
                 f"&timestamp={timestamp}&redirect={urllib.parse.quote(redirect_url)}&ssid={urllib.parse.quote(ssid)}"
    
    return redirect(portal_url, 302)

# Tu ruta principal existente
@app.route('/')
def portal():
    # Obtener parámetros de la nueva URL
    client_mac = request.args.get('client_mac', '')
    redirect_url = request.args.get('redirect', '')
    
    # Resto de tu lógica...
    return render_template('index.html', client_mac=client_mac, redirect_url=redirect_url)

# Ruta principal del portal cautivo
@app.route('/')
def portal():
    client_mac = request.args.get('id', '')
    redir_url = request.args.get('redir', 'https://google.com')

    # Guardar log de acceso
    with open('access.log', 'a') as log:
        log.write(f"{datetime.now()} - MAC: {client_mac}, Redir: {redir_url}, UA: {request.headers.get('User-Agent')}\n")

    # Detectar dispositivos iOS
    user_agent = request.headers.get('User-Agent', '')
    if 'captive.apple.com' in redir_url or 'iPhone' in user_agent or 'iPad' in user_agent:
        portal_url = f"{request.host_url}index?id={client_mac}&redir={redir_url}"
        return render_template('ios_redirect.html', portal_url=portal_url)

    # Para otros dispositivos
    portal_url = f"{request.host_url}index?id={client_mac}&redir={redir_url}"
    return render_template('click_to_continue.html', portal_url=portal_url)

# Página de encuesta/login
@app.route('/index')
def index():
    client_mac = request.args.get('id', '')
    redir_url = request.args.get('redir', 'https://google.com')
    return render_template('index.html', client_mac=client_mac, redir_url=redir_url)

# Procesar encuesta
@app.route('/procesar', methods=['POST'])
def procesar():
    redir_url = request.form.get("redir_url", "https://google.com")
    return redirect(f'/success?redir={redir_url}')

# Página de éxito
@app.route('/success')
def success():
    redir_url = request.args.get('redir', 'https://google.com')
    return render_template('success.html', redir_url=redir_url)

# Manejadores especiales de detección de red
@app.route('/library/test/success.html')
def ios_success():
    return make_response("<!DOCTYPE html><html><body>Success</body></html>", 200)

@app.route('/generate_204')
def android_204():
    return '', 204

@app.route('/ncsi.txt')
def windows_detect():
    return "Microsoft NCSI", 200

@app.route('/hotspot-detect.html')
def hotspot_detect():
    return redirect('/', 302)

# Diagnóstico de archivos
@app.route('/debug')
def debug():
    template_dir = os.path.join(os.getcwd(), 'templates')
    static_dir = os.path.join(os.getcwd(), 'static')
    return {
        "template_dir": template_dir,
        "templates_files": os.listdir(template_dir) if os.path.exists(template_dir) else [],
        "static_files": os.listdir(static_dir) if os.path.exists(static_dir) else []
    }

if __name__ == '__main__':
    app.debug = True  # Activar para ver errores
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
