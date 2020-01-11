

function refreshPost()
{
    var post = $.post( '/post-refresh', { postid: postid } );
        post.done(function( data ) {
            if(!data.startsWith("<!DOCTYPE"))
                $('#post').html(data)
        });
}

// liking from post page
// TODO: separate this out of feed js
function toggleLikePost(post_id) {
    
    let url = '/post/'+post_id+'/like';
       
    var res = $.get( url );
    res.done(function( data ) {
        refreshPost();
    });
}

// commenting from post page
function postCommentPost(post_id) {
    let txt = $('#comment-input').val().trim();
    if(txt == '') return false;
    
    let url = '/post/'+post_id+'/comment';
    let form = '#comment'+post_id;
    let content = $(form).serialize();
    
    var res = $.post( url , content);
    res.done(function( data ) {
        refreshPost();
    });
}