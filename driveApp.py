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
				#API.authenticate()
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
	#items= #API.GetFileList()
	
	items=[{'id': '1srtAtR52s0g8xnMrkmuMzqs-en_L2M5n', 'name': 'cam18May2021151632.png'},
    {'id': '1GGSF-zvXfWHs5Kcvgth31zirPcIf9VEE', 'name': 'Flask_Web_Development_Developing_Web_Applications_With_Python_by_Miguel_Grinberg_z-lib.org.pdf'}, 
    {'id': '18XnZNpMIbaYdMDEPfnnA32RnDuxpkd0u', 'name': 'gweb.py'}, 
    {'id': '1sRsS3-Is3lyBM3d6guANoTKF_lQB8JK3', 'name': 'drive-app.py'}, 
    {'id': '1TffJSWw2sLlPMuCKJWcAWDPlyaNHIj1E', 'name': 'download-upload-drive.py'}, 
    {'id': '1idAzrd7u0k-cq-Q60JoWcw-dV4aoGxpp', 'name': 'Copy of Welcome To Colaboratory'}, 
    {'id': '1atsG_EyQSbney1d2hXW5j2KqN1X-Vk3nFuYNKOdI5Wk', 'name': 'COBWEB Manual'}, 
    {'id': '14-aM0cUj7006GqzSxsKpq2Blv8o9MuDYk0iooWk9c28', 'name': 'Copy of COBWEB Manual'}, 
    {'id': '1161YKuTmcMfvjxWBF74IQ6JWg_rAtqBN', 'name': 'COBWEB-Literature review'}, 
    {'id': '1zA6Kj4Cx_oYAT1EycCqNow7gHYMdFLYg', 'name': 'me.jpg'}]


	return render_template("download.html", items=items)