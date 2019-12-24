$(document).ready(function () {
    $('.field textarea').on('keyup', function () {
        let empty = false;

        $('.field textarea').each(function () {
            empty = ($(this).val().length) <= 0;
        });

        if (empty)
            $('.field button').attr('disabled', 'disabled');
        else
            $('.field button').attr('disabled', false);
    });

    $('.field textarea').on('keydown', function () {
        let empty = false;

        $('.field textarea').each(function () {
            empty = ($(this).val().length) <= 0;
        });

        if (empty)
            $('.field button').attr('disabled', 'disabled');
        else
            $('.field button').attr('disabled', false);
    });
});