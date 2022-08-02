# Cansat Software 2022 - Team ITBA

## Mission Overview 
>Design a Cansat that shall consist of a container and a payload. The payload shall be
attached to the container by a 10 meter long tether. The Cansat shall be launched to an
altitude ranging from 670 meters to 725 meters above the launch site and deployed near
apogee (peak altitude). Orientation of deployment is not controlled and is very violent with
large shock forces. The Cansat must survive the forces incurred at launch and deployment.
Once the Cansat is deployed from the rocket, the Cansat shall descend using a parachute at
a rate of 15 m/s. At 400 meters, the Cansat shall deploy a larger parachute to reduce the
descent rate to 5 m/s. At 300 meters, the Cansat shall release a tethered payload to a
distance of 10 meters in 20 seconds. During that time, the payload shall maintain the
orientation of a video camera pointing in the south direction. The video camera shall be
pointed 45 degrees downward to assure terrain is in the video.
Bonus: As the container is releasing the payload, the container shall contain a video camera
and start recording to show the descent of the payload. All videos are to be recorded and
recovered when the Cansat is recovered from the field.>

Source: https://www.cansatcompetition.com/docs/CanSat_Mission_Guide_2022.pdf

## Modules

The CanSat Software consists on 3 modules:
- Container Module
- Payload Module
- Ground Module

### Container Module
Programed in Micropython using a Raspberry Pi Pico as microcontroller. The main goal of this module is to read sensor data in order to determine cansat position and flight status along other usefull variables, that will allow the main program to execute tasks such as releasing parachutes at certain altitude, release tethered payload when descending and relay telemetry (both container and payload) to ground station.

### Payload Module
Payload's main program goal is the camera stabilization, achieved by obtaining sensor's data and correcting its movement with a servo, and relaying all data to the container (which relays that telemetry to ground station).   

### Ground Module
Ground Module allows the visualization of all telemetry sent by the container. It uses ChartJS for that purpose. 

#### Compilation
Requirements:

NodeJS
NPM
To run the Application, enter the repo and run the following commands:

``cd GroundModule``<br />
``npm install``<br />
``npm start``<br />
