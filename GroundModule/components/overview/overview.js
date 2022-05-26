const chartjs = require('chart.js');

let label_length = 0;
let last_payload = 0;
let last_container = 0;
let offset = 0;

//'rgb(92,94,93)', //Gray
//'rgb(255, 99, 132)', //Red
//'rgb(54, 162, 235)', //Blue

const telemetryChartConfig = {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Container',
      backgroundColor: 'rgb(255, 99, 132)', //Red
      borderColor: 'rgb(255, 99, 132)', //Red
      data: [],
      fill: false,
    },
    {
      label: 'Payload',
      backgroundColor: 'rgb(120, 0, 120)',
      borderColor: 'rgb((120, 0, 120)',
      data: [],
      fill: false,
    },
    ]
  },
  options: {
    responsive: true,
    mantainAspectRation: false,
    spanGaps: true,
    title: {
      display: true,
      text: 'Payload'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Mission Time (hh/mm/ss)'
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Altitude (m)'
        }
      }]
    }
  }
};


telemetryCanvasCtx = document.getElementById('telemetry-canvas').getContext('2d');
telemetryChart = new chartjs.Chart(telemetryCanvasCtx, telemetryChartConfig);

function addValueToTelemetryChart(index, value, label) {
  if (label_length == 0)
    offset = value;
    if (offset < 0)
      offset *= -1;
    
  if (index == 1) {
    if (last_payload == label_length) {
      telemetryChart.data.labels.push(label);
      label_length++;
    } 
    telemetryChart.data.datasets[index].data[label_length - 1] = value + offset - 30;
    last_payload = label_length
    console.log("PAYLOAD: " + telemetryChart.data.datasets[1].data.toString());
  } else {
    if (last_container == label_length) {
      telemetryChart.data.labels.push(label);
      label_length++;
    }
    telemetryChart.data.datasets[index].data[label_length - 1] = value + offset;
    last_container = label_length;
    console.log("CONTAINER: " + telemetryChart.data.datasets[0].data.toString());
  }
  
  // if (telemetryChart.data.labels.length > 20) {
  //   telemetryChart.data.datasets[0].data.shift();
  //   telemetryChart.data.datasets[1].data.shift();
  //   telemetryChart.data.labels.shift();
  // }
  
  
  telemetryChart.update();
}

function sendCustomCommand() {
  let inputElem = document.getElementById('custom-command-input');
  sendCommand(inputElem.value);
}

function testAll() {
  parsePacketAndAddValues('6082,00:01:30,50,C,F,N,500.3,29.3,4.42,15:48:02,36.3501,-3.3501,50.3,16,LANDED,CXON');
  parsePacketAndAddValues('6082,01:22:10,50,C,500.3,29.3,4.31,20,18,21,30,35,30,-133,-130, 2600,0,STANDBY');
}

//testAll();

function setCurrentTemperature(id, temp) {
  let elem = document.getElementById(id);
  elem.innerHTML = 'Current temperature: ' + temp;
}

function setCurrentBatteryVoltage(id, volts) {
  let elem = document.getElementById(id);
  elem.innerHTML = 'Current battery voltage: ' + volts;
}

function setCurrentGPSCoords(id, lat, lng) {
  let elem = document.getElementById(id);
  elem.innerHTML = 'Current GPS coordinates: ' + lat + ', ' + lng;
}

function setCurrentRotationRate(id, rate) {
  let elem = document.getElementById(id);
  elem.innerHTML = 'Current rotation rate: ' + rate;
}

