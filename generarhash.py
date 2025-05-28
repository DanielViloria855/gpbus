from werkzeug.security import generate_password_hash

# Usa pbkdf2:sha256 para que sea compatible con check_password_hash
password_plano = "1234567"
hash = generate_password_hash(password_plano, method='pbkdf2:sha256')

print(hash)
