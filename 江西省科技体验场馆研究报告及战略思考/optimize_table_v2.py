
import os

file_path = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Container
content = content.replace(
    '<div class="overflow-hidden border border-gray-200 rounded-lg shadow-inner">',
    '<div class="overflow-x-auto border border-gray-200 rounded-lg shadow-inner">'
)

# 2. Find the Base Table
table_marker = 'id="base-baseTable"'
start_idx = content.find(table_marker)

if start_idx == -1:
    print("Error: Could not find base table.")
    exit(1)

# Find the end of the table
end_idx = content.find('</table>', start_idx)
if end_idx == -1:
    print("Error: Could not find table end.")
    exit(1)

table_content = content[start_idx:end_idx]

# 3. Update Headers (inside table_content)
# We can replace the <thead> block.
old_thead_start = table_content.find('<thead')
old_thead_end = table_content.find('</thead>') + 8

if old_thead_start != -1:
    new_thead = """<thead class="bg-gray-100 sticky top-0 z-10 shadow-sm">
                                    <tr>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider whitespace-nowrap w-16">序号</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider min-w-[200px]">基地名称</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider whitespace-nowrap w-32">所属地区</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider whitespace-nowrap w-40">认定批次</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider whitespace-nowrap w-32">基地类型</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider min-w-[300px]">备注</th>
                                    </tr>
                                </thead>"""
    # Replace the thead in table_content
    # Note: need to handle potential indentation in original file if we want to be clean, 
    # but regex replace of the block is easier.
    import re
    table_content = re.sub(r'<thead.*?</thead>', new_thead, table_content, flags=re.DOTALL)
else:
    print("Warning: Could not find thead.")

# 4. Update Body Rows (inside table_content)
# Name
table_content = table_content.replace(
    '<td class="px-6 py-4 text-sm font-bold text-primary">',
    '<td class="px-6 py-4 text-sm font-bold text-primary min-w-[200px]">'
)
# Region and Type
table_content = table_content.replace(
    '<td class="px-6 py-4 text-sm text-secondary">',
    '<td class="px-6 py-4 text-sm text-secondary whitespace-nowrap">'
)
# Batch (prefix match)
table_content = table_content.replace(
    '<td class="px-6 py-4 text-sm text-muted"',
    '<td class="px-6 py-4 text-sm text-muted whitespace-nowrap"'
)
# Remarks
table_content = table_content.replace(
    '<td class="px-6 py-4 text-sm text-secondary italic">',
    '<td class="px-6 py-4 text-sm text-secondary italic min-w-[300px]">'
)

# 5. Reconstruct full content
new_content = content[:start_idx] + table_content + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Table optimized successfully.")
