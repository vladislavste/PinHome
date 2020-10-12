from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings.application import create_application
from ext import db

manager = Manager(create_application)
migrate = Migrate(create_application, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
