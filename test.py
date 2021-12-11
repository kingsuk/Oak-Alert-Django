import json
message_body="""type = CurrentAlert 

data = {
"id": 27924,
"device_id": "134916",
"energy": "386.7000",
"current": 37.673425827107806,
"voltage": 249.59,
"power": "4640.0000",
"power_factor": 0.8643,
"reactive_power": 2.5300000000000002,

"consumed_active_energy": null,

"frequency": null,
"measurement_time": "2021-08-05 16:55:00",
"phase": "R",
"current_deviation": 37.673425827107806
}"""

type_=str(message_body.split("=")[1].split("\n")[0].strip())
print(type_)
body = str(message_body.split("data =")[1])

json_body = """{"type": """+type_+""", "body": """+body+"""}"""

print(json.loads(json_body))