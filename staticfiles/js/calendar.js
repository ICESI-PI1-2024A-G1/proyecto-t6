document.addEventListener('DOMContentLoaded', function() {

    let request_calendar = "donde salen los eventos"
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth'
    });
    calendar.render();
  });