const readline = require('readline');
const fs = require('fs');

const CONTAINER_TELEMETRY_FILE_NAME = 'Flight_1082_C.csv'
const PAYLOAD_TELEMETRY_FILE_NAME = 'Flight_1082_T.csv'
var containerTelemetryWriteStream = fs.createWriteStream('telemetry/' + CONTAINER_TELEMETRY_FILE_NAME, {flags:'w'});
var payloadTelemetryWriteStream = fs.createWriteStream('telemetry/' + PAYLOAD_TELEMETRY_FILE_NAME, {flags:'w'});

addValueToTelemetryCsv(containerTelemetryWriteStream,
  '<TEAM_ID>,<MISSION_TIME>,<PACKET_COUNT>,<PACKET_TYPE>,<MODE>,<TP_RELEASED>,\
  <ALTITUDE>,<TEMP>,<VOLTAGE>,<GPS_TIME>,<GPS_LATITUDE>,<GPS_LONGITUDE>,\
  <GPS_ALTITUDE>,<GPS_SATS>,<SOFTWARE_STATE>,<CMD_ECHO>');
addValueToTelemetryCsv(payloadTelemetryWriteStream,
    '<TEAM_ID>,<MISSION_TIME>,<PACKET_COUNT>,<PACKET_TYPE>,<TP_ALTITUDE>,\
    <TP_TEMP>,<TP_VOLTAGE>,<GYRO_R>,<GYRO_P>,<GYRO_Y>,<ACCEL_R>,<ACCEL_P>,<ACCEL_Y>,\
    <MAG_R>,<MAG_P>,<MAG_Y>,<POINTING_ERROR>,<TP_SOFTWARE_STATE>');

function addValueToTelemetryCsv(stream, content) {
  stream.write(content + "\n");
}

function getSimCommandListFromFile() {
  let result = []
  const readInterface = readline.createInterface({
    input: fs.createReadStream('data/flight19v2.csv'),
    output: process.stdout,
    console: false
  });
  readInterface.on('line', function(line) {
    const processedLine = line.split('#')[0];
    if (processedLine.length) result.push(line);
  });
  return result;
}

function lastElem(array) {
  return array[array.length - 1];
}