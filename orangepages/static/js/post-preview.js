
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