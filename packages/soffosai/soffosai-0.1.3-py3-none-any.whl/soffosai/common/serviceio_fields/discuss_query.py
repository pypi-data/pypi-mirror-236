'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Discuss Query Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DiscussQueryIO(ServiceIO):
    service = ServiceString.DISCUSS_QUERY
    required_input_fields = ["query"]
    optional_input_fields = []
    input_structure = {
        "query": str
    }

    output_structure = {
        "response": str,
        "context": str,
        "messages": list
    }

