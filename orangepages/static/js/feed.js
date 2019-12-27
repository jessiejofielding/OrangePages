// function getTimeAgo(timeString) {
//     var timeStamp = new Date(timeString);
//     var now = new Date();
//     var offset = now.getTimezoneOffset() * 60000;

//     var secondsPast = (now.getTime() - (timeStamp.getTime() - offset)) / 1000;
//     if (secondsPast < 60) {
//         document.write(parseInt(secondsPast) + 's');
//         return;
//     }
//     if (secondsPast < 3600) {
//         document.write(parseInt(secondsPast / 60) + 'm');
//         return;
//     }
//     if (secondsPast <= 86400) {
//         document.write(parseInt(secondsPast / 3600) + 'h');
//         return;
//     }
//     if (secondsPast <= 604800) {
//         document.write(parseInt(secondsPast / 86400) + 'd');
//         return;
//     }
//     if (secondsPast > 604800) {
//         day = timeStamp.getDate();
//         month = timeStamp.toDateString().match(/ [a-zA-Z]*/)[0].replace(" ", "");
//         year = timeStamp.getFullYear() == now.getFullYear() ? "" : " " + timeStamp.getFullYear();
//         document.write(day + " " + month + year);
//     }
// }


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


$(document).ready(function() {
    $("#load-new-posts").click(showNewPosts); 
});


// liking
var likingPost = false;
function toggleLike(post_id) {
    
    let url = '/post/'+post_id+'/like';
    
    if(!likingPost) {
        likingPost = true;
        var res = $.get( url );
        res.done(function( data ) {
            refreshFeed();
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
            refreshFeed();
            postingComment = false;
        });
    }

}

// auto refresh
window.onload = setupRefresh;
function setupRefresh()
{
    setInterval(refreshFeed,20000); // 20s
}

// Don't refresh if a modal is open
var modalOpen = false;

function openModal() { modalOpen = true; }
function closeModal() { modalOpen = false; }

// Refresh: update posts currently displayed on feed
// Check: check if there are new posts available to be displayed
var refreshingFeed = false; // sync
var checkingFeed = false; // sync
function refreshFeed()
{
    if (modalOpen) return;

    if(!refreshingFeed) {
        refreshingFeed = true;
        var posts = $.post( '/feed-refresh', { t_first: t_first, t_last: t_last } );
        posts.done(function( data ) {
            $('#posts').html(data)
            refreshingFeed = false;
        });
    }
    if(!checkingFeed) {
        checkingFeed = true;
        var newPosts = $.post( '/feed-check', { t_first: t_first, t_last: t_last } );
        newPosts.done(function( data ) {

            let numPosts = parseInt(data);

            if(numPosts > 0) {
                let txt = 'View ' + numPosts + ' new post'
                if(numPosts > 1) {
                    txt = txt + 's'
                }

                $('#load-new-posts').html(txt)
            }

            
            $('#load-new-posts').toggle(numPosts > 0)
            checkingFeed = false;
        });
    }
}

// Display new posts
var updatingFeed = false; // sync
function updateFeed()
{
    if(!updatingFeed) {
        updatingFeed = true;
        var newPosts = $.post( '/feed-new', { t_first: t_first, t_last: t_last } );
        newPosts.done(function( data ) {
            $('#load-new-posts').hide();
            $( "#posts" ).prepend( data );
            updatingFeed = false;
        });
    }
}
function showNewPosts() {
    updateFeed();
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth'
    });
}


// Batch fetch older posts

// t_first and t_last global vars are initialized in
// script tag in feed_posts.html

var gettingMoreFeed = false; // sync
function getMoreFeed()
{
    if(!gettingMoreFeed) {
        gettingMoreFeed = true;
        var getMorePosts = $.post( '/feed-next', { t_first: t_first, t_last: t_last } );
        getMorePosts.done(function( data ) {
            $( "#posts" ).append( data );
            gettingMoreFeed = false;
        });
    }
}

$(window).scroll(function() {
    if($(window).scrollTop()+1 >= $(document).height() - $(window).height()) {
           getMoreFeed()
    }
});
