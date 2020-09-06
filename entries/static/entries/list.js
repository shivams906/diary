window.Entries = {}
window.Entries.initialize = function () {
    $('.box').on('click', function () {
        $(this).siblings('ul').toggle();
    });
}
$(document).ready(function () {
    window.Entries.initialize();
})