import re

file_path = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Container to allow X scrolling
# Look for the container div
content = content.replace(
    '<div class="overflow-hidden border border-gray-200 rounded-lg shadow-inner">',
    '<div class="overflow-x-auto border border-gray-200 rounded-lg shadow-inner">'
)

# 2. Update Headers
# We'll replace the entire <thead> block to be safe and clean
old_thead_pattern = r'<thead class="bg-gray-100 sticky top-0 z-10 shadow-sm">.*?</thead>'
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

content = re.sub(old_thead_pattern, new_thead, content, flags=re.DOTALL)

# 3. Update Data Rows
# We need to process each <tr> in the specific table.
# Let's extract the tbody first to narrow down
tbody_pattern = r'(<table class="min-w-full divide-y divide-gray-200 relative" id="base-baseTable">.*?<tbody>)(.*?)(</tbody>)'
match = re.search(tbody_pattern, content, re.DOTALL)

if match:
    prefix = match.group(1)
    tbody_content = match.group(2)
    suffix = match.group(3)
    
    # Now process rows inside tbody_content
    # We will use simple replacements for the td classes since they follow a pattern
    
    # 3.1. Name Column (Index 1) - The one with font-bold text-primary
    # old: <td class="px-6 py-4 text-sm font-bold text-primary">
    # new: <td class="px-6 py-4 text-sm font-bold text-primary min-w-[200px]">
    tbody_content = tbody_content.replace(
        '<td class="px-6 py-4 text-sm font-bold text-primary">',
        '<td class="px-6 py-4 text-sm font-bold text-primary min-w-[200px]">'
    )
    
    # 3.2. Region Column (Index 2) - This has a span inside.
    # The td wrapper is <td class="px-6 py-4 text-sm text-secondary">
    # BUT wait, the Type Column and Remarks column also use this class!
    # We must be specific.
    # Regex approach for each row is safer.
    
    def process_row(row_match):
        row_html = row_match.group(0)
        
        # Split into cells
        cells = re.split(r'(<td.*?>)', row_html)
        # cells[0] is empty or tr start
        # cells[1] is tag for col 0, cells[2] is content for col 0
        # cells[3] is tag for col 1, cells[4] is content for col 1 (Name)
        # cells[5] is tag for col 2, cells[6] is content for col 2 (Region)
        # cells[7] is tag for col 3, cells[8] is content for col 3 (Batch)
        # cells[9] is tag for col 4, cells[10] is content for col 4 (Type)
        # cells[11] is tag for col 5, cells[12] is content for col 5 (Remarks)
        
        # This splitting is fragile if content has nested <td> (unlikely here)
        # Let's try a strict findall of <td>...</td>
        
        # Better: just use specific regex for the cells we want to modify based on their content/structure known from generation
        
        # Region: contains <span ...>RegionName</span>. We want to make the TD whitespace-nowrap?
        # Actually, the region name is short (e.g. "南昌"), so wrapping isn't the issue.
        # But "南昌（南昌县）" might wrap. Let's add whitespace-nowrap to the TD.
        
        # The TD for region is: <td class="px-6 py-4 text-sm text-secondary">...</td>
        # The TD for type is: <td class="px-6 py-4 text-sm text-secondary">...</td>
        # The TD for remarks is: <td class="px-6 py-4 text-sm text-secondary italic">...</td>
        
        pass 
        return row_html

    # Let's regularize via string replacement since the generation code used specific strings
    
    # Batch Column: <td class="px-6 py-4 text-sm text-muted" title="...">...</td>
    tbody_content = tbody_content.replace(
        'class="px-6 py-4 text-sm text-muted"',
        'class="px-6 py-4 text-sm text-muted whitespace-nowrap"'
    )
    
    # Remarks Column: <td class="px-6 py-4 text-sm text-secondary italic">
    tbody_content = tbody_content.replace(
        'class="px-6 py-4 text-sm text-secondary italic"',
        'class="px-6 py-4 text-sm text-secondary italic min-w-[300px]"'
    )
    
    # For Region and Type, they share `class="px-6 py-4 text-sm text-secondary"`
    # But we want whitespace-nowrap on them.
    # Note: Name used `font-bold text-primary`, Batch used `text-muted`, Remarks used `text-secondary italic`.
    # So `text-secondary` is only used for Region and Type?
    # Let's check the generation script/output.
    # Region: `<td class="px-6 py-4 text-sm text-secondary"><span ...`
    # Type: `<td class="px-6 py-4 text-sm text-secondary"><span ...`
    # Yes. So we can safely replace that class string.
    
    tbody_content = tbody_content.replace(
        'class="px-6 py-4 text-sm text-secondary"',
        'class="px-6 py-4 text-sm text-secondary whitespace-nowrap"'
    )
    
    # Just to be sure, check if ID column uses it?
    # ID: `<td class="px-6 py-4 text-sm font-medium text-gray-500">` -> No.
    
    # Reassemble
    new_table_block = prefix + tbody_content + suffix
    content = content.replace(match.group(0), new_table_block)
    
    print("Table rows updated.")
else:
    print("Could not find table body.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
