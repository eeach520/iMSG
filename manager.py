from app import create_app
from flask.ext.script import Manager

app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    # manager.run()
    app.run(host='0.0.0.0', port=80)
