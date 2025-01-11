def log_message(message):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"{message}\n")

def format_data(data):
    return {key: str(value) for key, value in data.items()}

def calculate_percentage(part, whole):
    if whole == 0:
        return 0
    return (part / whole) * 100