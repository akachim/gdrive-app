import os
from flask import Flask, render_template, redirect, flash, session, request
from flask.helpers import send_file, url_for
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from flask_modals import Modal
from flask_modals import render_template_modal
from werkzeug.utils import secure_filename
from Api import API
import shutil

app = Flask(__name__)
app.config["SECRET_KEY"]="oh well i hope it works this time"
#app.config["MAX_CONTENT_LENGTH"]=1024*1024
app.config["UPLOAD_PATH"] = 'uploads'

bootstrap=Bootstrap(app)
modal=Modal(app)

BOOTSTRAP_SERVE_LOCAL=True


class FileForm(FlaskForm):
	file=FileField(validators=[FileRequired()])
	submit=SubmitField("Submit")

@app.route('/', methods=['GET','POST'])
def index():

	#authenticate = API.authenticate()

	form = FileForm()
	flag = session.pop('flag', False)

	if request.method=='POST':

		uploaded_file = request.files['file']

		filename = secure_filename(uploaded_file.filename)

		if filename !='':
			#trying to make the directory
			os.mkdir(app.config["UPLOAD_PATH"])

			folder_path=os.path.join(app.config['UPLOAD_PATH'], filename)

			uploaded_file.save(folder_path)

			if form.validate_on_submit:
				API.authenticate()
				#getting the list of the file in the folder
				files=os.listdir(app.config['UPLOAD_PATH'])

				#trying to get the full path of the file
				path=os.path.abspath('{}/{}'.format(app.config["UPLOAD_PATH"],files[0]))

				API.FileUpload(path) #uploading the file

				flash("File Uploaded to drive")

				shutil.rmtree(app.config["UPLOAD_PATH"]) # removing the directory	

			session['flag'] = True

			return redirect(url_for('index'))

	modal = None if flag else 'modal-form'

	return render_template_modal('index.html', form=form, authenticate=True, modal=modal)

	
@app.route('/download', methods=['GET','POST'])
def download():
	API.authenticate()

	items= API.GetFileList()
	
	if request.method=='POST':
		files= request.form.getlist('files')
		for file in files:
			f_name= file[0]
			f_id = file[1]
			API.FileDownload(f_id, f_name)
			
		flash('Files Downloaded successfully')	
		return redirect(url_for('index'))

	return render_template("download.html", items=items)