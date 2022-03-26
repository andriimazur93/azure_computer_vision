import time
import json

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests
from PIL import Image, ImageDraw, ImageFont


credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']

cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

image_url = "https://i.insider.com/532b6e2a6bb3f7a361cae216?width=1300&format=jpeg&auto=webp"
response = cv_client.read(url=image_url, language='en', raw=True)

files = ['img1.png', 'img2.png', 'img3.png', 'img4.png', 'img5.png']
for local_file in files:
    response = cv_client.read_in_stream(open(local_file, 'rb'), language='en', raw=True) 

    operationLocation = response.headers['Operation-Location']
    operation_id = operationLocation.split('/')[-1]
    read_result = cv_client.get_read_result(operation_id)


    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = cv_client.get_read_result(operation_id)
        if str(read_result.status) not in ['OperationStatusCodes.notStarted', 'OperationStatusCodes.running']:
            break
        time.sleep(1)

    if str(read_result.status) == 'OperationStatusCodes.succeeded':
        read_results = read_result.analyze_result.read_results
        for analyzed_result in read_results:
            for line in analyzed_result.lines:
                print(line.text)

    image = Image.open(local_file)
    if str(read_result.status) == 'OperationStatusCodes.succeeded':
        read_results = read_result.analyze_result.read_results
        for analyzed_result in read_results:
            for line in analyzed_result.lines:
                x1, y1, x2, y2, x3, y3, x4, y4 = line.bounding_box
                draw = ImageDraw.Draw(image)
                draw.line(
                    (
                        (x1, y1), (x2, y1), 
                        (x2, y2), (x3, y2),
                        (x3, y3), (x4, y3),
                        (x4, y4), (x1, y4),
                        (x1, y1)), 
                        fill=(255, 0, 0), 
                        width=5
                )
    # image.show()
    filename = local_file.split('.')[0]
    image.save(f'{filename}_detected.jpg')
