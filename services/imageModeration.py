import json
import requests
import os

from models.moderationResponse import moderationResponse

edenKey = os.getenv('EDEN_KEY')

ACCEPTANCE_NSFW_SCORE = 0.4
BANNED_NSFW_SCORE = 0.9

def checkImageModeration(image):
    headers = {"Authorization": "Bearer " + edenKey}

    paidAuthor = 'google'

    url = " https://api.edenai.run/v2/image/explicit_content"
    json_payload = {
        "providers": paidAuthor,
        "file_url": image,
        "fallback_providers": ""
    }

    response = requests.post(url, json=json_payload, headers=headers)
    result = json.loads(response.text)

    moderationRate = result[paidAuthor]['nsfw_likelihood_score']
    print ('google: ' + str(moderationRate))

    if (moderationRate <= ACCEPTANCE_NSFW_SCORE):
        return moderationResponse(code= 200, 
            message= 'Content does not violate Community Standard', isViolated= False,
            isBanned= False, reproducedContent= '', reason= '')
    
    elif (moderationRate <= BANNED_NSFW_SCORE):
        return moderationResponse(code= 200, 
            message= 'Content violated Community Standard', isViolated= True,
            isBanned= False, reproducedContent= '', reason= result[paidAuthor]['items'])
    
    else: 
        return moderationResponse(code= 200, 
            message= 'Content violated Community Standard', isViolated= True,
            isBanned= True, reproducedContent= '', reason= result[paidAuthor]['items'])
