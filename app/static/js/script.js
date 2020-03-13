function hourlyGraph(station){
    var selectedStation = station;
    var d = new Date();
    var day = d.getDay();

    $.getJSON("http://127.0.0.1:5000/hourlyData/" + selectedStation + "/" + day, null, function(hourly){
    console.log(day);
    console.log(selectedStation);
    console.log(hourly)

    google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Time', 'Average Number of Available Bikes',],
          ['05:00',  hourly[5]["AVG(available_bikes)"],    ],
          ['06:00',  hourly[6]["AVG(available_bikes)"],    ],
          ['07:00',  hourly[7]["AVG(available_bikes)"],    ],
          ['08:00',  hourly[8]["AVG(available_bikes)"],    ],
          ['09:00',  hourly[9]["AVG(available_bikes)"],    ],
          ['10:00',  hourly[10]["AVG(available_bikes)"],   ],
          ['11:00',  hourly[11]["AVG(available_bikes)"],   ],
          ['12:00',  hourly[12]["AVG(available_bikes)"],   ],
          ['13:00',  hourly[13]["AVG(available_bikes)"],   ],
          ['14:00',  hourly[14]["AVG(available_bikes)"],   ],
          ['15:00',  hourly[15]["AVG(available_bikes)"],   ],
          ['16:00',  hourly[16]["AVG(available_bikes)"],   ],
          ['17:00',  hourly[17]["AVG(available_bikes)"],   ],
          ['18:00',  hourly[18]["AVG(available_bikes)"],   ],
          ['19:00',  hourly[19]["AVG(available_bikes)"],   ],
          ['20:00',  hourly[20]["AVG(available_bikes)"],   ],
          ['21:00',  hourly[21]["AVG(available_bikes)"],   ],
          ['22:00',  hourly[22]["AVG(available_bikes)"],   ],
          ['23:00',  hourly[23]["AVG(available_bikes)"],   ],
          ['00:00',  hourly[0]["AVG(available_bikes)"],    ],

        ]);

        var options = {
          title: 'Hourly Data for Selected Station',
          vAxis: {
              minValue: 0,
              title: "Average Number of Available Bikes",
            },
          hAxis: {
              title: "Time",
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

