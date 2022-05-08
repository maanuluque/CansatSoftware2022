const chartjs = require('chart.js');

//'rgb(92,94,93)', //Gray
//'rgb(255, 99, 132)', //Red
//'rgb(54, 162, 235)', //Blue

const containerTelemetryChartConfig = {
  type: 'line',
  data: {
    labels: ['00:00:00'],
    datasets: [{
      label: 'Altitude',
      backgroundColor: 'rgb(255, 99, 132)', //Red
      borderColor: 'rgb(255, 99, 132)', //Red
      data: [0],
      fill: false,
    }]
  },
  options: {
    responsive: true,
    mantainAspectRation: false,
    title: {
      display: true,
      text: 'Container'
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

const payloadTelemetryChartConfig = {
  type: 'line',
  data: {
    labels: ['00:00:00'],
    datasets: [{
      label: 'Altitude',
      backgroundColor: 'rgb(255, 99, 132)', //Red
      borderColor: 'rgb(255, 99, 132)', //Red
      data: [0],
      fill: false,
    }]
  },
  options: {
    responsive: true,
    mantainAspectRation: false,
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


containerTelemetryCanvasCtx = document.getElementById('container-telemetry-canvas').getContext('2d');
containerTelemetryChart = new chartjs.Chart(containerTelemetryCanvasCtx, containerTelemetryChartConfig);

payloadTelemetryCanvasCtx = document.getElementById('payload-telemetry-canvas').getContext('2d');
payloadTelemetryChart = new chartjs.Chart(payloadTelemetryCanvasCtx, payloadTelemetryChartConfig);


function addValueToTelemetryChart(chart, value, label) {
  chart.data.datasets[0].data.push(value);
  chart.data.labels.push(label);
  if (chart.data.labels.length > 20) {
    chart.data.datasets[0].data.shift();
    chart.data.labels.shift();
  }
  console.log(chart);
  chart.update();
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

