from os import path

BASEPATH = path.dirname(__file__).removesuffix("src")
SRCPATH = path.join(BASEPATH, "src")
ENVPATH = path.join(BASEPATH, ".env")