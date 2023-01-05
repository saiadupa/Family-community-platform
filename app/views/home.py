from flask import Blueprint, redirect, render_template, request, url_for, jsonify, session, flash
from passlib.hash import sha256_crypt
from ..models import *

hom = Blueprint('hom', __name__ , static_folder="static", template_folder="templates")

@hom.route('/', methods=["GET","POST"])
def home():

    if request.method == "POST":
        email = request.form.get('email')
        pswd = request.form.get('pswd')

        user = Users.query.filter_by(email=email).first()
        print("found user")
        if user:
            if sha256_crypt.verify(pswd, user.password):
                session['id'] = user.id
                return redirect(url_for('user.profile'))
            flash('Invalid password!')
        flash('Invalid Credentials!')
    return render_template('home/home.html')

@hom.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        s_name = request.form.get('s_name')
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        pswd = request.form.get('pswd')
        pno = request.form.get('p_no')

        pswd = sha256_crypt.hash(pswd)
        
        if Users.query.filter_by(email=email).first():
            return jsonify({"message": "This email is already registered."})
        else:
            user = Users(sur_name=s_name.lower(),first_name=f_name.lower(),last_name=l_name.lower(),email=email,password=pswd,phone_number=pno,registered=True)
            db.session.add(user)
            db.session.commit()

            session['id'] = Users.query.filter_by(email=email).first().id

            return redirect(url_for('user.profile'))

    return render_template('home/signup.html')

@hom.route('/about')
def about():
    return render_template('about.html')

@hom.route('/contact', methods=['GET','POST'])
def contact():
    return render_template('contact.html')


