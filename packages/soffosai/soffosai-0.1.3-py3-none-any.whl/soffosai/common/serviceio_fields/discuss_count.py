'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Discuss Count Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussCountIO(ServiceIO):
    service = ServiceString.DISCUSS_COUNT
    required_input_fields = ["return_messages"]
    optional_input_fields = []
    input_structure = {
        "return_messages": bool
    }

    output_structure = {
        "sessions": list,
        "session_count": int
    }

