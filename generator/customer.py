from datetime import datetime
class Customer:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    def to_dict(self):
        return {"name": self.name, "contact": self.contact}

class Order:
    def __init__(self, number, product_name, purchase_date, received_date):
        self.number = number
        self.product_name = product_name
        self.purchase_date = purchase_date
        self.received_date = received_date

    def to_dict(self):
        return {
            "number": self.number,
            "product_name": self.product_name,
            "purchase_date": self.purchase_date,
            "received_date": self.received_date
        }

class Issue:
    def __init__(self, description, preferred_resolution):
        self.description = description
        self.preferred_resolution = preferred_resolution

    def to_dict(self):
        return {
            "description": self.description,
            "preferred_resolution": self.preferred_resolution
        }

class Case:
    def __init__(self, customer: Customer, order: Order, issue: Issue):
        self.customer = customer
        self.order = order
        self.issue = issue
        self.source = "transcript_parser"
        self.created_at = datetime.now()
        self.case_id = self.generate_case_id()

    @staticmethod
    def generate_case_id(counter: int = 1) -> str:
        today_str = datetime.now().strftime("%Y%m%d")
        case_id = f"CS-{today_str}-{counter:04d}"
        return case_id

    def to_dict(self):
        return {
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "case_id": self.case_id,
            "customer": self.customer.to_dict(),
            "order": self.order.to_dict(),
            "issue": self.issue.to_dict()
        }