+++
title = "flaskの基礎"
description = ""
weight = 20
+++


flask で記述したスクリプトを実行すると，
ウェブサーバとして動作する．

## flask スクリプト

拡張子 `.py` をもったテキストファイルとして作成する．
<a href="hello.py" download>hello.py</a>を参照．

#### 起動

* ファイル `hello.py` を適当なディレクトリに保存する．
* コマンドプロンプトを起動し，ファイルを保存したディレクトリに移動する．
* hello.py を実行．以下のように表示されるはず．

```
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 144-781-899
 * Running on http://localhost:8088/ (Press CTRL+C to quit)
```

#### ファイル先頭

ファイルの先頭には必ずこれを書く

```python
import flask
from flask import Flask, redirect, url_for, request, render_template, \
    flash, abort, make_response
app = Flask(__name__)
```

#### route

flask はウェブサーバである．
ブラウザからのリクエストを処理する．
下のコードは，
ブラウザが，`http://マシン名/hello` というURLにアクセスしたときに
サーバが行う動作を指定したものである．

```python
@app.route('/hello')
def func_hello():
    return 'こんにちは．'
```

一般的には次のようになる．

```
   @app.route('相対URL')
   def 名前():
       .... 関数本体 ....
```

関数の名前は適当に決めて良いし，後で変更することもできる．
ただし，以下のことに注意する．

* 半角英字で始まる半角英数字であること．
* 1つのファイル中で複数回同じ関数名を使ってはいけない．

URLはユーザに公開するものであるから，よく考えて決めなくてはいけない．

関数本体にはさまざまなことを書くことができる．少しずつ紹介する．
ここでは，単に文字列を返している．この場合，この文字列が
ブラウザに表示されることになる．

{% exc seq="12-1" %}

1. ブラウザから，`http://localhost:8088/hello` にアクセスしてみよ．
1. ソースの `'こんにちは．'` を他の文字列に書き換えてみよ．
1. ソースの `@app.route('/hello')` を `@app.route('/hello2')` に書き換え，
ブラウザから，`http://localhost:8088/hello` と
`http://localhost:8088/hello2` と
にアクセスしてみよ．
1. 関数名 func_hello を他のものに変更してみよ．

{% /exc %}

次の関数は，`http://localhost:8088/bye` へのアクセスを処理する．

```python
@app.route('/bye')
def func_bye():
    return 'さようなら．'
```

次の関数は，`http://localhost:8088/Tsurumi/University/LAIS`
へのアクセスを処理する．

```python
@app.route('/Tsurumi/University/LAIS')
def func_tu():
    return '鶴見大学ドキュメンテーション学科'
```

#### HTML文書

今までの例は，単なるテキスト文字列を返すものであった．
HTML文書をPythonレベルで作成して，メソッド render_template_string を用いると，
HTML文書を返すこともできる．

ただし，普通はこのような使い方はせず，
後述するテンプレートというものを使う．
ここでは，HTML文書も返せるということを示すために例示する．

```python
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
```

#### ファイル末尾

ファイル末尾には，当面，必ず下の2行を書く．

```python
app.run(host='localhost', port=8088, debug=True)
```


{% exc seq="12-2" %}

flask スクリプト exc12-2.py を書いて起動し，次の両方を実現せよ．

* ブラウザから，`http://localhost:8088/morning/ja` にアクセスすると，
  「おはようございます」と表示される．
* ブラウザから，`http://localhost:8088/morning/en` にアクセスすると，
  「Good Morning」と表示される．

{% /exc %}


{% exc seq="12-3" %}

flask スクリプト exc12-3.py を書いて起動し，次を実現せよ．

* ブラウザから，`http://localhost:18088/morning/ja` にアクセスすると，
  「おはようございます」と表示される．
* ブラウザから，`http://localhost:18088/morning/en` にアクセスすると，
  「Good Morning」と表示される．

{% /exc %}

