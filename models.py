import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

db = None

def init_db():
    global db
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
            # ※ファイル名が以前と違う場合はここを修正してください
            cred_path = os.path.join(os.path.dirname(__file__), 'firebase-key.json')
            cred = credentials.Certificate(cred_path)
            
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()

# --- 保存する機能 ---
def add_book(title, author, rating, memo, date_read, source):
    books_ref = db.collection('books')
    # ここで保存するラベル名（キー）を固定します
    books_ref.add({
        'title': title,
        'author': author,
        'rating': rating,
        'memo': memo,
        'date_read': date_read,
        'source': source
    })

# --- 取り出す機能 ---
def get_books():
    books_ref = db.collection('books')
    
    # .order_by('date_read', direction='DESCENDING') を追加して、日付の新しい順に並べ替えます
    docs = books_ref.order_by('date_read', direction='DESCENDING').stream()
    
    book_list = []
    for doc in docs:
        b = doc.to_dict()
        book_list.append([
            doc.id,
            b.get('title', 'タイトルなし'),
            b.get('author', '不明'),
            b.get('rating', 0),
            b.get('memo', ''),
            b.get('date_read', '未入力'),
            b.get('source', '未記入')
        ])
    return book_list

# --- 削除する機能 ---
def delete_book(book_id):
    # ドキュメントIDを指定して削除を実行
    db.collection('books').document(book_id).delete()
    
    
