#-------------------------------------------------------------------------------
# 先頭が # で始まっている行はコメントである．

# 当面，次の行は必ず書く．
import flask
from flask import Flask, redirect, url_for, request, render_template, \
    flash, abort, make_response
app = Flask(__name__)

# 次のように書くことによって，ブラウザからの要求を処理することができる:
#
#    @app.route('相対URL')
#    def 名前():
#        .... 関数本体 ....
#
# 関数本体にはさまざまなことを書くことができる．少しずつ紹介する．

# 下の関数は，http://localhost:8088/hello というアクセスを処理する．
@app.route('/hello')
def func_hello():
    return 'こんにちは．'

#  @route('/hello')
#   「http://localhost:8088」を除いた部分 (/hello) が相対URLとして
#    指定されている．
#
#  def func_hello():
#    def の後ろに書く名前は，何でも良い．ただし，
#        - 半角英字で始まる半角英数字
#        - 1つのファイル中で複数回同じ名前を使ってはいけない．
#    最後のコロンを忘れやすいので注意する．
#
#    関数本体は，半角スペース4つを行頭に置く．
#    もっとも簡単なものは，return '文字列'
#     return 'こんにちは．'
#

# 下の関数は，http://localhost:8088/bye というアクセスを処理する．
@app.route('/bye')
def func_bye():
    return 'さようなら．'

# 下の関数は，http://localhost:8088/Tsurumi/University/LAIS
# というアクセスを処理する．
@app.route('/Tsurumi/University/LAIS')
def func_tu():
    return '鶴見大学ドキュメンテーション学科'

# 下のように，HTML文書を返すこともできる．
# ただし，普通はこのような書き方はせず，templateというものを使う．後述．
# ここでは，HTML文書も返せるということを示すために書いている．
@app.route('/rich_hello')
def func_rich_hello():
    html_page = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>ようこそ</h1>
    <hr/>
    <p>こんにちは．<span style="color:red;">どうぞ</span><b>よろしく</b></p>
    <hr/>
  </body>
</html>
'''
    return flask.render_template_string(html_page)

# ファイル末尾には，当面，必ず下の行を書く．
app.run(host='localhost', port=8088, debug=True)
