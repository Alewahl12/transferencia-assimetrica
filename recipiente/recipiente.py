from flask import Flask, request, render_template
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json

app = Flask(__name__)

# Carregando a chave privada
with open('C:\\Users\\Ale\\Desktop\\assimetrico_sservidor\\recipiente\\chave_privada.pem', 'rb') as key_file:
    chave_privada = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

def decrypt(mensagem_criptografada):
    # Descriptografar a mensagem com a chave privada
    mensagem_descriptografada = chave_privada.decrypt(
        bytes.fromhex(mensagem_criptografada),  # Convertendo de string hexadecimal para bytes
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_descriptografada.decode("utf-8")

@app.route('/receber_mensagem', methods=['POST'])
def receber():
    if 'mensagem_criptografada' in request.form:
        mensagem_criptografada = request.form['mensagem_criptografada']
        mensagem_descriptografada = decrypt(mensagem_criptografada)
        print(f"Mensagem recebida: {mensagem_descriptografada}")
        return "Mensagem recebida!"
    else:
        return "Error: No data received"

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
