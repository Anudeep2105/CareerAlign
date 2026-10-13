from typing import List, Dict, Any

class PIIFilter:
    def __init__(self, disabled_fields: List[str] = None):
        self.disabled_fields = disabled_fields or []

    def filter_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        filtered_data = data.copy()
        
        # Handle contact details PII
        if "contact_details" in filtered_data:
            contact = filtered_data["contact_details"].copy()
            for field in self.disabled_fields:
                if field in contact:
                    contact[field] = "[REDACTED]"
            filtered_data["contact_details"] = contact
            
        return filtered_data
