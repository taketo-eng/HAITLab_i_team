import os
from flask import Flask, request, render_template
from wtforms import Form, SubmitField, validators, ValidationError
from PIL import Image
import numpy as np

import glob

#Flaskを定義
app = Flask(__name__)

#画像の一時保存フォルダ
save_url = './static/images/uploads/'

@app.route('/')
def predicts():
    #uploadsフォルダ内にあるファイルを確認
    src = './static/images/uploads'
    all_file = glob.glob("%s/*" % src)
    print(all_file)
    #uploadsフォルダ内に画像ファイルがある場合それをすべて削除
    if all_file:
        for f in all_file:
            os.remove(f)

    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        #アップロードされたファイル取得
        file = request.files['file']
        #画像ファイルをnumpyの配列へ変換
        image = Image.open(file)
        image = image.convert('RGB')
        data = np.asarray(image)

        #numpy配列から画像へ変換
        reImg = Image.fromarray(data)
        
        #結果の画像を一時保存
        reImg.save(save_url + file.filename)

        return render_template('result.html', result=file.filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    #引数で設定していないのときPortは5000がデフォルト