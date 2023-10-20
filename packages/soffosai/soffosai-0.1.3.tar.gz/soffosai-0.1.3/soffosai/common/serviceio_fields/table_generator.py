'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Table Generator Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TableGeneratorIO(ServiceIO):
    service = ServiceString.TABLE_GENERATOR
    required_input_fields = ["text","table_format"]
    optional_input_fields = ["topic"]
    input_structure = {
        "text": str, 
        "table_format": str, 
        "topic": str
    }

    output_structure = {
        "tables": dict
    }

