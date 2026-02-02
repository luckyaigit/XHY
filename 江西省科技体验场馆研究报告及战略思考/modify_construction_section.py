import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rename H3 "筹建关键要素" to "展品内容设计框架"
# <h3 ...><i ...></i>筹建关键要素</h3>
# We keep the icon or change it? The user didn't specify, but 'hammer' (筹建) might not fit 'Content'.
# '展品' might fit 'layer-group' or 'cubes'. 
# Let's just keep the text change for now to be safe, or minimize changes.
# Regex to find H3:
content = re.sub(
    r'(<h3[^>]*>\s*<i[^>]*></i>\s*)筹建关键要素(\s*</h3>)',
    r'\1展品内容设计框架\2',
    content
)

# 2. Remove Hardware Section and Grid
# We look for the Grid container: <div class="grid lg:grid-cols-2 gap-8">
# Inside, we have 2 columns.
# We want to remove the first column (Hardware) and the Grid class.
# And remove the H4 "展品内容设计框架" from the second column (since H3 is now that).

# Strategy:
# Find the specific block using unique string markers.
# Marker 1: <h4 class="text-lg font-semibold text-primary mb-4">硬件设施规划建议</h4>
# Marker 2: <h4 class="text-lg font-semibold text-primary mb-4">展品内容设计框架</h4>

# Locate the start of the grid.
# It is the parent of these markers.
# Since parsing HTML with regex is hard, I will use Python's string manipulation if the structure is consistent.

start_marker = '<div class="grid lg:grid-cols-2 gap-8">'
end_marker = '<!--' # Finding the end of the block might be tricky if not clearly marked.
# But we can look at the file content we viewed.
# The block ends before `<div class="bg-white rounded-2xl shadow-lg p-8">` (next section: 互动体验创新方向)
# Actually, the grid is inside `<div class="bg-white rounded-2xl shadow-lg p-8">` (Implementation Recommendations)

# Let's try to reconstruct the whole block content based on known lines.
# We viewed lines 4150-4300.
# The Grid starts around 4161.
# The Hardware Div starts 4162, ends 4191.
# The Content Div starts 4193.
# The Grid ends around 4246?

# Let's verify the lines again with strict file reading to be precise.
# Or use `replace` on the substring if we can uniquely identify the surrounding.

# I will assume the structure viewed is accurate.
# I'll read the file, find the line with `<div class="grid lg:grid-cols-2 gap-8">`,
# then find the line with `硬件设施规划建议` and the matching closing div.
# Instead of complex parsing, I can just replace the whole HTML chunk with the new simplified one.
# I will construct the New HTML Content for that block.

new_block_content = '''
                            <div class="mt-8">
                                <div class="bg-gradient-to-br from-indigo-50 to-purple-50 p-4 rounded-lg mb-4">
                                    <h5 class="font-semibold text-primary text-sm mb-3">金字塔三层架构</h5>
                                    <div class="space-y-3">
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3">
                                                基</div>
                                            <div>
                                                <div class="font-semibold text-primary text-xs">基础认知层 40%</div>
                                                <div class="text-secondary text-xs">AI发展历史、基本概念、原理演示</div>
                                            </div>
                                        </div>
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-indigo-500 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3">
                                                中</div>
                                            <div>
                                                <div class="font-semibold text-primary text-xs">应用体验层 35%</div>
                                                <div class="text-secondary text-xs">智能制造、医疗、农业、文化等应用</div>
                                            </div>
                                        </div>
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-indigo-400 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3">
                                                顶</div>
                                            <div>
                                                <div class="font-semibold text-primary text-xs">创造实践层 25%</div>
                                                <div class="text-secondary text-xs">机器人组装、AI模型训练、项目开发</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="bg-gradient-to-r from-red-50 to-orange-50 p-3 rounded-lg">
                                    <h5 class="font-semibold text-primary text-sm mb-2">江西特色融入建议</h5>
                                    <div class="space-y-1 text-xs text-secondary">
                                        <div class="flex items-center">
                                            <i class="fas fa-flag text-red-500 mr-2"></i>
                                            <span>"红色AI"：革命文献分析、苏区经济模型重建</span>
                                        </div>
                                        <div class="flex items-center">
                                            <i class="fas fa-leaf text-green-500 mr-2"></i>
                                            <span>"绿色AI"：鄱阳湖生态监测、稀土智能勘探</span>
                                        </div>
                                        <div class="flex items-center">
                                            <i class="fas fa-palette text-blue-500 mr-2"></i>
                                            <span>"古色AI"：书院智能教育、方言识别保护</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
'''
# Note: I replaced the `grid` div and its children with just a wrapper div (mt-8 for spacing)
# and the content of the second column (Pyramid + Jiangxi Features).
# I removed the H4 "展品内容设计框架" since H3 handles it.

