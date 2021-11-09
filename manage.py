from flask_script import Manager,Server
from app import create_app,db
from  flask_migrate import Migrate, MigrateCommand
from app.models import User

#Create manage instance
app= create_app('test')
app = create_app('production')

#Create manage instance
manager = Manager(app)
manager.add_command('server',Server)

#Create migrate instance
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

#decorator manager.command section where will import unittest
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


#decorator manager.shell section
@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User)

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'choomba'
    app.config['DATABASE_URL'] = 'postgresql+psycopg2://esa:moringa@localhost/sin_city'
    manager.run()
