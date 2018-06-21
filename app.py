#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


from flask import Flask,flash,Blueprint,render_template,request,redirect,session,url_for,abort,send_file,safe_join
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from models import *
import bcrypt
from werkzeug import secure_filename, FileStorage
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail,Message
import datetime
import time
import random
from sqlalchemy.pool import StaticPool
import boto3,botocore
import string
from flask_mongoalchemy import MongoAlchemy
from werkzeug.utils import secure_filename
import config
#-----------------------------------------a-----------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)

# file upload config
photos = UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST']='static/img'
configure_uploads(app,photos)

@app.route('/feed')
def feed():
    posts = Posts.query.all()
    return render_template('pages/feed.html',posts=posts)


@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if bcrypt.hashpw(request.form['password'].encode('utf-8'),user.password.encode('utf-8')) == user.password.encode('utf-8'):
            session['username'] = request.form['username']
            return render_template('pages/feed.html')
    return render_template('forms/SignIn.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10))
        user_data= User(email=request.form['username'],username=request.form['username'],password=hashed_password.decode('utf-8'))
        user_data.save()
        flash('Signup Success!')
        return redirect(url_for('signin'))

    return render_template('forms/SignUp.html')

@app.route('/post',methods=['POST'])
def post():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        file = request.files['photo']
        post = Posts(caption=request.form['caption'],filename=filename,username=session['username'],category=request.form.getlist('category')[0],date=datetime.datetime.utcnow())
        post.save()
        flash('Your new post is up!')
        return redirect(url_for('feed'))







@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
