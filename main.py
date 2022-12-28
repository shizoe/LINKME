from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from database import db_session
from models import Urls, User
from hashids import Hashids

main = Blueprint('main', __name__)
hashids = Hashids(min_length=4)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/<id>')
def url_redirect(id):
    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = Urls.query.filter_by(id=original_id, user_id=current_user.id).first()
        original_url = url_data.original_url
        clicks = url_data.clicks

        url_data.clicks = clicks + 1
        db_session.commit()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('main.index'))


@main.route('/home')
@login_required
def home():
    return render_template('home.html')


@main.route('/home', methods=['POST'])
def link_post():
    url = request.form.get('url')

    if not url:
        flash('The URL is required!')
        return redirect(url_for('main.home'))

    check = Urls.query.filter_by(original_url=url, user_id=current_user.id).first()
    if check:  # if a user is found, we want to redirect back to signup page so user can try again
        hashid = hashids.encode(check.id)
        short_url = (request.host_url + hashid)
        flash('Website already shortened: See the link below')
    save_url = Urls(original_url=url, user_id=current_user.id)
    db_session.add(save_url)
    db_session.commit()

    get_url = Urls.query.filter_by(original_url=url, user_id=current_user.id).first()
    hashid = hashids.encode(get_url.id)
    short_url = request.host_url + hashid

    return render_template('home.html', short_url=short_url)


@main.route('/stats')
@login_required
def stats():
    db_urls = Urls.query.filter_by(user_id=current_user.id).all()
    number = 0
    urls = []
    for url in db_urls:
        number = number + 1
        url.number = number
        url.short_url = request.host_url + hashids.encode(url.id)
        urls.append(url)

    return render_template('stats.html', urls=urls)


# insert data to sqlite database via html forms
@main.route('/stats/insert', methods=['POST'])
@login_required
def insert():
    if request.method == 'POST':
        original_url = request.form['original_url']

        check = Urls.query.filter_by(original_url=original_url, user_id=current_user.id).first()
        if check:  # if a user is found, we want to redirect back to signup page so user can try again
            hashid = hashids.encode(check.id)
            short_url = (request.host_url + hashid)
            flash('Website already shortened: The short URL is ' + short_url)
            return redirect(url_for('main.stats'))

        my_data = Urls(original_url, user_id=current_user.id)

        db_session.add(my_data)
        db_session.commit()

        flash("URL Inserted Successfully")
        return redirect(url_for('main.stats'))


# update urls
@main.route('/stats/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        my_data = Urls.query.get(request.form.get('id'))

        my_data.original_url = request.form['original_url']
        my_data.created = datetime.utcnow()

        db_session.commit()
        flash("URL Updated Successfully")
        return redirect(url_for('main.stats'))
    return redirect(url_for('main.stats'))


# delete employee
@main.route('/stats/delete/<id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    my_data = Urls.query.filter_by(id=id, user_id=current_user.id).first()
    db_session.delete(my_data)
    db_session.commit()
    flash("URL Deleted Successfully")
    return redirect(url_for('main.stats'))


def getUser(id):
    user = User.query.filter_by(id=id).first()
    return user
