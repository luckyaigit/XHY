import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

new_title = "南昌鲸鱼AI机器人科技馆筹建与资源整合设想"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the H1 block
# We look for <h1 ...> ... </h1>
# The content inside H1 in the file is complex (spans, br), so we use DOTALL
# We identify it by the class content or some unique substring if possible.
# Unique substring: "科普基地发展研究综合报告"

pattern = re.compile(
    r'(<h1[^>]*>)(.*?)(</h1>)',
    re.DOTALL | re.IGNORECASE
)

def replace_title(match):
    # Check if this is the Hero H1. It contains "江西省科技体验场馆与AI" or "科普基地发展研究综合报告"
    text = match.group(2)
    if "科普基地发展研究综合报告" in text or "江西省科技体验场馆与AI" in text:
        # Rebuild H1 with new content
        # Maintain the span class for gradient text
        new_inner = f'''
                        <span
                            class="gradient-text bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">{new_title}</span>
'''
        return match.group(1) + new_inner + match.group(3)
    return match.group(0)

new_content = pattern.sub(replace_title, content, count=1)

if content != new_content:
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Title updated successfully.")
else:
    print("Title not found or already updated.")
