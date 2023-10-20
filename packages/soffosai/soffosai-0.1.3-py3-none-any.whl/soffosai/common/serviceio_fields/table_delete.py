'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Table Delete Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TableDeleteIO(ServiceIO):
    service = ServiceString.TABLE_DELETE
    required_input_fields = ["table_ids"]
    optional_input_fields = []
    input_structure = {
        "table_ids": list
    }

    output_structure = {
        "success": bool
    }

