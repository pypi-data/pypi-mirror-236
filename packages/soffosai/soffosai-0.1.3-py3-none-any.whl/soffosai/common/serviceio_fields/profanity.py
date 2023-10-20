'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Profanity Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class ProfanityIO(ServiceIO):
    service = ServiceString.PROFANITY
    required_input_fields = ["text"]
    optional_input_fields = []
    input_structure = {
        "text": str
    }

    output_structure = {
        "profanities": list,
        "offensive_probability": float,
        "offensive_prediction": bool
    }

