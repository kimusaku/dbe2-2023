+++
title = "ユーザ認証"
description = ""
weight = 60
+++

特定の利用者にだけアクセスを許すような運用をしたい場合，
ユーザ名とパスワードによって，利用者を認証することになる．
ページを遷移するたびに利用者にパスワードを入力させるわけには
いかないので，一度パスワードによって認証した利用者の，その後の
アクセスを認めるようにしなければならない．

Flask には，外部ライブラリ Flask-Login が用意されており，
これを用いると，認証機構を比較的簡単に構築することができる．


## 準備

### ライブラリのインストール

```
pip install Flask-Login Flask-WTF scrypt
```

### ソースコード

これらのライブラリを使用するために，ソースコード上方に次の記述が必要である．

``` python
import flask
from flask import Flask, redirect, url_for, request, render_template, \
    flash, abort, make_response
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import scrypt
from flask_wtf.csrf import CSRFProtect
```

### 配布ファイル

このセクションの[配布ファイル](auth.zip) を展開する．
また，<a href="dbe2_3.sql" download>dbe2_3.sql</a> を MySQL にインポートする．


## ウェブアプリケーションでの利用者認証

ウェブアプリケーションでユーザ認証やその他のセキュリティに関しては，
考慮しなくてはいけないことが非常に多い．
ここでは，そのほんのわずかな部分だけを説明する．
興味のあるものは，たとえば次の書籍などで勉強すると良い: 

* 徳丸浩「体系的に学ぶ 安全なWebアプリケーションの作り方 第2版」
(SBクリエイティブ)

### 例題

配布ファイルを展開し，bad_auth.py を起動し，
http://localhost:8088/ にアクセスする．
以下の2人のユーザが登録されている．

* ユーザ名: user01, パスワード: password01，実名: 赤間一郎
* ユーザ名: user02, パスワード: password02, 実名: 岩瀬春子

どちらでも良いのでログインし，一通りのリンクを追ってみてほしい．
データベースに「秘密の情報」が格納してあり，パスワードを知っている
本人だけが，その情報を見られる，という設定である．

提供されているソースコード `bad_auth.py` 
および各種テンプレートファイルを読み，
どのように機能が実現されているかを把握してほしい．

{% exc seq="17-1" %}

この実装 bad_auth.py にはいくつかの問題点がある．それらを指摘せよ．

{% /exc %}

以下で，この練習問題の解答を行う．

### アクセス手順

実装 `bad_auth.py` の最大の問題点は，
___パスワード認証が全く機能していない___
点である．
試みに，ログインしていない状態でブラウザのアドレスバーで，
次のように入力してみられたい: 
http://localhost:8088/secret?username=user01 ．
これで，user01 の秘密情報が画面に表示されたであろう．
つまり，パスワードを知らなくても，秘密情報を読めてしまうわけだ．

重要な教訓は，利用者は，特に悪意のある利用者は，
__アプリケーション設計者が考えた手順でアクセスしてくるとは限らない__，
ということである．
これは，ウェブアプリケーションを作成するときに，
常に注意しなければならない．この例では，GET メソッドであったので
特に簡単にアクセスできてしまったが，
POST メソッドにしたところで話は同じである．利用者がどのような
手順でアクセスしようと，パスワードを知らない限り，
認証が必要な情報にはアクセスできないようにしなければならない．

### パスワードの保持方法

もう一つの大きな問題点は，パスワードの保持方法である．
bad_auth.py を見てもわかるし，dbe2_3.sql ファイルを見てもわかるが，
__パスワードそのものが，データベースに保存されている．
これは，決して行ってはならない__ ことである．

どのように堅牢なアプリケーションを作ったとしても，
情報の流出の機会を0にすることはできない．
データベースの内容が流出したときに，
そこにパスワード情報が含まれていては致命的である．
利用者が同じパスワードを使い回していたら，被害がどこまで広がるかわからない．

この問題を避けるために，データベースに格納する情報は，
パスワードそのものではなく，パスワードから計算される値にしなければならない．
詳細はここでは説明しないので，前掲の参考書などを読むことを勧める．

Python では，scrypt モジュールが提供する，hashpw という関数を用いて
ハッシュ化した値を格納する．


### エラー表示

細かいことだが，パスワード関係のエラーはあまり細かく表示してはいけない．
ユーザ名のエラーメッセージとパスワードのエラーメッセージを変えてしまうと，
後者が表示されたとき，「ユーザ名は正しい」という情報が伝わってしまう．
どちらも同じエラーメッセージ 「ユーザ名またはパスワードが正しくありません」
などにするべきである．

パスワードを平文で画面に出すなど，論外である．

## 例題のコードの説明

auth.py では，上の2つの問題に対処している．

### FlaskLogin ライブラリ

ユーザ認証機能は，FlaskLogin ライブラリに実装されている．
スクリプト先頭で必要なメソッドをインポートする．
パスワード照合に使うライブラリ scrypt もインポートしておく．

```python
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import scrypt
```

ログインマネージャなる機能を立ち上げる．

```python
login_manager = LoginManager()
login_manager.init_app(app)
```

