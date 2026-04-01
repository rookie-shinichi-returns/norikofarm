const btn = document.getElementById('toggleBtn');
const form = document.getElementById('formContent');

btn.addEventListener('click', () => {
    if (form.style.display === 'block') {
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
    }
});