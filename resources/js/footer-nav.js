$(document).ready(function() {
    var currentUrl = $(location).attr('href');
    currentUrl = currentUrl.split("=");
    currentProject = currentUrl[1];
    console.log(currentProject);
    $('#' + currentProject).addClass("footer-current-project");
});