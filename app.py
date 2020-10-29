from settings.application import create_application
import logging

app = create_application()
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')

if __name__ == '__main__':
    app.run(debug=True)
