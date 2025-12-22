import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# 1. Firebaseの初期化（秘密鍵を使って接続する）
# main.pyと同じ場所にある firebase-key.json を読み込みます
cred_path = os.path.join(os.path.dirname(__file__), 'firebase-key.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# 2. データベース（Firestore）を操作する準備
db = firestore.client()

def init_db():
    # Firebaseではテーブル作成の必要がないので、何もしなくてOKです
    pass

def add_book(title, author, rating, memo, date_read, source):
    # 'books' という名前のコレクション（棚）にデータを保存します
    db.collection('books').add({
        'title': title,
        'author': author,
        'rating': int(rating),
        'memo': memo,
        'date_read': date_read,
        'source': source,
        'created_at': firestore.SERVER_TIMESTAMP # 保存した時間を記録
    })

def get_books():
    # 'books' からすべての本を、作成日時が新しい順に取得します
    docs = db.collection('books').order_by('created_at', direction=firestore.Query.DESCENDING).stream()
    
    book_list = []
    for doc in docs:
        b = doc.to_dict()
        # JavaScript側が期待する「ID」として、Firebaseが自動で振ったドキュメントIDを入れます
        book_list.append([
            doc.id, b.get('title'), b.get('author'), 
            b.get('rating'), b.get('memo'), b.get('date_read'), b.get('source')
        ])
    return book_list

def delete_book(book_id):
    # 指定されたIDのドキュメント（本のデータ）を削除します
    db.collection('books').document(book_id).delete()
    
