from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os, filetype, yadisk
from private.config import token as TOKEN

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
    args=""
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if filetype.guess(file).extension != '' and filetype.guess(file).extension in allowed_extensions:
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
            y = yadisk.YaDisk(token=TOKEN)
            y.upload(file, 'app:/'+str(file.filename))
            args="Жесть, ты только что загрузил(а) свой файл!\nИ даже без без флешки, прикинь"
        else:
            args="Что-то пошло не так, братишка/сестричка"
    return render_template('index.html', form=form, args=args)


if __name__ == '__main__':
   app.run(debug = True)
