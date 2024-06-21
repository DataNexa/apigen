from config.config import config
from reader.reader import reader
from gen.generate  import generate
conf = config()
reader(conf)
generate(conf)
# print(conf.toString())