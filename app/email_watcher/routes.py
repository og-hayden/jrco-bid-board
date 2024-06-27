from flask import Blueprint

email_watcher_bp = Blueprint('email_watcher', __name__)

@email_watcher_bp.route('/')
def home():
    return 'Email Watcher is running'