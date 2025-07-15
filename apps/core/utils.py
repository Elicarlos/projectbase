import uuid


def unique_filename(instance, filename):
    ext = filename.split(".")[-1]
    return f"{uuid.uuid4()}.{ext}"
