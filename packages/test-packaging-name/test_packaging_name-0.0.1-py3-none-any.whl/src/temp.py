from utils.fileparse import FileParserFactory

path = './etc/sample.json'

parser_fatctory = FileParserFactory()
parse = parser_fatctory.create_parser(path)
data = parse.parse(path)

print(data)