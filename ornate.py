from flask import Flask,render_template,url_for,redirect,flash,request,jsonify,send_file
#from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine,asc,and_,func,extract
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import session as login_session
import string
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory

from ornate_db import Base,Admins,Students



app=Flask(__name__)

engine = create_engine('sqlite:///ornate_db.db',connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = 'static/receipts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def main_page():
	return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def regsiter():
	if request.method == 'POST':
		if 'file' not in request.files:
			return "<script> alert('File not selected')</script>"
		file = request.files['file']
			# if user does not select file, browser also
			# submit an empty part without filename
		if file.filename == '':
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			name=request.form['name']
			idnum=request.form['idnum']
			email=request.form['email']
			college=request.form['col']
			branch=request.form['branch']
			phone=request.form['pnum']
			tech = request.form.getlist('tech')
			string = ', '.join(tech)
			print(string)
			student=Students(id_num=idnum,name=name,email=email,receipt=filename,branch=branch,contact=phone,events=string)
			session.add(student)
			session.commit()
			flash('Happy ga undandi!! Your registration is successsful')
			return redirect(url_for('main_page'))
	else:
		return "<script> alert('Methods is not posting into the database! Contact the developer')</script>"
@app.route('/admin')
def admin():
	data=session.query(Students).all()
	return render_template('admin.html',data=data)

@app.route('/download/<int:id>')
def downloadfile(id):
	student=session.query(Students).filter_by(id=id).first()
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               student.file,as_attachment=True)

if __name__=='__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)