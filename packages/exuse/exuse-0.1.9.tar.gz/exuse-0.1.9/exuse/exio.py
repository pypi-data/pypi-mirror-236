import json
from collections import OrderedDict


def load_json(fp: str):
    """read json from a file"""
    with open(fp) as rd:
        return json.load(rd)


def dump_json(obj, fp: str, indent=4):
    """save json to a file"""
    with open(fp, "w") as wt:
        json.dump(obj, wt, indent=indent)


def read_jsonlike_file(fp: str):
    "根据文件扩展名自动读取文件内容"
    if fp.endswith("toml"):
        import toml

        return toml.load(fp)
    elif fp.endswith("yaml"):
        import yaml

        with open(fp) as r:
            return yaml.load(r)
    elif fp.endswith("json"):
        import json

        with open(fp) as r:
            return json.load(r)
    else:
        raise ValueError(f"Unsupported file extension: {fp.split('.')[-1]}")


def read_file(fp: str) -> str:
    with open(fp) as r:
        return r.read().strip()


def write(text: str, fp: str) -> None:
    with open(fp, "w") as w:
        w.write(text)


def readline(reader):
    """读取一行，但不包括末尾换行符"""
    content = reader.readline()
    if isinstance(content, bytes):
        return content.decode("utf-8").rstrip("\n")
    return content.rstrip("\n")


def read_tsv(file_reader, sep="\t", row_handler=None):
    if isinstance(file_reader, str):
        file_reader = open(file_reader)

    data = []
    headers = readline(file_reader).split(sep)
    while line := readline(file_reader):
        if line and (values := line.split(sep)):
            row = OrderedDict({k: v for k, v in zip(headers, values)})
            if row_handler:
                row = row_handler(row, headers=headers)
            data.append(row)

    file_reader.close()
    return data
