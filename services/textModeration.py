import string
from profanity_check import predict_prob
from better_profanity import profanity
import json
import requests
import os
from dotenv import load_dotenv
from models.moderationResponse import moderationResponse

profanity.load_censor_words()
load_dotenv()

edenKey = os.getenv('EDEN_KEY')

ACCEPTANCE_NSFW_SCORE = 0.4
BANNED_NSFW_SCORE = 0.9

def checkModerationLowPriority(content):
    moderationRate = checkModerationByProfanity(content)[0]
    print(moderationRate)
    if (moderationRate <= ACCEPTANCE_NSFW_SCORE):
        return moderationResponse(code= 200, 
            message= 'Content does not violate Community Standard', isViolated= False,
            isBanned= False, reproducedContent= censorModeratingContent(content), reason= '')
    
    elif (moderationRate <= BANNED_NSFW_SCORE):
        return moderationResponse(code= 200, 
            message= 'Content violated Community Standard', isViolated= True,
            isBanned= False, reproducedContent= censorModeratingContent(content), reason= '')
    
    else:
        return moderationResponse(code= 200, 
            message= 'Content violated Community Standard', isViolated= True,
            isBanned= True, reproducedContent= '', reason= 'Reach our limit of Community Standard')

def checkModerationHighPriority(content):
    print(edenKey)
    headers = {"Authorization": "Bearer " + edenKey}
    url = "https://api.edenai.run/v2/text/moderation"
    
    freeAuthor = 'openai'
    paidAuthor = 'microsoft' if len(content) > 199 else 'google'
    payload = {
        "providers": freeAuthor + ',' + paidAuthor,
        "language": "auto-detect",
        "text": content,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)

    paidAuthorNSFWScore = result[paidAuthor]['nsfw_likelihood_score']
    freeAuthorNSFWScore = result[freeAuthor]['nsfw_likelihood_score']

    print('paid: '+ str(paidAuthorNSFWScore))
    print('free: '+ str(freeAuthorNSFWScore))

    paidAuthorReason = result[paidAuthor]['items']
    freeAuthorReason = result[freeAuthor]['items']
    paidAuthorReason.extend(freeAuthorReason)

    if (paidAuthorNSFWScore <= ACCEPTANCE_NSFW_SCORE
            and freeAuthorNSFWScore <= ACCEPTANCE_NSFW_SCORE):
        return moderationResponse(code= 200, 
            message= 'Content does not violate Community Standard', isViolated= False, 
            isBanned= False, reproducedContent= '', reason= '')
        
    elif (paidAuthorNSFWScore <= BANNED_NSFW_SCORE 
            and freeAuthorNSFWScore <= BANNED_NSFW_SCORE):
        return moderationResponse(code= 200, 
            message= 'Content violated Community Standard', isViolated= True, 
            isBanned= False, reproducedContent= '', 
            reason= paidAuthorReason)
    
    else:
        return moderationResponse(code= 200, 
            message= 'Content violated Community Standard', isViolated= True, 
            isBanned= True, reproducedContent= '', 
            reason= paidAuthorReason)

def checkModerationByProfanity(content):
    prompt = string.Template('predict() ${content}')
    values = {"content": content}
    prompt = prompt.substitute(values)
    return predict_prob([prompt])

def censorModeratingContent(content):
    return profanity.censor(content)