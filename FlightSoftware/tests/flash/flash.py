import os
import json
import utime

current_state = "PAYLOAD_DEPLOY"
send_telemetry = True
simulation_mode = False
tp_deploy_time = 00:00:00
descend_payload = False
package_count = 0
var2 = 2.0
print(utime.localtime())

dictionary = {"key1": var1, "key2": var2}
json_data = json.dumps(dictionary)

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(json_data, file)