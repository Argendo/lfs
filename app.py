from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from werkzeug.utils import secure_filename
import os, filetype, yadisk, time
from private.config import token as TOKEN

app = Flask(__name__)
app.config['SECRET_KEY']='secsec'
app.config['UPLOAD_FOLDER']='static/files'

allowed_extensions = ['mp3', 'mp4', 'wav']

class UploadFileForm(FlaskForm):
    surname = StringField(u'Фамилия')
    file = FileField("")
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
        fsurname = form.surname.data
        if filetype.guess(file).extension != '' and filetype.guess(file).extension in allowed_extensions:
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
            y = yadisk.YaDisk(token=TOKEN)
            filelist=list(y.listdir('app:/'))
            sflist = [sub['name'] for sub in filelist]
            if len(str(fsurname))!=0:
                if len([ sub for sub in filelist if sub['name']==str(fsurname) and sub['type']=='dir']) > 0:
                    if str(file.filename) in [sub ['name'] for sub in list(y.listdir('app:/'+str(fsurname)))]:
                        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']+'/'+str(fsurname),str(file.filename[:-4])+' '+str(int(time.time()))+str(file.filename[-4:])))
                        y.upload(file, 'app:/'+str(fsurname)+'/'+str(file.filename[:-4])+' '+str(int(time.time()))+str(file.filename[-4:]))
                        args='Такое уже есть в твоей папке, но мы сохранили снова, не благодари ;)'
                    else:
                        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']+'/'+str(fsurname),file.filename))
                        y.upload(file, 'app:/'+str(fsurname)+'/'+str(file.filename))
                        args='Сохранили в твою папку ;)'
                else:
                    os.mkdir(str(app.config['UPLOAD_FOLDER'])+'/'+str(fsurname))
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']+'/'+str(fsurname),file.filename))
                    y.mkdir('app:/'+str(fsurname))
                    y.upload(file, 'app:/'+str(fsurname)+'/'+str(file.filename))
                    args="Создали твою папку и сохранили твой файл. Было сложно, но мы справились"
            else:
                if str(file.filename) in sflist:
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],str(file.filename[:-4])+' '+str(int(time.time()))+str(file.filename[-4:])))
                    y.upload(file, 'app:/'+str(file.filename[:-4])+' '+str(int(time.time()))+str(file.filename[-4:]))
                    args='У нас такое уже есть, но мы сохранили снова, не благодари ;)'
                else:
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
                    y.upload(file, 'app:/'+str(file.filename))
                    args="Всё сохранили, но в общую папку"
        else:
            args="Ничего не вышло, возможно ты загрузил(а) файл не того формата."
    return render_template('index.html', form=form, args=args)


if __name__ == '__main__':
   app.run(debug = True)
