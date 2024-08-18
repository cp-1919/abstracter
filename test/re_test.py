import re

a = '```json\n{  {\n  "mem.read": [\n    {"note": "万物归一", "content": "Everything is one."}\n  ]\n}\n```'
res = re.findall(r'```json\n((.|\n)*?)\n```', a)[0]
print(res)