from flask import Flask, request, render_template
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import io
import json

app = Flask(__name__)

# Carregando a chave pública
with open('C:\\Users\\Ale\\Desktop\\assimetrico_sservidor\\servidor\\chave_publica.pem', 'rb') as key_file:
    chave_publica = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

rota_final = "http://localhost:5001/receber_mensagem"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    mensagem = request.form.get('mensagem')
    if mensagem is not None:
        # Criptografar a mensagem com a chave pública
        mensagem_criptografada = chave_publica.encrypt(
            mensagem.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Enviar a mensagem criptografada
        dados_post = {'mensagem_criptografada': mensagem_criptografada.hex()}  # Convertendo para string hexadecimal
        requests.post(rota_final, data=dados_post)
        return dados_post['mensagem_criptografada']
    else:
        return "Error: Missing 'mensagem' data in request"

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
