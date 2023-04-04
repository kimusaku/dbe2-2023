+++
title = "模擬図書館アプリケーション"
description = ""
weight = 1
alwaysopen = true
+++


* [アプリケーション](manage_lib.zip)
* <a href="dbe2_3.sql" download>データベースDBE2</a>を初期状態にする．

## アプリケーション

[manage_lib.zip](manage_lib.zip) を展開し，
トップディレクトリにある flask スクリプト mlib.py を実行し，
http://localhost:8088/ にアクセスすれば使用できる．

## 利用している機能

### 静的ファイル

静的ファイル (画像ファイル，JavaScriptファイル，
スタイルシートファイルなどの加工する必要のないファイル) は，
static という名前のサブディレクトリを作成して，その下に置く．
(さらにサブディレクトリを作成しても良い．)
トップページなど，テンプレート機能を必要としない HTML ファイルについても，
この機能を利用することができる．

URL としても，/static から始まるパス名を書けば，このファイルの内容が
取得できる．
[http://localhost:8088/static/html/example.html](http://localhost:8088/static/html/example.html) にアクセスしてみよ

### リダイレクト

アクセスされたときにHTMLページを組み立てることなく，
別のURLの内容をブラウザに表示させることができる．
これを，リダイレクト (redirect) と呼ぶ．
redirect という関数が，この機能を実現する．

下のコードによって，
[http://localhost:8088/](http://localhost:8088/) にアクセスされたときに，
[http://localhost:8088/static/html/top.html](http://localhost:8088/static/html/top.html) の内容を返すようにすることができる．

```python
@app.route('/')
def func_root():
    return redirect('/static/html/top.html')
```

### GET アクセスのパラメタの取得

Form でユーザが入力した値は，`request.form` という
辞書 (のようなもの) で取得できるのであった．

これと似た内容として，URL のパラメタがある．
例として以下のHTMLタグを考える:

`<a href="http://localhost:8088/action1?key1=value1&key2=value2&key3=value3">`

このようなURLにおいて，疑問符 (`?`) 以降がパラメタである．
パラメタはキーと値からなり，その間は等号 (`=`) で区切られている．
また，パラメタどうしは，アンパサンド (`&`) で区切られている．
上の例では，次の3つのパラメタがあることになる．

* キーが key1，値が value1
* キーが key2，値が value2
* キーが key3，値が value3

上の a タグがユーザによってクリックされると，ウェブサーバ (flaskスクリプト)
には，GET メソッドによってアクセスが行われる．
(Form では通常 POST メソッドでアクセスされるのであった)

パラメタが異なったとしても，flask スクリプトでは，同じ 
`@app.route('/action1')` に対応する関数が呼び出される．
このように GET メソッドでアクセスされた場合には，パラメタの値は
`request.form` ではなく，
`request.args` という辞書 (のようなもの) で取得できる．

したがって，同じアクションを GET と POST の両方に対応させたい場合には，
次のように書くと良い:

```python
@app.route('/...', methods=['GET', 'POST'])
def func_...():
    if request.method == 'POST':
        req = request.form
    else:       # この場合には GET メソッド
        req = request.args
    foo = req.get('foo')
    bar = req.getlist('bar')
    ....
```

### LIKE 述語

SQL の LIKE述語を使用する際には，注意が必要である．
たとえば「`abc`を含む文字列」を検索しようとするときには，
`WHERE field1 LIKE '%abc%'` という WHERE 句を書きたい．
この `%` 記号が，
`cursor.execute` メソッドでは「プレースホルダを示す」
という特殊な意味を持っているので，このままでは動作しない．
`WHERE field1 LIKE '%%abc%%'` と，`%` を重ねて指定する必要がある．

また，通常，`abc` の部分は，ユーザがブラウザで入力した値であろう．
この際には，SQL 文は，`WHERE field1 LIKE %s` のように，プレースホルダーを
使用して書き，`cursor.execute` の第2引数のリストに，
`%abc%` という文字列が入るようにすれば良い．下のようなコードに
なるであろう．

```python
def func_xxxx():
    req = request.form
    user_input = req.get('xxxxx')
    with connect_db() as cursor:
        sql = 'SELECT ... WHERE field1 LIKE %s'
        value = f'%{user_input}%'
        cursor.execute(sql, [value])
```



{% exc seq="19-1" %}

このアプリケーションは，まだまだ書きかけである．適当な機能を実装してみよ．
下に例を示す．

* 利用者情報
  * 氏名完全一致による表示の実装
  * 他のフィールドでも検索できるようにする
* 利用者詳細情報画面
  * 他のフィールドの値も表示する．
  * 現在，この利用者が借りている書籍の一覧を表示する．
  * 登録画像がないときには，「(写真無し)」と表示する．
    または，特定の "no photo" イメージを表示する．
* 利用者検索結果一覧画面
  * 他のフィールドの値も表示する．
  * 検索結果がn件を超えるときには，最初のn件だけ表示して，「次」「前」
    のボタンを置く．
* 貸出手続き
  * 該当の本がすでに貸し出されている場合，エラーを報告する．
  * 日付の形式の妥当性をチェックし，必要ならエラーにする．
    * 形式が不当
    * 貸出日と返却予定日の前後関係
  * 未返却の本があっても，n冊までは貸し出せるようにする．
    * 貸出期限を超えて未返却の本がある場合には不可．
      (今日の日付を入力できるようにする．)
    * 利用者区分によって，nを変えられるようにする．
      例えば，市内居住者は5冊，
      市外居住者は2冊，など．利用者区分をデータベースに追加する必要が
      ある．
  * 返却予定日を入力させず，代わりに，貸出日の2週間後の日付を自動的に
    用いるようにする．
* 書籍情報を実装する．
* 返却手続きを実装する．

{% /exc %}


