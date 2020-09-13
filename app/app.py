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

#ファイルが画像ファイルかどうか確認
allowed_files = ['jpg', 'jpeg', 'png', 'svg', 'JPG', 'JPEG']

def check_file(file_name):
    file_type = file_name.split('.')[1]
    for a in range(len(allowed_files)):
        if(file_type == allowed_files[a]):
            return 1
    return 0
    

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

        if check_file(file.filename):
            #画像ファイルをRGBへ変換
            image = Image.open(file)
            image = image.convert('RGB')

            #numpy配列に変換する場合
            #data = np.asarray(image)
            #numpy配列から画像へ変換
            #reImg = Image.fromarray(data)
            
            #結果の画像を一時保存(numpy配列変換なし)
            image.save(save_url + file.filename)
            #結果の画像を一時保存(numpy配列変換あり)
            #reImg.save(save_url + file.filename)
            return render_template('result.html', result=file.filename)
        else:
            return render_template('result.html', msg='って、あなた...', msg2='しっかり画像ファイルをアップロードしなさいよ！')
        

        

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    #引数で設定していないのときPortは5000がデフォルト