def save_text_to_file(text, path="./sample/sample.html", encoding="utf8"):
    with open(path, "w", encoding=encoding) as f:
        f.write(text)