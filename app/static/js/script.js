function dailyGraph(station){
    var selectedStation = station;
    var d = new Date();
    var day = d.getDay();

    $.getJSON("http://127.0.0.1:5000/dailyData/" + selectedStation, null, function(daily){
    //console.log(day);
    console.log(selectedStation);
    console.log(daily)

    google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Day', 'Average Number of Available Bikes',],
          ['Mon',  daily[0]["AVG(available_bikes)"],    ],
          ['Tue',  daily[1]["AVG(available_bikes)"],    ],
          ['Wed',  daily[2]["AVG(available_bikes)"],    ],
          ['Thu',  daily[3]["AVG(available_bikes)"],    ],
          ['Fri',  daily[4]["AVG(available_bikes)"],    ],
          ['Sat',  daily[5]["AVG(available_bikes)"],   ],
          ['Sun',  daily[6]["AVG(available_bikes)"],   ],

        ]);

        var options = {
          title: 'Daily Data for Selected Station',
          vAxis: {
              minValue: 0,
              title: "Average Number of Available Bikes",
            },
          hAxis: {
              title: "Day",
            },
          //curveType: 'function',
          legend: { position: 'bottom' },
          animation: {
            duration: 800,
            startup: true 
          }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    })

}

