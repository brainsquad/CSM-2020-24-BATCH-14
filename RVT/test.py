import json
import requests

# Run inference on an image
url = "https://api.ultralytics.com/v1/predict/6GCQBtrZo64reQIUmBFS"
headers = {"x-api-key": "8a44fe9e3dd1b1607c9234c22ab3b6a108cbd01f8e"}
data = {"size": 640, "confidence": 0.25, "iou": 0.45}
with open("images/frame2.png", "rb") as f:
	response = requests.post(url, headers=headers, data=data, files={"image": f},verify=False)

# Check for successful response
response.raise_for_status()

# Print inference results
print(json.dumps(response.json(), indent=2))