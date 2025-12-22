// 1. 保存する関数
async function saveBook() {
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const rating = document.getElementById('rating').value;
    const memo = document.getElementById('memo').value;
    const date_read = document.getElementById('date_read').value;
    const source = document.getElementById('source').value;

    if (!title) {
        alert("本のタイトルを入力してください！");
        return;
    }

    // Flaskの /add_book にデータを送る
    const response = await fetch('/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            author: author,
            rating: rating,
            memo: memo,
            date_read: date_read,
            source: source
        })
    });

    if (response.ok) {
        // 入力欄をクリア
        document.getElementById('title').value = "";
        document.getElementById('author').value = "";
        document.getElementById('memo').value = "";
        document.getElementById('date_read').value = "";
        document.getElementById('source').value = "";

        alert("保存しました！");
        displayBooks();
    } else {
        alert("保存に失敗しました。");
    }
}

// 2. 表示する関数
async function displayBooks() {
    // Flaskの /get_books からデータを取得
    const response = await fetch('/get_books');
    const books = await response.json();

    const bookListDiv = document.getElementById('bookList');
    bookListDiv.innerHTML = ""; 

    books.forEach(book => {
        const bookItem = document.createElement('div');
        bookItem.className = 'book-item';
        
        const displayDate = book.date_read ? book.date_read : "未入力";
        const displaySource = book.source ? book.source : "未記入";

        bookItem.innerHTML = `
            <h3>${book.title}</h3>
            <p>著者: ${book.author}</p>
            <p>入手経路: ${displaySource}</p>
            <p>読了日: ${displayDate}</p>
            <p>評価: ${"★".repeat(book.rating)}</p>
            <p>感想: ${book.memo}</p>
            <button onclick="deleteBook(${book.id})" style="background-color: #e57373; margin-top: 10px;">この記録を消す</button>
            <hr>
        `;
        bookListDiv.appendChild(bookItem);
    });
}

// 本を削除する関数
async function deleteBook(id) {
    if (!confirm('本当にこの記録を消してもよろしいですか？')) return;

    // サーバーの /delete/ID という住所に「消して！」とリクエストを送る
    const response = await fetch(`/delete/${id}`, {
        method: 'POST'
    });

    if (response.ok) {
        // 消せたら画面を更新する
        loadBooks();
    } else {
        alert('削除に失敗しました。');
    }
}

// アプリ起動時に表示
displayBooks();
