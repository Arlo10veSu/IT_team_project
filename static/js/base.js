//移动框体，测试中...
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
title.addEventListener('mousedown', function (e) {
    var x = e.pageX - login.offsetLeft;
    var y = e.pageY - login.offsetTop;
    document.addEventListener('mousemove', move)
    function move(e) {
        login.style.left = e.pageX - x + 'px';
        login.style.top = e.pageY - y + 'px';
    }
    document.addEventListener('mouseup', function () {
        document.removeEventListener('mousemove', move);
    })
})

//发布评论
var text = document.querySelector('textarea');
link.addEventListener('click', function () {
    text.value = '';
})
var ul = document.querySelector('.ul');
var send = document.querySelector('#send');
send.addEventListener('click', function () {
    if (text.value === '') {
        alert('You have not input anything.');
        return false;
    } else {
        var li = document.createElement('li');
        li.innerHTML = text.value + "</br>";
        ul.insertBefore(li, ul.children[0]);
    }
    mask.style.display = 'none';
    login.style.display = 'none';
})
