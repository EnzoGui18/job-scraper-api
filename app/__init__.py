from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@db/jobsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    return app
