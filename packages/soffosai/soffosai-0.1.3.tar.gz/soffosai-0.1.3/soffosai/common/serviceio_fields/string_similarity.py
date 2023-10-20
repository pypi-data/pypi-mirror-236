'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for String Similarity Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class StringSimilarityIO(ServiceIO):
    service = ServiceString.STRING_SIMILARITY
    required_input_fields = ["a","b"]
    optional_input_fields = []
    input_structure = {
        "a": str, 
        "b": str
    }

    output_structure = {
        "score": float,
        "text_spans": dict
    }

