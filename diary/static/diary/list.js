window.diary = {};
window.diary.initialize = function () {
    $('.caret').on('click', function () {
        $(this).siblings('ul').toggle();
        $(this).toggleClass('caret-down');
    });
}
$(document).ready(function () {
    window.diary.initialize();
});