'''
pip install Flask pywin32 passlib


'''
import os
import win32net
import win32netcon
import string
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from passlib.context import CryptContext

app = Flask(__name__)

# Configuración para gestionar las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar si el usuario existe en Windows
def user_exists(username):
    try:
        win32net.NetUserGetInfo(None, username, 1)
        return True
    except win32net.error:
        return False

# Función para generar una contraseña aleatoria
def generate_temp_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Ruta para generar una contraseña temporal
@app.route('/generate_password', methods=['POST'])
def generate_password():
    data = request.get_json()
    username = data.get('username')

    # Verificar si el usuario existe en el sistema Windows
    if not user_exists(username):
        return jsonify({"error": "El usuario no existe"}), 404

    # Generar una contraseña temporal
    temp_password = generate_temp_password()
    
    # Establecer el tiempo de expiración (4 horas a partir de ahora)
    expiration_time = datetime.now() + timedelta(hours=4)

    # Aquí se puede guardar la contraseña temporal y la fecha de expiración en una base de datos si es necesario
    # Por simplicidad, la imprimimos en la consola
    print(f"Usuario: {username}, Contraseña temporal: {temp_password}, Expira: {expiration_time}")

    # Hashear la contraseña antes de devolverla
    hashed_password = pwd_context.hash(temp_password)

    # Retornar la contraseña generada y la fecha de expiración
    return jsonify({
        "username": username,
        "temp_password": temp_password,
        "expires_at": expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(debug=True)
