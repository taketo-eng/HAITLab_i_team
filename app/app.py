import os
from flask import Flask, request, render_template
from wtforms import Form, SubmitField, validators, ValidationError
from PIL import Image
import numpy as np

import glob

#Flaskを定義
app = Flask(__name__)

save_url = './static/images/uploads/'

@app.route('/')
def predicts():
    src = './static/images/uploads'
    all_file = glob.glob("%s/*" % src)
    print(all_file)
    if all_file:
        for f in all_file:
            os.remove(f)
    else:
        print('False')

    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        image = Image.open(file)
        image = image.convert('RGB')
        data = np.asarray(image)

        reImg = Image.fromarray(data)
        
        reImg.save(save_url + file.filename)

        return render_template('result.html', result=file.filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    #引数で設定していないのときPortは5000がデフォルト