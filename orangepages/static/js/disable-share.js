$(document).ready(function () {
    $('.field textarea').on('keyup', function () {
        let empty = false;
        var str = document.querySelector('.field textarea').value.trim();

        $('.field textarea').each(function () {
            empty = str.length <= 0;
        });

        if (empty)
            $('.field button').attr('disabled', 'disabled');
        else
            $('.field button').attr('disabled', false);
    });

    $('.field textarea').on('keydown', function () {
        let empty = false;
        var str = document.querySelector('.field textarea').value.trim();

        $('.field textarea').each(function () {
            empty = str.length <= 0;
        });

        if (empty)
            $('.field button').attr('disabled', 'disabled');
        else
            $('.field button').attr('disabled', false);
    });
});