# Now I need to identify the Range to Replace in the original file.
# Start: <div class="grid lg:grid-cols-2 gap-8"> (Line ~4161)
# End: Closing div of the grid. Line ~4246.
# How to find the closing div reliably?
# It's the div before the closing of `bg-white rounded-2xl` block.
# Which is followed by `<div class="bg-white rounded-2xl shadow-lg p-8">` (Next block).

# I'll use a regex to capture the whole grid block.
# pattern: <div class="grid lg:grid-cols-2 gap-8">.*?</div>\s*</div>\s*</div> (too risky)
# Better: Look for the specific H4 headers inside the block.

pattern_block = re.compile(
    r'(<div class="grid lg:grid-cols-2 gap-8">)([\s\S]*?)(</div>\s*</div>\s*</div>)', 
    # Validating the closing tags is hard.
    # Let's match from <div class="grid...> until "江西特色融入建议" block ends.
)

# Actually, I can use the `replace_file_content` tool since I know the exact content from `view_file`.
# But `replace_file_content` failed before on whitespace.
# I will use Python to do string replacement with exact matching from the file read.

# I'll define a start and end substring contained in the file.
start_str = '<div class="grid lg:grid-cols-2 gap-8">'
end_str = '<!--' # No...
# Look at line 4246: `</div>` closers.
# Text at end of block: `"古色AI"：书院智能教育、方言识别保护</span>`
# follows by closing divs.

# Let's read the file, find lines indices, slice and replace.
start_idx = -1
end_idx = -1
lines = content.splitlines()
for i, line in enumerate(lines):
    if '<div class="grid lg:grid-cols-2 gap-8">' in line:
        start_idx = i
    if '"古色AI"：书院智能教育、方言识别保护' in line:
         # The block ends a few lines after this.
         # Line 4241: span
         # Line 4242: div
         # Line 4243: div
         # Line 4244: div (col 2 end)
         # Line 4245: div (grid end)
         # Let's check the indentation/context in `view_file` output in step 531.
         # 4241: <span>...</span>
         # 4242: </div>
         # 4243: </div>
         # 4244: </div>
         # 4245: </div>
         # 4246: </div>
         # 4247: </div>
         # Wait, 4246 is the closing of "bg-white", 4247 is closing of "space-y-8"?
         # Let's be careful.
         # Start 4161.
         # Replace from 4161 to 4246?
         
         end_idx = i + 5 # Approximation based on 4241->4246
         
if start_idx != -1 and end_idx != -1:
    # Double check end_idx
    # We want to keep the outer container?
    # No, the grid is inside the H3 container.
    # Logic:
    # ... H3 ...
    # <div class="grid ...">  <-- Replace this
    # ...
    # </div> <!-- Grid end -->
    
    # Let's try to match the exact strings for start and end of the chunks we want to remove.
    pass

# Simplified Approach:
# Use `replace` on the substring identifying the Hardware Column and Grid wrapper.
# Remove: <div class="grid lg:grid-cols-2 gap-8">
# Remove: entire first column div.
# Remove: closing div of grid.

# Let's try to just build the new content from scratch and replace the whole `space-y-8` block? No, that's too big.
# Replace the `bg-white rounded-2xl shadow-lg p-8` block that contains "筹建关键要素".

block_pattern = re.compile(
    r'(<h3[^>]*>.*?筹建关键要素.*?</h3>\s*)(<div class="grid lg:grid-cols-2 gap-8">[\s\S]*?)(</div>\s*</div>\s*</div>)',
    re.IGNORECASE
)
# This is risky blindly.

# Precise Plan:
# 1. Read file lines.
# 2. Find line with `筹建关键要素`. Change text to `展品内容设计框架`.
# 3. Find line with `<div class="grid lg:grid-cols-2 gap-8">`.
# 4. Filter out lines from there until the line before `<div>... 金字塔三层架构 ...</div>` (Start of 2nd col) ??
#    No, 2nd col starts with `<div>` then `<h4 ...>展品内容设计框架</h4>`.
#    We want to keep the INNER content of 2nd col.
#    And discard 1st col.
# 5. Write back.

