from flask import Blueprint, render_template, redirect, url_for, request, flash, render_template_string, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.home'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not password == confirm_password:
        flash("Password and Verify Password Missmatch")
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, firstname=firstname, lastname=lastname,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db_session.add(new_user)
    db_session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/changepassword')
@login_required
def changepassword():
    return render_template('changepassword.html')


@auth.route('/changepassword', methods=['POST'])
@login_required
def changepassword_post():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    verify_password = request.form.get('verify_password')
    user_email = current_user.email

    if not new_password == verify_password:
        flash('New Password Verification failed. Please Ensure that Password and Password Verify Match')
        return redirect(url_for('auth.changepassword'))

    user = User.query.filter_by(email=user_email).first()
    if not check_password_hash(user.password, old_password):
        flash('Wrong old password, Please try again or click on forget password')
        return redirect(url_for('auth.changepassword'))

    if check_password_hash(user.password, new_password):
        flash('Old password cannot be the same as the new password')
        return redirect(url_for('auth.changepassword'))

    user.password = generate_password_hash(new_password, method='sha256')
    db_session.commit()

    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')
