'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Summarization Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class SummarizationIO(ServiceIO):
    service = ServiceString.SUMMARIZATION
    required_input_fields = ["text","sent_length"]
    optional_input_fields = []
    input_structure = {
        "text": str, 
        "sent_length": int
    }

    output_structure = {
        "summary": str
    }


    @classmethod
    def special_validation(self, payload):
        
        if payload.get('sent_length'):
            if payload['sent_length'] > payload['text'].count("."):
                return False, 'Provided "sent_length" value is larger than the number of sentences in the input text.'

        return super().special_validation(payload)