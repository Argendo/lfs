from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY']='secsec'
app.config['UPLOAD_FOLDER']='static/files'

allowed_extensions = ['mp3', 'mp4', 'wav']

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Вот сюда жмакай, чтобы нам файл заслать")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if file.filename != '' and allowed_file(file.filename):
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
            return "Жесть, ты только что загрузил(а) свой файл!\nИ даже без без флешки, прикинь"
    return render_template('index.html', form=form)

if __name__ == '__main__':
   app.run(debug = True)
