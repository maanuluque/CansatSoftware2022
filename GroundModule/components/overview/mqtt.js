var mqtt = require('mqtt');

var mqttActivated = false;

//actualizar cuando este la nuestra
var client  = mqtt.connect({
  host: 'cansat.info',
  port: 1883,
  username: '2764',
  password: 'Nuyvlapy296!'
});

topic = 'teams/2764';
 
client.on('connect', function () {
  console.log('Connected');
  client.subscribe('presence', function (err) {
    if (!err) {
      console.log('Received presence!');
      client.publish('presence', 'Hello mqtt')
    } else {
      console.log('Error:');
      console.log(err);
    }
  });
})
 
client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  client.end()
})


function toggleMQTTActivated() {
  mqttActivated = !mqttActivated;
  document.getElementById('mqtt-on-indicator').style.display = mqttActivated ? 'block' : 'none';
  document.getElementById('mqtt-off-indicator').style.display = mqttActivated ? 'none' : 'block';
  console.log('MQTT activated: ' + mqttActivated);
}

//Example telemetry '6082,1:22:10,50,C,500.3,29.3,4.31,20,18,21,30,35,30,-133,-130,2600,0,STANDBY
function publishMQTTMessage(message){
  client.publish(topic, message);
}