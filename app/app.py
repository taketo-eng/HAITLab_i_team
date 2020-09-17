import os
import gan
#from ipynb.fs.full.gan import *
from flask import Flask, request, render_template
from wtforms import Form, SubmitField, validators, ValidationError
from PIL import Image
import numpy as np

import glob

import tensorflow as tf

#Flaskを定義
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
    
src = './static/images/uploads'
def deleteImg():
    #uploadsフォルダ内にあるファイルを確認
    all_file = glob.glob("%s/*" % src)
    print(all_file)
    #uploadsフォルダ内に画像ファイルがある場合それをすべて削除
    if all_file:
        for f in all_file:
            os.remove(f)

#ProGanの処理
#filenameを受け取り、一時保存した画像を取得できるようにしている
def ganProcess(filename):
    if gan.image_from_module_space:
        target_image = gan.get_module_space_image()
    else:
        #ファイル取得
        target_image = gan.upload_image(save_url + filename)
        target_image= target_image.astype("float32")
      
        #学習
        images, loss = gan.find_closest_latent_vector(gan.num_optimization_steps, gan.steps_per_image, target_image)

        #test保存(学習後)
        test2 = Image.fromarray((images[len(images)-1] * 255).astype(np.uint8))
        test2.save(save_url+'test2.jpg')

        #学習結果で得られた画像をgifに変換し、保存する
        print(np.array(images).shape)
        gan.animate(np.stack(images))


@app.route('/', methods=['GET', 'POST'])
def predicts():
    #uploadsフォルダがパンクしないように削除処理
    deleteImg()
    
    #送信されたら以下のif文がTrue
    if request.method == 'POST':
        #アップロードされたファイル取得
        file = request.files['file']

        #画像以外のファイルがアップロードされた時の文言
        msg = ['って、あなた...', 'しっかり画像ファイルをアップロードしなさいよ！']

        if not check_file(file.filename):
            #画像以外のファイルが送信された時の処理
            return render_template('result.html', msg=msg[0], msg2=msg[1])
        
        if file.filename == '':
            #画像ファイル名が存在しないときもダメ
            return render_template('result.html', msg=msg[0], msg2=msg[1])
        
        #問題なく突破すれば下の処理に進む
        #画像ファイルをRGBへ変換
        image = Image.open(file)
        image = image.convert('RGB')
        #アップロード画像を一時保存し、のちのGANに渡せるようにする
        image.save(save_url + file.filename)


        #学習回数 default value is 200
        gan.num_optimization_steps=200

        #ProGanの処理関数
        ganProcess(file.filename)
        return render_template('result.html', result='animation.gif')
            
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    #引数で設定していないのときPortは5000がデフォルト