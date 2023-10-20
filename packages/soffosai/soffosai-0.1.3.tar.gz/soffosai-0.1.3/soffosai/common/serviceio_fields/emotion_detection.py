'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Emotion Detection Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class EmotionDetectionIO(ServiceIO):
    service = ServiceString.EMOTION_DETECTION
    required_input_fields = ["text","sentence_split","sentence_overlap"]
    optional_input_fields = ["emotion_choices"]
    input_structure = {
        "text": str, 
        "sentence_split": int, 
        "sentence_overlap": bool, 
        "emotion_choices": str
    }

    output_structure = {
        "spans": dict
    }


    @classmethod
    def special_validation(self, payload):
        
        choices = ['joy','trust','fear','surprise','sadness','disgust','anger','anticipation']

        if payload["sentence_split"] == 1 and payload["sentence_overlap"] == True:
            return False, 'Value "sentence_overlap" must be false when "sentence_split" is set to 1.'
        
        if 'emotion_choices' in payload:
            unsupported_emotion = []
            for emotion in payload['emotion_choices']:
                if emotion not in choices:
                    unsupported_emotion.append(emotion)
            if len(unsupported_emotion) > 0:
                return False, f'unsupported emotions: [{", ".join(unsupported_emotion)}].'
            
        payload['sentence_overlap'] = 1 if payload['sentence_overlap'] else 0

        return super().special_validation(payload)