ユーザを表すクラス `User` を定義する．
クラス機能については，この講義でも各論IIでも扱わない．
興味のある者は調べると良い．
(きょうびのプログラミング言語でクラスを扱わないものは少ないので，
勉強する価値はある．言語間の差は大きいが...)

```python
class User(UserMixin):
    def __init__(self, username, realname):
        self.username = username
        self.realname = realname
    def __repr__(self):
        return f'User({self.username})'
    def get_id(self):
        return self.username
```

`User` というクラスは，`UserMixin` というクラスを継承して
作成することになっている．
ここでは，User クラスに，username と realname を持たせるように設計した．
`__init__` という名前のメソッドは必ず定義する必要がある．
メソッドの第1引数は，self という名前をつける慣習で，これが
クラスのオブジェクトを表す．持たせたい情報を引数に指定し，
これらをオブジェクトの属性として設定する．

他の 2つのメソッド `__repr__` と `get_id` は，このように書いておけば良い．

`load_user` という関数を定義することになっている．
これは，前述の `get_id` メソッドが返す値を引数に与えられると，
User オブジェクトを復元するメソッドである．

```python
@login_manager.user_loader
def load_user(username):
    with connect_db() as cursor:
        sql = 'SELECT realname FROM userInfo WHERE username = %s'
        cursor.execute(sql, [username])
        for c in cursor:
            return User(username, c[0])
        return None
```

ログインしていないユーザが，ログインしなければ見られないページに
アクセスしたときのエラーメッセージを定義できる:

```python
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login_required.html')
```

これだけの準備をした上で，ログインしているときにしかアクセスさせない
ページについて，`@app.route` の次の行に
`@login_required` を指定する．すると，ログインしていない場合には
前述のエラーページに飛ばされることになる．

```python
@app.route('/secret')
@login_required
def func_secret():
    ....
```

### パスワードの照合

テーブル userInfo には，パスワードに関して，2つのフィールド
hashed と salt が定義されている．どちらも型は `VARCHAR(100)` である．

今回のコードには書かれていないが，パスワード文字列 password から，
hashed と salt は，次のように作成できる．
(正確に言うと，salt はランダム文字列として作成され，password と
salt から hashed が生成される)

```python
    import os
    from base64 import b64encode, b64decode

    bin_salt = os.urandom(64)
    bin_hashed = scrypt.hash(password.encode(), bin_salt)
    salt = b64encode(bin_salt)
    hashed = b64encode(bin_hashed)
```

このようにして生成した値が，テーブル userInfo に格納されている．
データベースの userInfo テーブルに格納されている hashed の値をみて，
それが，ユーザの指定したパスワードと似ても似つかないものであることを
確認してほしい．

パスワードの照合は，次のように行われている:

```python
        sql = 'SELECT hashed, salt, realname FROM userInfo WHERE username = %s'
        cursor.execute(sql, [username])
        hashed = None
        for c in cursor:
            (hashed, salt, realname) = c
```

この部分で，userInfo テーブルから，hashed と salt を取得して，
同じ名前の変数に設定を行っている．

```python
        if hashed is not None:
            bin_salt = b64decode(salt)
            bin_hashed = b64decode(hashed)
            if scrypt.hash(password.encode(), bin_salt) == bin_hashed:
                login_user(User(username, realname))
                return redirect('/welcome')
```

取得できた場合には，パスワードを作成したときと同じ方法でハッシュ値を生成し，
userInfo テーブルに格納されていたハッシュ値と比較する．
(encode, decode, b64decode, b64encode については，別項で説明する)
同じハッシュ値が生成された場合には，パスワード照合に成功したことになる．

{% exc seq="17-2" %}

新しいユーザを1つ追加して，自分でパスワードを設定せよ．
(phpMyAdmin などを使って，userInfo テーブルを直接編集する．)
そのユーザでログインができることを確認せよ．

{% /exc %}

{% exc seq="17-3" %}

トップページに「ユーザ登録」というリンクを追加し，以下を実現せよ．

* そのリンクをクリックすると，「ユーザ登録」というページが表示され，
  希望するユーザ名とパスワードが入力できる．
* そのページにある「登録」というボタンを押すと，そのユーザ名でデータベース上に1レコードが追加され，
  以降，登録したユーザ名とパスワードでログインができるようになる．
* すでに存在するユーザ名を登録しようとしたらエラーになる．

{% /exc %}


### CSRF

ログイン機能を作成するときには，
cross-site request forgery (CSRF) という攻撃に対する備えをしておくべきである．
CSRFについてはここでは説明しない．前掲参考書を参照．

Flask-WTF ライブラリに CSRF 防御機能が実装されているので，まず
インポートする:

```python3
from flask_wtf.csrf import CSRFProtect
```

機能を使用するためには秘密鍵を設定する必要がある．

```python
app.secret_key = 'c419e9be86cf484f9967a3b3e2b89850'
csrf = CSRFProtect(app)
```

上のようなランダムな文字列は，Jupyter Notebook で，
たとえば次のようにすれば作成できる:

```python
import os
os.urandom(12).hex()
```

この準備のもとで，フォームに次の記述を置く．
ユーザ名・パスワードを入力するフォームだけでなく，
すべてのフォームに書いておくことが望ましい．

```html
      <input type="hidden" name="csrf_token" value="{ csrf_token() }" />
```


