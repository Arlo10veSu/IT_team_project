// this method is to create a inner html to write the comment sections.

var login = document.querySelector('.login');
var mask = document.querySelector('.login-bg');
var link = document.querySelector('#link');
var closeBtn = document.querySelector('#closeBtn');
var title = document.querySelector('#title');
link.addEventListener('click', function () {
    mask.style.display = 'block';
    login.style.display = 'block';
})
closeBtn.addEventListener('click', function () {
    mask.style.display = 'none';
    login.style.display = 'none';
})

var text = document.querySelector('textarea');
link.addEventListener('click', function () {
    text.value = '';
})
var ul = document.querySelector('.ul');
var send = document.querySelector('#send');
