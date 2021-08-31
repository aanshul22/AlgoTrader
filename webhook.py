import json
import requests

WEBHOOK_URL = DISCORD_WEBHOOK_URL

# message = {"content" : "Testing webhook"}

# payload = {'payload_json': json.dumps(message)}

# r = requests.post(WEBHOOK_URL, payload)

# print(r)

def send_alerts(lastest_date, alert_list):
	alert_list = _beautify(alert_list)
	content = f"Date: {lastest_date}\n\n"
	content += "\n".join(alert_list)
	message = {"content": content}
	payload = {'payload_json': json.dumps(message)}
	r = requests.post(WEBHOOK_URL, payload)
	print(r)


def _beautify(alert_list):
	foo = lambda x : x[:-3]
	alert_list = list(map(foo, alert_list))
	alert_list = list(map(str.capitalize, alert_list))
	return sorted(alert_list)

