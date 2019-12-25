function getTimeAgo(timeString) {
    var timeStamp = new Date(timeString);
    var now = new Date();
    var offset = now.getTimezoneOffset() * 60000;
    console.log(timeStamp)
    console.log(now)
    console.log(offset)
    var secondsPast = (now.getTime() - (timeStamp.getTime() - offset)) / 1000;
    if (secondsPast < 60) {
        document.write(parseInt(secondsPast) + 's');
        return;
    }
    if (secondsPast < 3600) {
        document.write(parseInt(secondsPast / 60) + 'm');
        return;
    }
    if (secondsPast <= 86400) {
        document.write(parseInt(secondsPast / 3600) + 'h');
        return;
    }
    if (secondsPast <= 604800) {
        document.write(parseInt(secondsPast / 86400) + 'd');
        return;
    }
    if (secondsPast > 604800) {
        day = timeStamp.getDate();
        month = timeStamp.toDateString().match(/ [a-zA-Z]*/)[0].replace(" ", "");
        year = timeStamp.getFullYear() == now.getFullYear() ? "" : " " + timeStamp.getFullYear();
        document.write(day + " " + month + year);
    }
}

window.onload = setupRefresh;
function setupRefresh()
{
    setInterval(refreshBlock,10000);
}

function refreshBlock()
{
   $('#posts').load("feed #posts");
}
