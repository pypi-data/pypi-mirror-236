'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Table Get Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TableGetIO(ServiceIO):
    service = ServiceString.TABLE_GET
    required_input_fields = []
    optional_input_fields = []
    input_structure = {

    }

    output_structure = {
        "tables": list
    }

