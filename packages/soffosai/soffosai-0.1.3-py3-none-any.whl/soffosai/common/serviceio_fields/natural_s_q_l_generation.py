'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Updated at: 2023-10-09
Purpose: Input/Output description for Natural S Q L Generation Service
-----------------------------------------------------
'''
from .service_io import ServiceIO
from ..constants import ServiceString


class NaturalSQLGenerationIO(ServiceIO):
    service = ServiceString.NATURAL_S_Q_L_GENERATION
    required_input_fields = []
    optional_input_fields = ["query","messages","tables","notes","classify_tables","table_prefix","table_aliases","boost"]
    input_structure = {
        "query": str, 
        "messages": list, 
        "tables": list, 
        "notes": list, 
        "classify_tables": bool, 
        "table_prefix": str, 
        "table_aliases": list, 
        "boost": bool
    }

    output_structure = {
        "messages": list,
        "boost": bool,
        "sql": str,
        "sql_count": str
    }


    @classmethod
    def special_validation(self, payload):
        
        if payload.get('query') and payload.get('messages'):
            return False, 'Only one of "messages" and "query" can be provided.'
        if not payload.get('query') and not payload.get('messages'):
            return False, 'Please provide either "messages" or "query".'

        return super().special_validation(payload)
