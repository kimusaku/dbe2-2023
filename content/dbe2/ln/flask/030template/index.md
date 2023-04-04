+++
title = "テンプレート"
description = ""
weight = 30
+++

[この節で使用するファイル(03template.zip)](03template.zip)

HTML ファイル を動的に作成してブラウザに返すためには，
___テンプレート___ (template) を用いる．

Python 言語用のテンプレートライブラリは多数開発されている．
flask では，Jinja2 というテンプレートライブラリを用いている．
Jinja2 テンプレートの詳細な記法は 
[このページ](https://jinja.palletsprojects.com/en/3.0.x/templates)
に解説されている．Jinja2全体のマニュアルは
[このページ](https://jinja.palletsprojects.com/en/3.0.x/)
にある．

### 単純なテンプレート

テンプレートファイルは，拡張子 `.html` で作成する．
配置する場所は，flask スクリプトのあるディレクトリの下の，
`templates` サブディレクトリである．

最も単純なテンプレートは，HTML文書そのものである．

例として，単なるHTML文書である stA.html を，ブラウザに送ってみよう．
simpleTemplate1.py を実行し，
ブラウザから `http://localhost:8088/st/1` にアクセスする．

```python
@app.route('/st/1')
def func_st_1():
    return render_template('stA.html')
```

関数が render_template(filename) を返すと，
指定されたファイルの内容がブラウザに送られる．

{% exc seq="13-1" %}

勝手な内容のテンプレートファイルを任意の名前で一つ作れ．
simpleTemplate.py  を改造し，
`http://localhost:8080/st/1x` へのアクセスが行われた場合には，
そのテンプレートファイルの内容が表示されるようにせよ．

{% /exc %}

### テンプレートにデータを渡す

固定のファイルを返すのであれば，なにも「テンプレート」という
仕組みを使うまでもない．
テンプレートが行うことができることがいくつかあるが，
もっとも簡単な仕事は，値を埋め込むことである．

* 関数 template() の呼び出しの際に `変数名=値` を
  (いくつか) 指定することによって，テンプレートに値を渡すことができる．
* テンプレート内に `{`...`}` と書くことで，値を埋め込むことができる．

flask スクリプト simpleTemplate2.py を実行してみよう．

```python
@app.route('/st/2b')
def func_st_2b():
    return render_template('stB.html', hoge='こんにちは')
```

`http://localhost:8088/st/2b` にアクセスすると，上のコードが
実行され，
stB.html がブラウザに送られる．その際，`{`...`}` の値埋め込みでは，
変数 hoge の値は `'こんにちは'` として実行される．

stB.html には，次の部分がある．

```html
    <p>変数hogeの値は，{ hoge } に設定されました．</p>
```

この，`{ hoge }` の部分が，`こんにちは` に置き換わる．

`{`...`}` による埋め込みでは，値だけではなく，式も書くことができる．

```html
    <p>多数回繰り返す: { hoge * 10 } </p>
```

ここでは，hoge * 10 の計算結果である
`こんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちは` が埋め込まれることになる．

テンプレートに
複数個の値を渡すこともできる．カンマで区切って並べる．

```python
@app.route('/st/2c')
def func_st_2c():
    uchidajiro = '内田二郎'
    endo = '遠藤'
    natsuko = '夏子'
    endonatsuko = endo + natsuko
    return render_template('stC.html', name1='赤尾一郎', name2='岩瀬春子',
                    name3=uchidajiro, name4=endonatsuko)
```

Python では，現在時刻を取得するために， `datetime.datetime.now()` を
用いることができる．このことを利用して，現在時刻を表示する
ページを作ることができる．

```python
import datetime

@app.route('/st/2d')
def func_st_2d():
    now_o = datetime.datetime.now()
    s = str(now_o)
    return render_template('stD.html', nowtime=s)
```

最後の3行は，もちろん，次のようにまとめて書くこともできる:

```python
    return render_template('stD.html',
                            nowtime=str(datetime.datetime.now()))
```

{% exc seq="13-2" %}

simpleTemplate2.py や，そこで用いられているテンプレートファイルに関し，
以下を行え．

1. hoge の値を適当な他の文字列に変更して，表示が変わることを確認せよ．
1. stC.html のコメントで指示されている内容を実行してみよ．
1. /st/2d にアクセスしたとき，時刻部分 (hh:mm:ss) のみが表示されるようにせよ．
   (ヒント: 文字列 s の位置nから位置mの直前までを切り出すには，スライス
   `s[n:m]` が使える．)

{% /exc %}
