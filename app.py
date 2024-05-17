from flask import Flask
from routes.usuarios import usuario_bp

app = Flask(__name__)

app.register_blueprint(usuario_bp, url_prefix='/usuarios')

if __name__ == '__main__':
    app.run(debug=True)