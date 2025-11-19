
import json
from datetime import datetime
from pathlib import Path
import json
from .customer import Customer, Order, Issue, Case



def generate_json(extracted_text: str) -> dict:
    import json
    try:
        data = json.loads(extracted_text)
        customer = Case(            
            customer= Customer(name=data.get("Customer Name"), 
                               contact=data.get("Contact Info")),

            order= Order(number=data.get("Order Number"), 
                         product_name=data.get("Product Name"), 
                         purchase_date=data.get("Date of Purchase"),
                         received_date=data.get("Date of Received")),

            issue= Issue(description=data.get("Issue Description"), 
                         preferred_resolution=data.get("Preferred Resolution"))
        )

        output_file = Path(r"output/intake_payload.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        json_text= json.dumps(customer.to_dict(), indent=4)
        print(json_text)
        output_file.write_text(json_text)
        return json_text
    
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return {"error": "Invalid JSON format"} 
