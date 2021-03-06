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

$(document).ready(function() {
    $("#load-new-posts").click(showNewPosts); 
});

// auto refresh
window.onload = setupRefresh;
function setupRefresh()
{
    feedInterval = setInterval(refreshFeed,20000); // 20s
}

function stopRefresh()
{
    clearInterval(feedInterval);
}

// Refresh: update posts currently displayed on feed
// Check: check if there are new posts available to be displayed
var refreshingFeed = false; // sync
var checkingFeed = false; // sync
function refreshFeed()
{
    if(!refreshingFeed) {
        refreshingFeed = true;
        var posts = $.post( '/feed-refresh', { t_first: t_first, t_last: t_last } );
        posts.done(function( data ) {
            if(!data.startsWith("<!DOCTYPE"))
                $('#posts').html(data)
            refreshingFeed = false;
        });
    }
    if(!checkingFeed) {
        checkingFeed = true;
        var newPosts = $.post( '/feed-check', { t_first: t_first, t_last: t_last } );
        newPosts.done(function( data ) {

            if(!data.startsWith("<!DOCTYPE")) {

                let numPosts = parseInt(data);

                if(numPosts > 0) {
                    let txt = 'View ' + numPosts + ' new post'
                    if(numPosts > 1) {
                        txt = txt + 's'
                    }

                    $('#load-new-posts').html(txt)
                }

                $('#load-new-posts').toggle(numPosts > 0)
            }
            
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
            if(!data.startsWith("<!DOCTYPE")) {
                $('#load-new-posts').hide();
                $( "#posts" ).prepend( data );
            }
            
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
            if(!data.startsWith("<!DOCTYPE"))
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
