from django.shortcuts import render
import requests
import json
import time
url = "https://api.bland.ai/v1/calls/{call_id}"
headers = {"authorization": "sk-j7yf7sf02y12oh0pyiet5k2663t6jbvfcehzmdlv7xu3xo36og8ad4o8weob94ts69"}
def fetch_transcript(call_id):
    while True:
        response = requests.request("GET", url.format(call_id=call_id), headers=headers)
        response_json = json.loads(response.text)
        if response_json.get('completed'):
            return response_json.get('concatenated_transcript')
        time.sleep(5)

def index(request):
    return render(request, 'index.html')

def transcript(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        prompt = request.POST.get('prompt')
        import requests
        url = "https://api.bland.ai/v1/calls"
        payload = {
            "phone_number": phone_no,
            "task": prompt
        }
        headers = {
            "authorization": "sk-j7yf7sf02y12oh0pyiet5k2663t6jbvfcehzmdlv7xu3xo36og8ad4o8weob94ts69",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)
        response_json = json.loads(response.text)
        call_id = response_json.get('call_id')
        print(call_id)
        output=fetch_transcript(call_id)
        print(output)
        context={
                    "output" : output
                }
        print(context)
        return render(request, 'return.html', context)        
    return render(request, 'index.html')  # Render the input form on a GET request