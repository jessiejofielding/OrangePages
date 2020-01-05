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

// liking
var likingPost = false;
function toggleLike(post_id) {
    let url = '/post/'+post_id+'/like';
    
    if(!likingPost) {
        likingPost = true;
        var res = $.get( url );
        res.done(function( data ) {
            refreshPostId(post_id);
            likingPost = false;
        });
    }

}

// commenting
var postingComment = false;
function postComment(post_id) {

    // Prevent empty comment
    let txt = '#comment-txt'+post_id;
    txt = $(txt).val().trim();
    if(txt == '') return false;

    let url = '/post/'+post_id+'/comment';
    let form = '#comment'+post_id;
    let content = $(form).serialize();
    
    if(!postingComment) {
        postingComment = true;
        var res = $.post( url , content);
        res.done(function( data ) {
            refreshPostId(post_id);
            postingComment = false;
        });
    }

}

var refreshingPost = false;
function refreshPostId(post_id) {
    if(!refreshingPost) {
       refreshingPost = true;
       let div = '#post'+post_id;
       let p = $.post( '/post-preview-refresh', { postid: post_id } );
        p.done(function( data ) {
            $(div).html(data)
            refreshingPost = false;
        });
    }
}