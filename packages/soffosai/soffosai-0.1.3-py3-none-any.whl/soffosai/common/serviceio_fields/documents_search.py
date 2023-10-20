'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Documents Search Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class DocumentsSearchIO(ServiceIO):
    service = ServiceString.DOCUMENTS_SEARCH
    required_input_fields = []
    optional_input_fields = ["query","document_ids","top_n_keyword","top_n_natural_language","filters","date_from","date_until"]
    input_structure = {
        "query": str, 
        "document_ids": list, 
        "top_n_keyword": int, 
        "top_n_natural_language": int, 
        "filters": dict, 
        "date_from": str, 
        "date_until": str
    }

    output_structure = {
        "items": list
    }

