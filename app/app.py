from flask import Flask, request, render_template
from wtforms import Form, SubmitField, FileField

#Flaskを定義
app = Flask(__name__)

class UploadForm(Form):
    upload = FileField('あなたの顔写真をアップロード')

    submit = SubmitField('判定')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index.html', form=form)

    elif request.method == 'GET':
        return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()
    #引数で設定していないのでPortは5000がデフォルト