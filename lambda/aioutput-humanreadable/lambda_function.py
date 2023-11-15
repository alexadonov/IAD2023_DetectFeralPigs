import json
import logging

def get_num_pigs(event):
    # Global variables
    MIN_CONF = 0.85
    PIG_LABEL_ID = 21  # 22
    PIGLET_LABEL_ID = 23  # 24
    print(event)
    
    inferenceload = json.loads(event['Records'][0]['Sns']['Message'])
    print(inferenceload)
    
    inference = json.loads(inferenceload['responsePayload']['body'])
    print(inference)
    # Error handling
    try:
        for pred in inference:
            pred['polygons'].append({'labelID': 'NONE', 'confScore': 0.00})
    
        # Get pig/piglet predictions
        pig_predictions = [pred for pred in inference if pred['polygons'][0]['labelID'] == PIG_LABEL_ID and pred['confScore'] >= MIN_CONF]
        piglet_predictions = [pred for pred in inference if pred['polygons'][0]['labelID'] == PIGLET_LABEL_ID and pred['confScore'] >= MIN_CONF]
    
    except Exception as e:
        print('fail')
        print(e)
        return False
    
    num_pigs = {
        'num_pigs': len(pig_predictions),
        'num_piglets': len(piglet_predictions)
    }
    
    print(num_pigs)
    return num_pigs
            
def lambda_handler(event, context):
    return get_num_pigs(event)
