import sys

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of "清单" or "资源进行整合"
search_term = "清单"
start = 0
found = False
while True:
    pos = content.find(search_term, start)
    if pos == -1:
        break
    found = True
    # Get line number
    line_no = content.count('\n', 0, pos) + 1
    # Get snippet
    snippet = content[pos-50:pos+150].replace('\n', ' ')
    print(f"Found '{search_term}' at line {line_no}: ...{snippet}...")
    start = pos + 1

if not found:
    print(f"Search term '{search_term}' not found.")

# Also search for the ID
search_term = 'id="integration-recommendations"'
pos = content.find(search_term)
if pos != -1:
    line_no = content.count('\n', 0, pos) + 1
    print(f"Found '{search_term}' at line {line_no}")
else:
    print(f"ID '{search_term}' not found.")
