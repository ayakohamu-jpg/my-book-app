from flask import Flask, render_template, request, jsonify
import models

app = Flask(__name__, template_folder='web', static_folder='web', static_url_path='')

# データベース初期化
models.init_db()

# メイン画面を表示
@app.route('/')
def index():
    return render_template('index.html')

# 1. 保存する機能（ここを修正しました）
@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        # JavaScriptから届いたデータをmodels.pyのadd_book関数に渡します
        models.add_book(
            data.get('title'),
            data.get('author'),
            data.get('rating'),
            data.get('memo'),
            data.get('date_read'),
            data.get('source')
        )
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"保存エラー: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. データを取り出す機能
@app.route('/get_books')
def get_books():
    # models.get_books() から返ってくるリストをそのままJavaScriptに送ります
    books = models.get_books()
    return jsonify(books)

# 3. 削除する機能
@app.route('/delete_book', methods=['POST'])
def delete_book():
    try:
        data = request.get_json()
        book_id = data.get('id')
        print(f"削除要請を受け取りました: ID={book_id}")
        
        if book_id:
            models.delete_book(book_id)
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "IDが空です"}), 400
    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# アプリの起動設定
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    