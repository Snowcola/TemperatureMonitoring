// socket
var socket = io.connect('http://' + document.domain + ':' + location.port);
var char = $('chart').get(0);
socket.on('connect', function() {
    if (chart.getContext) {
        render();
        window.onresize = render;
    }
    //load historical data
    send();
});

socket.on('disconnect', function() {
    if (smoothie){
        smoothie.stop();
    }
    $('#transport').text('(disconnected)');
});

var temps = new Array;
socket.on('new_temp', function(msg) {
          $('#log').append('<br>Temp: ' + msg.data + ' degC');
          if (time) {
              time.append(+new Date, msg.data);
          }
          if (temps && labels) { 
              labels.push(new Date)
              temps.push(msg.data);
              if(temps.length > 10) {
                  temps.shift();
                  labels.shift();
              }
              chart1.update();
              send();
          }
});

function send() {
    $('#transport').text(socket.io.engine.transport.name);
}

// charts - smoothie

  var smoothie;
  var time;
  var max = 10;
  var min = 0;
  var sections = max - min;
  function render() {
      if (smoothie)
          smoothie.stop();
      chart.width = document.body.clientWidth;
      smoothie = new SmoothieChart({verticalSections:sections, maxValue:max,minValue:min})
      smoothie.streamTo(chart, 2000);
      time = new TimeSeries();
      smoothie.addTimeSeries(time, {
          strokeStyle: 'rgb(255, 0, 0)',
          fillStyle: 'rgba(255, 0, 0, 0.4)',
          lineWidth: 2
      });
  }

// new chart - chartjs

var labels = new Array;

var ctx = document.getElementById('chart1').getContext('2d');
ctx.canvas.width = 1000;
ctx.canvas.height = 300;
var cfg = {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: 'Temperature over time',
      data: temps,
      type: 'line',
      pointRadius: 0,
      fill: false,
      lineTension: 0,
      borderWidth: 2
    }]
  },
  options: {
    scales: {
      xAxes: [{
        type: 'time',
                    time: {
                        displayFormats:{
                            second: 'h:mm:ss a'
                        }
                    },
        distribution: 'series',
        ticks: {
          source: 'labels'
        }
      }],
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Temperature (degC)'
        }
      }]
    }
  }
};
var chart1 = new Chart(ctx, cfg);