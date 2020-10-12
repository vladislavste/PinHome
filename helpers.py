from flask import current_app


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
