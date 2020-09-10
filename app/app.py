import os
from flask import redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

from flask import Flask, request, render_template
from wtforms import Form, SubmitField, FileField
from PIL import Image
import numpy as np

class UploadForm(Form):
    upload = FileField('あなたの顔写真をアップロード')
    submit = SubmitField('判定')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

#Flaskを定義
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def predicts():
    form = UploadForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index.html', form=form)
        else:
            # file = request.files['file']
            # image = Image.open(file)
            # image = image.convert('RGB')
            # data = np.asarray(image)
            # reImg = Image.fromarray(data)
            # return render_template('result.html', data=reImg)
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']

            if file.filename=='':
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER']))

                return redirect(url_for('uploaded_file', filename=filename))
    elif request.method == 'GET':
        return render_template('index.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    #引数で設定していないのときPortは5000がデフォルト