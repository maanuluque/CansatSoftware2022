var {SerialPort} = require('serialport');
var xbee_api = require('xbee-api');

var C = xbee_api.constants;

//actualizar
const CONTAINER_MAC_ADDRESS = '0013A20041BA3838';


var sendSimData = false;
var simCommands = getSimCommandListFromFile();
var currentSimCommandIndex = 0;

var xbeeAPI = new xbee_api.XBeeAPI({
  api_mode: 1
});

var serialport = new SerialPort({ path: "/dev/ttyUSB0", baudRate: 9600, parser: xbeeAPI.rawParser()})

// var serialport = new SerialPort("COM3", {
//   baudRate: 9600,
//   parser: xbeeAPI.rawParser()
// });

serialport.on("open", function() {
  console.log("Serial port open... sending ATND");
  var frame = {
    type: C.FRAME_TYPE.ZIGBEE_TRANSMIT_REQUEST,
    destination64: CONTAINER_MAC_ADDRESS,
    data: 'CMD,HELLO,THERE'
  };

  serialport.write(xbeeAPI.buildFrame(frame), function(err, res) {
    if (err) throw(err);
    else console.log(res);
  });
});


// Switches the port into "flowing mode"
serialport.on('data', function (data) {
  xbeeAPI.parseRaw(data);
})
console.log("flowing mode on")

xbeeAPI.on("frame_object", function(frame) {
  if (frame.data) parsePacketAndAddValues(String.fromCharCode.apply(null, frame.data));
});

xbeeAPI.on("frame_raw", function(frame) {
  console.log(frame);
});
xbeeAPI.on("error", function(frame) {
  console.log(frame);
});

setInterval(()=> {
  if (sendSimData) {
    sendCommand(simCommands[currentSimCommandIndex]);
    currentSimCommandIndex++;
  }
}, 1000);

function toggleSendSimData() {
  sendSimData = !sendSimData;
  document.getElementById('sim-on-indicator').style.display = sendSimData ? 'block' : 'none';
  document.getElementById('sim-off-indicator').style.display = sendSimData ? 'none' : 'block';
  console.log('SIM activated: ' + sendSimData);
  if (sendSimData) currentSimCommandIndex = 0;
}

function sendCommand(cmdData) {
  var frame = {
    type: C.FRAME_TYPE.ZIGBEE_TRANSMIT_REQUEST,
    destination64: CONTAINER_MAC_ADDRESS,
    data: cmdData
  };
  console.log("Sending command " + cmdData);
  serialport.write(xbeeAPI.buildFrame(frame), function(err, res) {
    if (err) throw(err);
    else console.log(res);
  });
}

function sendContainerSetTimeCommand(){
  sendCommand('CMD,1082,ST,' + getUtcTimeStr());
}

function getUtcTimeStr() {
  const date = new Date();
  return date.toUTCString().split(" ")[4];
}

function parsePacketAndAddValues(content) {
  console.log('RECEIVED: ' + content)
  const telemetryElements = content.split(',');
  // FOR DESCENDING PAYLOAD
  // if (telemetryElements.length >= 2) {
  //   let speed = telemetryElements[0]
  //   let step = telemetryElements[1]
  //   let avg = telemetryElements[4]
  //   addValueToTelemetryChart(0, Number(speed), Number(step), Number(avg))
  // }
  // FOR NORMAL MODE
  let word = telemetryElements[3]
  console.log(telemetryElements)
  if (word === 'C') { // Received container telemetry
    addValueToTelemetryChart(0, Number(telemetryElements[6]), telemetryElements[1]);
    addValueToTelemetryCsv(containerTelemetryWriteStream, content);
    setCurrentTemperature('container-telemetry-temperature', telemetryElements[7]);
    setCurrentBatteryVoltage('container-telemetry-battery-voltage', telemetryElements[8]);
    setCurrentGPSCoords('container-telemetry-gps-coordinates', telemetryElements[10], telemetryElements[11]);
    publishMQTTMessage(content);
  } else if (word == 'P') { // Received payload telemetry
      telemetryElements[1] = getUtcTimeStr();
      addValueToTelemetryChart(1, Number(telemetryElements[4]), telemetryElements[1]);
      addValueToTelemetryCsv(payloadTelemetryWriteStream, content);
      setCurrentTemperature('payload-telemetry-temperature', telemetryElements[5]);
      setCurrentRotationRate('payload-telemetry-rotation-rate', telemetryElements[7]); //uso gyro_r
      publishMQTTMessage(content);
  }
}
