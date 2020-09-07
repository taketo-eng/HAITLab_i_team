from flask import Flask, request, render_template

#Flaskを定義
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    #引数で設定していないのでPortは5000がデフォルト