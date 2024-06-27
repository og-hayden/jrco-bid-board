from flask import Flask
from app.email_watcher.routes import email_watcher_bp
from app.email_processor.routes import email_processor_bp
from app.config import DATABASE_URI
from app.models import Base
from sqlalchemy import create_engine
from app.email_watcher.email_watcher import start_email_processing
import threading

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    
    # Initialize database
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    
    # Register blueprints
    app.register_blueprint(email_watcher_bp)
    app.register_blueprint(email_processor_bp)
    
    # Start the email watching process in a separate thread
    email_thread = threading.Thread(target=start_email_processing)
    email_thread.daemon = True
    email_thread.start()
    
    return app