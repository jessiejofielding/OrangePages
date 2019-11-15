$('.hidden').removeClass('hidden').hide();
$('.toggle-text').click(function () {
    $(this).find('span').each(function () { $(this).toggle(); });
});