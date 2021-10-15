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
from wtforms.widgets.core import ListWidget, RadioInput
from Api import API
from flask import send_from_directory
import shutil

app = Flask(__name__)
app.config["SECRET_KEY"]="oh well i hope it works this time"
#app.config["MAX_CONTENT_LENGTH"]=1024*1024
app.config["UPLOAD_PATH"] = 'uploads'

bootstrap=Bootstrap(app)
modal=Modal(app)


class FileForm(FlaskForm):
	file=FileField(validators=[FileRequired()])
	submit=SubmitField("Submit")

class RadioForm(FlaskForm): #Still in Progress
	pick=ListWidget('ul')



@app.route('/', methods=['GET','POST'])
def index():
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

	return render_template_modal('index.html', form=form, modal=modal)


@app.route('/download', methods=['GET','POST'])
def download():
	items=API.GetFileList()
	f_name = "name"
	f_id = "id"
	return render_template("download.html", items=items, f_name=f_name, f_id=f_id)