'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for N E R Service
-----------------------------------------------------
'''

from .service_io import ServiceIO
from ..constants import ServiceString


class NERIO(ServiceIO):
    service = ServiceString.N_E_R
    required_input_fields = ["text"]
    optional_input_fields = ["labels"]
    input_structure = {
        "text": str, 
        "labels": dict
    }

    output_structure = {
        "named_entities": list,
        "entity_counts": list
    }

