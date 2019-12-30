function getTimeAgo(timeString, spanId) {
    var timeStamp = new Date(timeString);
    var now = new Date();
    var offset = now.getTimezoneOffset() * 60000;

    let stamp = '';

    var secondsPast = (now.getTime() - (timeStamp.getTime() - offset)) / 1000;
    if (secondsPast < 60) {
        stamp = (parseInt(secondsPast) + 's');
    }
    else if (secondsPast < 3600) {
        stamp = (parseInt(secondsPast / 60) + 'm');
    }
    else if (secondsPast <= 86400) {
        stamp = (parseInt(secondsPast / 3600) + 'h');
    }
    else if (secondsPast <= 604800) {
        stamp = (parseInt(secondsPast / 86400) + 'd');
    }
    else if (secondsPast > 604800) {
        day = timeStamp.getDate();
        month = timeStamp.toDateString().match(/ [a-zA-Z]*/)[0].replace(" ", "");
        year = timeStamp.getFullYear() == now.getFullYear() ? "" : " " + timeStamp.getFullYear();
        stamp = (day + " " + month + year);
    }

    document.getElementById(spanId).innerHTML = stamp;
}

function refreshPost()
{
    var post = $.post( '/post-refresh', { postid: postid } );
        post.done(function( data ) {
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
    
    let url = '/post/'+post_id+'/comment';
    let form = '#comment'+post_id;
    let content = $(form).serialize();
    
    var res = $.post( url , content);
    res.done(function( data ) {
        refreshPost();
    });
}
