'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Search Recommendations Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class SearchRecommendationsIO(ServiceIO):
    service = ServiceString.SEARCH_RECOMMENDATIONS
    required_input_fields = ["text","document_ids"]
    optional_input_fields = []
    input_structure = {
        "text": str, 
        "document_ids": list
    }

    output_structure = {
        "recommendations": dict,
        "recommendations_no_info": dict
    }

