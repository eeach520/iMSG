import os
from app import create_app, db
# from app.models import User, Role, Message
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # manager.run()
