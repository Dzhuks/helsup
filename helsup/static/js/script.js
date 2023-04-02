const form = document.getElementById('theform');
const popup_button = document.querySelector('#createQuery');

popup_button.addEventListener('click', () => {
    form.classList.toggle('popup__form_active');
})

