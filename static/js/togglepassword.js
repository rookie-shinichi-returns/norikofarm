const togglePassword = document.getElementById("toggle-password");
const passwordInput = document.getElementById("id_password");

togglePassword.addEventListener("change", function() {
    if (this.checked) {
        // チェックが入ったらテキスト表示
        passwordInput.type = "text";
    } else {
        // チェックが外れたら伏せ文字に戻す
        passwordInput.type = "password";
    }
})