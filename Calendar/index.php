<?php
//index.php

?>
<!DOCTYPE html>
<html>
 <head>
  <title>Appsmatta Calendar</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.4.0/fullcalendar.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.6/css/bootstrap.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.4.0/fullcalendar.min.js"></script>
  <script>
   
  $(document).ready(function() {
   var calendar = $('#calendar').fullCalendar({
    editable:true, 
    slotWidth: 2,
    header:{
     contentHeight: 600,
     left:'prev,next today',
     center:'title',
     //right:'month'//,agendaWeek,agendaDay'
     right: 'month, agendaWeek, prev,next today'
    },
    events: 'load.php',
    selectable:true,
    selectHelper:true,
    contentHeight: 600,
    rendering: 'background',
    backgroundColor: '#ED1317',
    displayEventTime: false,

    select: function(start, end, allDay)
    {
     var title = prompt("Enter Event Title");
     if(title)
     {
      var start = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
      var end = $.fullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");
      $.ajax({
       url:"insert.php",
       type:"POST",
       data:{title:title, start:start, end:end},
       success:function()
       {
        calendar.fullCalendar('refetchEvents');
        alert("Added Successfully");
        //cell.css("background-color", "red");
       }
      })
     }
    },
    editable:true,

    eventDrop:function(event)
    {
     var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
     var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
     var title = event.title;
     var id = event.id;
     $.ajax({
      url:"update.php",
      type:"POST",
      data:{title:title, start:start, end:end, id:id},
      success:function()
      {
       calendar.fullCalendar('refetchEvents');
       alert("Event Updated");
      }
     });
    },

    eventClick:function(event)
    {
     if(confirm("Are you sure you want to remove it?"))
     {
      var id = event.id;
      $.ajax({
       url:"delete.php",
       type:"POST",
       data:{id:id},
       success:function()
       {
        calendar.fullCalendar('refetchEvents');
        alert("Event Removed");
       }
      })
     }
    },
    // eventAfterRender: function (event, element, view) {
    //     Rendering = Background;
    //     var dataHoje = new Date();
    //     if (event.start < dataHoje && event.end > dataHoje) {
    //         //event.color = "#FFB347"; //Em andamento
    //         //element.css('background-color', '#FFB347');
    //         element.css('borderColor', '#FFB347');
    //     } else if (event.start < dataHoje && event.end < dataHoje) {
    //         //event.color = "#77DD77"; //Concluído OK
    //         element.css('background-color', '#77DD77');
    //     } else if (event.start > dataHoje && event.end > dataHoje) {
    //         //event.color = "#AEC6CF"; //Não iniciado
    //         element.css('background-color', '#AEC6CF');
    //     }
    // },
   });
  });
   
  </script>
 </head>
 <body>
  <br />
  <h2 align="center" style="color:black;">Appsmatta Working Days</h2>
  <br />
  <div class="container">
   <div id="calendar">
   </div>
  </div>
 </body>
</html>