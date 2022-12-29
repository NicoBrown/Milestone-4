var words = ['Friends', 'Family', 'Anyone'],
    part,
    i = 0,
    offset = 0,
    len = words.length,
    forwards = true,
    skip_count = 0,
    skip_delay = 20,
    speed = 90;

var wordflick = function () {
    setInterval(function () {
        if (forwards) {
            if (offset >= words[i].length) {
                ++skip_count;
                if (skip_count == skip_delay) {
                    forwards = false;
                    skip_count = 0;
                }
            }
        } else {
            if (offset == 0) {
                forwards = true;
                i++;
                offset = 0;
                if (i >= len) {
                    i = 0;
                }
            }
        }
        part = words[i].substring(0, offset);
        if (skip_count == 0) {
            if (forwards) {
                offset++;
            } else {
                offset--;
            }
        }
        $('.word').text(part);
    }, speed);
};

document.onload = function () {

    // Check for click events on the navbar burger icon
    document.getElementsByClassName("navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        document.getElementsByClassName("navbar-burger").toggleClass("is-active");
        document.getElementsByClassName("navbar-menu").toggleClass("is-active");

    });

    toast = document.getElementsByClassName(".toast");
    toast.show();

    var rellaxH = new Rellax('.rellax', {
        horizontal: true
    });

    wordflick();
};