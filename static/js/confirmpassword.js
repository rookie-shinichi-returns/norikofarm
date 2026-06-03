// UserCreationFormのID「id_password1」と「id_password2」を取得
    const passwordInput1 = document.getElementById('id_password1');
    const passwordInput2 = document.getElementById('id_password2');
    const toggleCheckbox = document.getElementById('toggle-password');
    
    toggleCheckbox.addEventListener('change', function() {
        if (this.checked) {
            // チェックが入ったら両方テキスト表示にする 
            if(passwordInput1) passwordInput1.type = 'text';
            if(passwordInput2) passwordInput2.type = 'text';
        } else {
            // チェックが外れたら両方伏字に戻す
            if(passwordInput1) passwordInput1.type = 'password';
            if(passwordInput2) passwordInput2.type = 'password';
        }
    });