def save_text_to_file(text, path="./sample/log.txt", encoding="utf8"):
    with open(path, "w", encoding=encoding) as f:
        f.write(text)
