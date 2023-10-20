'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Discuss Delete Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussDeleteIO(ServiceIO):
    service = ServiceString.DISCUSS_DELETE
    required_input_fields = []
    optional_input_fields = ["session_ids"]
    input_structure = {
        "session_ids": list
    }

    output_structure = {
        "success": bool
    }

