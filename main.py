from flask import Flask, render_template, request, jsonify
import models

app = Flask(__name__, template_folder='web', static_folder='web', static_url_path='')

# データベース初期化
models.init_db()

# メイン画面を表示
@app.route('/')
def index():
    return render_template('index.html')

# 保存する機能
@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.json
    models.add_book(
        data['title'], data['author'], data['rating'], 
        data['memo'], data['date_read'], data['source']
    )
    return jsonify({"status": "success"})

# データを取り出す機能
@app.route('/get_books')
def get_books():
    books = models.get_books()
    book_list = []
    for b in books:
        book_list.append({
            "id": b[0], "title": b[1], "author": b[2],
            "rating": b[3], "memo": b[4], "date_read": b[5], "source": b[6]
        })
    return jsonify(book_list)

# 削除する機能
@app.route('/delete_book', methods=['POST'])
def delete_book():
    data = request.json
    models.delete_book(data['id'])
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # host='0.0.0.0' を追加することで、Renderの外側からのアクセスを許可します
    # port は Render が指定する数字を自動で使うように設定します
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    
