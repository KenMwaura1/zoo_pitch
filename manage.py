from flask_migrate import Migrate
from app import create_app
from config import config_options
from commands import photo_config, db_config, login_config, mail_config,db

app = create_app('development')
app.config.from_object(config_options['development'])
# print(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
photo_config(app)
db_config(app)
login_config(app)
mail_config(app)
migrate = Migrate(app, db)


@app.cli.command("db")
def db():
    """command to migrate"""

