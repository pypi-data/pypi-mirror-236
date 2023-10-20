'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Table Ingest Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class TableIngestIO(ServiceIO):
    service = ServiceString.TABLE_INGEST
    required_input_fields = ["table","document_name","description"]
    optional_input_fields = []
    input_structure = {
        "table": list, 
        "document_name": str, 
        "description": str
    }

    output_structure = {
        "table_id": str
    }

