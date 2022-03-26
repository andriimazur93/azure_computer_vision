import os
import io
import json

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeaturesTypes
import requests
from PIL import Image, ImageDraw, ImageFont


credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']

cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

image_url = "https://i.insider.com/532b6e2a6bb3f7a361cae216?width=1300&format=jpeg&auto=webp"
response = cv_client.read(url=image_url, language='en', raw=True)
operationLocation = response.headers['Operation-Location']
operation_id = operationLocation.split('/')[-1]
result = cv_client.get_read_result(operation_id)

print(result)
print(result.status)
print(result.analyze_result)


if result.status == OperationStatusCodes.succeeded:
    read_result = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines():
            print("Line: {line.text}")
            for work in line.words:
                print(f"Words: {word.text}")
