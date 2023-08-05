// Когда пользователь прокручивает страницу, выполняем myFunction
window.onscroll = function () {
    myFunction()
};

// Получаем шапку
var header = document.getElementById("myHeader");

// Получаем позицию элемента
var sticky = header.offsetTop;

// Добавляем класс sticky, когда шапка достигнет нужной позиции.
// Удаляем класс sticky, когда шапка уйдет с этой позиции.
function myFunction() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
}
