from pathlib import Path


def read(Path):
    try:
        cache = open(Path, "r", encoding='utf-8')
        msg = cache.read()
        cache.close()
        return msg
    except:
        return False

def write(Path, msg):
    with open(Path, mode="w") as cache:
        try:
            return cache.write(msg)
        except:
            return False
