import subprocess
import json
import urllib.parse
import boto3
import base64
import os
import requests

s3 = boto3.client('s3', region_name=os.environ['REGION'])

def lambda_handler(event, context):
    # Configure the S3 bucket and key from the event
    s3_event = event['Records'][0]['s3']
    s3_bucket = s3_event['bucket']['name']
    s3_key = urllib.parse.unquote_plus(s3_event['object']['key'])
    
    print(event)
    print(s3_bucket)
    print(s3_key)
    
     # Download the image from S3
    s3_object = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    image_data = s3_object['Body'].read()
    
    # Define the URL to which you want to send the POST request
    url = "https://app.maxusai.com/api/v2/predict/inference"
    
    # Construct the URL of the S3 object
    object_url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"
    print(object_url)
    
    # Image Base 64
    # IMAGE_BASE64 = $(curl -s object_url | base64 -w 0)
    url_base64 = base64.b64encode(image_data).decode('utf-8')

    # Define the data you want to send in the POST request (as a JSON payload)
    payload = {
        "projectID": os.environ['PROJECT_ID'],
        "modelID": os.environ['MODEL_ID'],
        "imageBase64": f"data:image/jpeg;base64,${url_base64}"
    }

    # Serialize the data to a JSON string
    post_data_json = json.dumps(payload)
    
    #headers
    headers_dict = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.environ['API_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    # Convert the list of headers to a dictionary
    # headers_dict = {}
    # for header in headers:
    #     key, value = header.split(": ", 1)
    #     headers_dict[key] = value

    # Define the curl command as a list of strings with the -X POST option
    # curl_command = ["curl", "-X", "POST"]
    
    # Add the headers to the curl command
    # for key, value in headers_dict.items():
    #     curl_command.extend(["-H", f"{key}: {value}"])
    
    # Add the post URL and data
    # curl_command.extend([url, "-d", post_data_json])

    try:
        response = requests.post(url, headers=headers_dict, json=payload)
        print(response)

        if response.status_code == 200:
            response_data = response.json()
            response_text = json.dumps(response_data, indent=2)
            response_status_code = 200
        else:
            response_text = f"HTTP error: {response.status_code}\n{response.text}"
            response_status_code = response.status_code
            
        # Run the curl command and capture the output
        # result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        # response = {
        #     "statusCode": 200,
        #     "body": result.stdout
        # }
    except Exception as e:
        response_text = str(e)
        response_status_code = 500

    s = 'body ' + response_text
    print(s)
    return {
        "statusCode": response_status_code,
        "body": response
    }
