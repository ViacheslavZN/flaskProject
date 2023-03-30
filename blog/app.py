import app as app
from flask import Flask, render_template
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.views.authors import authors_app


flask_bcrypt.init_app(app)

migrate = Migrate(app, db)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SECRET_KEY"] = "abcdefg123456"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)

app = Flask(__name__)

app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(authors_app, url_prefix="/authors")

cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")


@app.route("/")
def index():
    return render_template("index.html")

@app.cli.command("create-admin")
def create_admin():
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)