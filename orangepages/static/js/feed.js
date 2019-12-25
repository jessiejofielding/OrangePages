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

window.onload = setupRefresh;
function setupRefresh()
{
    setInterval(refreshFeed,13000);
}


function refreshFeed()
{
   // $('#posts').load("feed #posts");
   $.ajax({
        url: '/feed',
        success: function(response) {
            data = $(response).find('#posts');
            $('#posts').html(data);
        }
    });
}
