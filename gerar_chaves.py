import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def save_keys(private_key_pem, public_key_pem, private_key_dir, public_key_dir):
    # Salvar a chave privada em um arquivo no diretório especificado
    private_key_path = os.path.join(private_key_dir, 'chave_privada.pem')
    with open(private_key_path, 'wb') as private_key_file:
        private_key_file.write(private_key_pem)

    # Salvar a chave pública em um arquivo no diretório especificado
    public_key_path = os.path.join(public_key_dir, 'chave_publica.pem')
    with open(public_key_path, 'wb') as public_key_file:
        public_key_file.write(public_key_pem)

def generate_rsa_key_pair(private_key_dir, public_key_dir):
    # Gerar um par de chaves RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Obter a chave pública
    public_key = private_key.public_key()

    # Serializar a chave privada para o formato PEM
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serializar a chave pública para o formato PEM
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Salvar as chaves nos diretórios especificados
    save_keys(private_key_pem, public_key_pem, private_key_dir, public_key_dir)

    print("Chaves RSA geradas e salvas com sucesso!")



# Diretórios onde as chaves serão salvas
private_key_dir = 'recipiente'
public_key_dir = 'servidor'

# Gerar e salvar as chaves nos diretórios especificados
generate_rsa_key_pair(private_key_dir, public_key_dir)
