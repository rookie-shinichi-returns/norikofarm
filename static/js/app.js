var roses = [
    {src: '/media/image/22760162.jpg', name: 'バックトゥザフューチャー'},
    {src: '/media/image/ice09m.jpg', name: 'アイスバーグ'},
    {src: '/media/image/img_20221119_084441.jpg', name: 'カトレア1'},
    {src: '/media/image/img_20230113_154601.jpg', name: 'カトレア2'}
];

var roseImage = document.createElement('img');
roseImage.setAttribute('src', roses[0].src);
roseImage.setAttribute('alt', roses[0].name);
var roseName = document.createElement('p');
roseName.innerText = roseImage.alt;
var rosesFlame = document.querySelector('.card-body h5');
rosesFlame.insertBefore(roseImage, null);
rosesFlame.insertBefore(roseName, null);

for (var i = 0; i < roses.length; i++) {
    var thumbImage = document.createElement('img');
    thumbImage.setAttribute('src', roses[i].src);
    thumbImage.setAttribute('alt', roses[i].name);
    var thumbFlame = document.querySelector('.card-body .bottom');
    thumbFlame.insertBefore(thumbImage, null);
}

thumbFlame.addEventListener('click', function(event) {
    if (event.target.src) {
        roseImage.src = event.target.src;
        roseName.innerText = event.target.alt;
    }
});


