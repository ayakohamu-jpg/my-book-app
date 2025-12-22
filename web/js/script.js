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

    const response = await fetch('/add_book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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
        document.getElementById('title').value = "";
        document.getElementById('author').value = "";
        document.getElementById('memo').value = "";
        document.getElementById('date_read').value = "";
        document.getElementById('source').value = "";

        alert("保存しました！");
        displayBooks(); // 再表示
    } else {
        alert("保存に失敗しました。");
    }
}

// 2. 表示する関数
async function displayBooks() {
    const response = await fetch('/get_books');
    const books = await response.json();

    const bookListDiv = document.getElementById('bookList');
    bookListDiv.innerHTML = ""; 

    books.forEach(book => {
        // Firebaseからのデータはリスト形式 [id, title, author, rating, memo, date, source] で届きます
        const id = book[0];
        const title = book[1];
        const author = book[2];
        const rating = book[3];
        const memo = book[4];
        const date_read = book[5] ? book[5] : "未入力";
        const source = book[6] ? book[6] : "未記入";

        const bookItem = document.createElement('div');
        bookItem.className = 'book-item';
        
        bookItem.innerHTML = `
            <h3>${title}</h3>
            <p>著者: ${author}</p>
            <p>入手経路: ${source}</p>
            <p>読了日: ${date_read}</p>
            <p>評価: ${"★".repeat(rating)}</p>
            <p>感想: ${memo}</p>
            <button onclick="deleteBook('${id}')" style="background-color: #e57373; color: white; border: none; padding: 5px 10px; border-radius: 5px; margin-top: 10px;">この記録を消す</button>
            <hr>
        `;
        bookListDiv.appendChild(bookItem);
    });
}

// 3. 削除する関数
// script.js の deleteBook 関数をこれに書き換えてください
async function deleteBook(id) {
    if (!confirm('本当にこの記録を消してもよろしいですか？')) return;

    // main.py の /delete_book に、JSON形式でIDを送る
    const response = await fetch('/delete_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id }) // ここで 'id' という名前をつけて送る
    });

    if (response.ok) {
        displayBooks(); // 成功したら一覧を更新
    } else {
        alert('削除に失敗しました。');
    }
}

// アプリ起動時に実行
displayBooks();