from flask import Flask, render_template, session, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

from .models import *

#db.create_all(app=app)
#Data admin base code
class SecureView(ModelView):   
    column_hide_backrefs = False
    page_size = 50

admin_database = Admin()
admin_database.init_app(app=app)

admin_database.add_view(SecureView(Users, db.session))
admin_database.add_view(SecureView(Profile, db.session))
admin_database.add_view(SecureView(FamilyDetails, db.session))
admin_database.add_view(SecureView(DnaTest, db.session))
admin_database.add_view(SecureView(Contact, db.session))

from .views import home,user 

app.register_blueprint(home.hom, url_prefix="/")
app.register_blueprint(user.user, url_prefix="/user")



   

