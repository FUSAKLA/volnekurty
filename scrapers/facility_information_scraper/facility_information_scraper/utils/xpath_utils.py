

def extract_string_from_path(path):
    return " ".join(path.select("text()").extract())