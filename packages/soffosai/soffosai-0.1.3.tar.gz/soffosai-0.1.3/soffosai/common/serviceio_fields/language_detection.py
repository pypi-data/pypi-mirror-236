'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Language Detection Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class LanguageDetectionIO(ServiceIO):
    service = ServiceString.LANGUAGE_DETECTION
    required_input_fields = ["text"]
    optional_input_fields = []
    input_structure = {
        "text": str
    }

    output_structure = {
        "language": dict
    }

