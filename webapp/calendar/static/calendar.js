$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultDate: new Date().toISOString().substring(0, 10),
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: {
            url: 'data',
            error: function() {
                $('#script-warning').show();
            }
        },
        loading: function(bool) {
            $('#loading').toggle(bool);
        }
    });
});
