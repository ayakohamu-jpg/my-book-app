import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Firebaseの初期化
if not firebase_admin._apps:
    # 1. まずは「環境変数（Render上の設定）」から鍵を探す
    firebase_config = os.environ.get("FIREBASE_CONFIG")
    
    if firebase_config:
        # Renderで動いている場合：環境変数のテキストを辞書形式に変換して読み込む
        cred_dict = json.loads(firebase_config)
        cred = credentials.Certificate(cred_dict)
    else:
        # PCでテストしている場合：手元の firebase-key.json ファイルを読み込む
        cred_path = os.path.join(os.path.dirname(__file__), 'firebase-key.json')
        cred = credentials.Certificate(cred_path)
        
    firebase_admin.initialize_app(cred)

db = firestore.client()

def init_db():
    pass

def add_book(title, author, rating, memo, date_read, source):
    books_ref = db.collection('books')
    # ここで「どの名前(キー)で保存するか」をハッキリ指定します
    books_ref.add({
        'title': title,
        'author': author,
        'rating': int(rating),
        'memo': memo,
        'date_read': date_read,
        'source': source
    })

def get_books():
    books_ref = db.collection('books')
    docs = books_ref.stream()
    book_list = []
    for doc in docs:
        b = doc.to_dict()
        
        # どんな名前（titleやbook_titleなど）で保存されていても見つけ出す工夫
        title = b.get('title') or b.get('book_title') or b.get('本の名前') or "タイトルなし"
        author = b.get('author') or b.get('著者') or "不明"
        rating = b.get('rating') or 0
        memo = b.get('memo') or b.get('感想') or ""
        date_read = b.get('date_read') or b.get('読了日') or "未入力"
        source = b.get('source') or b.get('入手経路') or "未記入"

        book_list.append([
            doc.id,
            title,
            author,
            rating,
            memo,
            date_read,
            source
        ])
    return book_list

def delete_book(book_id):
    db.collection('books').document(book_id).delete()
    
