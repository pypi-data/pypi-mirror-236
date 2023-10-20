'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Documents Delete Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DocumentsDeleteIO(ServiceIO):
    service = ServiceString.DOCUMENTS_DELETE
    required_input_fields = ["document_ids"]
    optional_input_fields = []
    input_structure = {
        "document_ids": list
    }

    output_structure = {
        "success": bool
    }

