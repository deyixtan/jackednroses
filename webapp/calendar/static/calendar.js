$(document).ready(function() {
    $("#calendar").fullCalendar({
        header: {
            left: "prev,next today",
            center: "title",
            right: "month,agendaWeek,agendaDay"
        },
        editable: false,
        eventLimit: true,
        events: {
            url: "data",
            error: function() {
                $("#script-warning").show();
            }
        },
        loading: function(bool) {
            $("#loading").toggle(bool);
        }
    });
});
