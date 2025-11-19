import os

def load_file(file_path):
    try:
        if hasattr(file_path, "read"):
            raw = file_path.read()
            if isinstance(raw, bytes):
                try:
                    content = raw.decode("utf-8")
                except UnicodeDecodeError:
                    content = raw.decode("latin-1", errors="replace")
            else:
                content = str(raw)
            print(content)
            return preprocess_text(content)

        if isinstance(file_path, str):
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                except UnicodeDecodeError:
                    with open(file_path, "r", encoding="latin-1", errors="replace") as file:
                        content = file.read()
                print(content)
                return preprocess_text(content)
            return preprocess_text(file_path)

        print("Unsupported input type")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def preprocess_text(text):
    text =text.lower()
    text = text.replace('\r\n', '\n')  
    text = text.replace('[agent]', '')
    text = text.replace('[customer]', '')
    text = text.replace(':', '')
    return text.strip()