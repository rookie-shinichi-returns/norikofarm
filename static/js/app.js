document.addEventListener("DOMContentLoaded", () => {
    // HTMLの読み込み完了後に要素を取得する
    const btn = document.getElementById('toggleBtn');
    const form = document.getElementById('formContent');

    // form,btnが存在することを確認してから処理する
    if (form && btn) {
        // 初期状態のチェック（非表示でなければ、非表示にしてボタン文字を変える
        if (form.style.display !== 'none') {
            alert("フォームが開いています");
            form.style.display = 'none';
            btn.textContent = "作業フォームを開く";
        }
    }

    btn.addEventListener('click', () => {
        if (form.style.display === 'block') {
            form.style.display = 'none';
            btn.textContent = "フォームを開く";
        } else {
            form.style.display = 'block';
            btn.textContent = "フォームを閉じる";
        }
    });
});