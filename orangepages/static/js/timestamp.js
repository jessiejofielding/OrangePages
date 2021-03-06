function getTimeAgo(timeString, spanId) {
    timeString=timeString.replace(/\s/, 'T'); // safari
    var timeStamp = new Date(timeString);
    var now = new Date();
    var offset = now.getTimezoneOffset() * 60000;

    let stamp = '';

    var secondsPast = (now.getTime() - (timeStamp.getTime() - offset)) / 1000;
    if (secondsPast < 0) {
        secondsPast = 0;
    }
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

    spanId = '#'+spanId;
    $(spanId).text(stamp);
}