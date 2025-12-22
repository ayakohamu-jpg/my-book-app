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
    db.collection('books').add({
        'title': title,
        'author': author,
        'rating': int(rating),
        'memo': memo,
        'date_read': date_read,
        'source': source,
        'created_at': firestore.SERVER_TIMESTAMP
    })

def get_books():
    # 'created_at' が存在しない古いデータがあるとエラーになるのを防ぐためシンプルに取得
    docs = db.collection('books').stream()
    
    book_list = []
    for doc in docs:
        b = doc.to_dict()
        book_list.append([
            doc.id, b.get('title'), b.get('author'), 
            b.get('rating'), b.get('memo'), b.get('date_read'), b.get('source')
        ])
    return book_list

def delete_book(book_id):
    db.collection('books').document(book_id).delete()
    
