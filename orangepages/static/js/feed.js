function getTimeAgo(timeString) {
    var timeStamp = new Date(timeString + new Date().getTimezoneOffset());
    console.log(timeStamp)
    var date = new Date();
    console.log(date)
    var now_utc = Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),
        date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
    var now = new Date(now_utc)
    var secondsPast = (now.getTime() - timeStamp.getTime()) / 1000;
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
