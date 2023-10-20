'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Tag Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TagIO(ServiceIO):
    service = ServiceString.TAG
    required_input_fields = ["text"]
    optional_input_fields = ["types","n"]
    input_structure = {
        "text": str, 
        "types": str, 
        "n": int
    }

    output_structure = {
        "tags": dict
    }
