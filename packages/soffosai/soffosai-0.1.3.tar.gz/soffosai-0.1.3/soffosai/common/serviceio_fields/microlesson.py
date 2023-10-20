'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Microlesson Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class MicrolessonIO(ServiceIO):
    service = ServiceString.MICROLESSON
    required_input_fields = ["content"]
    optional_input_fields = []
    input_structure = {
        "content": list
    }

    output_structure = {
        "microlesson": dict
    }


    @classmethod
    def special_validation(self, payload):
        
        for i, d in enumerate(payload['content']):
            if 'source' not in d:
                return False, f"'source' field missing from element at index {i} in 'content'."
            elif not isinstance(d['source'], str):
                return False, f"'source' field at index {i} in 'content' has wrong type. Expecting str."
            if 'text' not in d:
                return False, f"'text' field missing from element at index {i} in 'content'."
            elif not isinstance(d['text'], str):
                return False, f"'text' field at index {i} in 'content' has wrong type. Expecting str."

        return super().special_validation(payload)