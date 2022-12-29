document.onload = function () {

    // Check for click events on the navbar burger icon
    document.getElementsByClassName(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        document.getElementsByClassName(".navbar-burger").toggleClass("is-active");
        document.getElementsByClassName(".navbar-menu").toggleClass("is-active");

    });
};