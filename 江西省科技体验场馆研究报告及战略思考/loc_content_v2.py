import sys

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"
log_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\loc_log.txt"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

with open(log_file, 'w', encoding='utf-8') as log:
    # Find all occurrences of "清单"
    search_term = "清单"
    start = 0
    found = False
    while True:
        pos = content.find(search_term, start)
        if pos == -1:
            break
        found = True
        line_no = content.count('\n', 0, pos) + 1
        snippet = content[pos-50:pos+150].replace('\n', ' ')
        log.write(f"Found '{search_term}' at line {line_no}: ...{snippet}...\n")
        start = pos + 1

    if not found:
        log.write(f"Search term '{search_term}' not found.\n")

    # Also search for the ID
    search_term = 'id="integration-recommendations"'
    pos = content.find(search_term)
    if pos != -1:
        line_no = content.count('\n', 0, pos) + 1
        log.write(f"Found '{search_term}' at line {line_no}\n")
    else:
        log.write(f"ID '{search_term}' not found.\n")
