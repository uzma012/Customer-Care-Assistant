

def prompt_text(file_content: str) -> str:

    prompt = """
    Extract the following information from the text below:
    - Customer Name
    - Contact Info (email or phone)
    - Order Number
    - Product Name
    - Date of Purchase
    - Date of Received
    - Issue Description
    - Preferred Resolution
    Inferred date of purchase correctly. If any information is missing, respond with "Not Provided" for that field. Format the output as a JSON object with the field names as keys. 
  
  Text:
    {file_content}

    """
    
    return prompt.format(file_content=file_content)