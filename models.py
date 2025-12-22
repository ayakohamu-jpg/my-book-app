import firebase_admin
from firebase_admin import credentials, firestore
import os

# 1. 鍵ファイルの「絶対パス（確実な住所）」を作る
# これにより、Render上でもファイルがどこにあるか迷わなくなります
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, 'firebase-key.json')

# 2. Firebaseの初期化（二重に初期化しないようにチェックを入れる）
if not firebase_admin._apps:
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        # もしファイルが見つからない場合はエラーをログに出す
        print(f"CRITICAL ERROR: Firebase key file NOT FOUND at: {cred_path}")

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
    