output_lines = []
skip = False
for line in lines:
    # 1. Title Rename
    if "筹建关键要素" in line:
        line = line.replace("筹建关键要素", "展品内容设计框架")
        
    # 2. Grid Start -> Start Skipping?
    # We want to remove the grid wrapper AND the first column.
    if '<div class="grid lg:grid-cols-2 gap-8">' in line:
        skip = True
        # We also need to inject the start of our new container?
        # Maybe just `<div class="mt-6">`
        output_lines.append('<div class="mt-6">') 
        continue
        
    if skip:
        # We are skipping the Grid Wrapper and First Column.
        # We need to detect when Second Column starts.
        # Second column starts with `<div>` and contains `展品内容设计框架` H4.
        if '展品内容设计框架' in line and '<h4' in line:
           # Found the H4 of 2nd col.
           # We stop skipping here? 
           # But we missed the opening `<div>` of the 2nd col.
           # And we want to Remove the H4 header too.
           # So we just continue skipping THIS line (the H4).
           # But we need to stop skipping generally.
           # Wait, checking `展品内容设计框架` H4 line is good anchor.
           # Lines before it was the `<div>`.
           pass
           
        if '金字塔三层架构' in line:
           # This is definitely inside 2nd col.
           # If we are strictly skipping, we need to turn it off.
           # And we want to capture everything from here onwards.
           skip = False
           # But we need to close the `div` we opened?
           # Depending on how many divs were closed at the end.
           output_lines.append(line)
           continue
           
    if not skip:
        # Normal copying
        # We need to handle the closing tags of the grid?
        # The grid had one closing div `</div>` at the end of the block.
        # Since we removed the opening `<div class="grid...`, we must remove one `</div>`.
        # How to detect the specific closing div?
        # It's the one after "古色AI" block closing.
        # This is tricky line-by-line.
        output_lines.append(line)

# This line-by-line logic is error prone without a state machine.

# Alternative:
with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Rename H3
text = text.replace('筹建关键要素', '展品内容设计框架')

# 2. Remove Grid and Hardware Col
# HTML is:
# <div class="grid lg:grid-cols-2 gap-8">
#    <div> ...Hardware... </div>
#    <div> ...Content... </div>
# </div>

# We want:
# <div class="space-y-6"> ...Content (without H4)... </div>

# Let's match the Hardware Block using H4.
# Regex to remove:
# <div>\s*<h4 ...>硬件设施规划建议</h4>[\s\S]*?</div>(\s*<div>)
# And remove the wrapping Grid div.

# Let's replace the whole grid block with processed content.
# I will construct the regex to match the Grid Block and extract the Content part.
pattern = re.compile(
    r'<div class="grid lg:grid-cols-2 gap-8">[\s\S]*?<h4[^>]*>硬件设施规划建议</h4>[\s\S]*?</div>(\s*<div>)\s*<h4[^>]*>展品内容设计框架</h4>([\s\S]*?)</div>\s*</div>',
    re.MULTILINE
)
# This assumes the closing divs match up.
# The grid ends with `</div>` (for grid)
# The 2nd col ends with `</div>` (for col)
# So `</div>\s*</div>` matches end of col and end of grid.

def replacer(match):
    # match.group(2) is the content of the 2nd col (Pyramid + Jiangxi)
    # We wrap it in a div if needed.
    return f'<div class="mt-6">{match.group(2)}</div>'

# Note: The pattern needs to be very accurate.
# <div class="grid..."> (Open Grid)
#   <div> (Open Col 1)
#     ...Hardware...
#   </div> (Close Col 1)
#   <div> (Open Col 2)   <-- Group 1 captures this `<div>`? No, `\s*<div>`
#     <h4>Content</h4>
#     ...Group 2...
#   </div> (Close Col 2)
# </div> (Close Grid)

# Refined Pattern:
# 1. Grid Start
# 2. Col 1 (non-greedy until Col 2 Start)
# 3. Col 2 Start (<div> ... <h4>Content</h4>)
# 4. Col 2 Content (Group)
# 5. Col 2 End + Grid End (</div> </div>)

regex = r'(<div class="grid lg:grid-cols-2 gap-8">\s*<div>\s*<h4[^>]*>硬件设施规划建议</h4>[\s\S]*?</div>\s*<div>\s*<h4[^>]*>展品内容设计框架</h4>)([\s\S]*?)(</div>\s*</div>)'

# Let's try to match and replace.
text_new = re.sub(regex, r'<div class="mt-6">\2</div>', text, count=1)

if text == text_new:
    print("Regex match failed. Falling back to simple replacement?")
    # Fallback: Just string literals if we are sure of indentation.
    # But indentation is variable.
    # Print failure to let me know.
    pass
else:
    text = text_new

# 3. Update TOC (using H2/H3 scan)
# Since we renamed H3 to "展品内容设计框架", the TOC update script logic (scanning H3 tags) should automatically pick up the new name
# IF we run the TOC regeneration.
# I will incorporate TOC regeneration here.

# Scan TOC logic (same as before)
toc_items = []
current_h2 = None
h2_pattern = re.compile(r'<section[^>]+id="([^"]+)"')
h_tag_pattern = re.compile(r'<(h[23])[^>]*?(?:id="([^"]*)")?[^>]*>(.*?)</\1>')
# Simplified scan:
# Because structure is strictly <section id..><h2..> for H2
# And <h3 id..> for H3 (maybe)

# Actually, I'll just use the `update_toc_and_title.py` logic again or call it.
# To be self-contained:
nav_start = text.find('<nav class="toc-fixed">')
nav_end = text.find('</nav>', nav_start) + 6
# Only if we successfully updated the text.

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Updated content.")
