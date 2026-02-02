import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

# 1. Update Title and Footer Punctuation
# Old: ...筹建与资源整合设想
# New: ...筹建、资源整合设想

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace in <title>
content = re.sub(
    r'<title>(.*?)(筹建与资源整合设想)(.*?)</title>',
    r'<title>\1筹建、资源整合设想\3</title>',
    content
)

# Replace in Footer H3
# <h3 id="integration-recommendations-1" class="...">...筹建与资源整合设想...</h3>
content = re.sub(
    r'(<h3[^>]*>[\s\S]*?)筹建与资源整合设想([\s\S]*?</h3>)',
    r'\1筹建、资源整合设想\2',
    content
)


# 2. Regenerate TOC
# Parse H2 and H3
# Structure:
# <nav class="toc-fixed">
#    <h3 ...>目录</h3>
#    <ul ...>
#       <li>
#           <a href="#id">H2 Title</a>
#           <ul ...>
#               <li><a href="#subid">H3 Title</a></li>
#           </ul>
#       </li>
#    </ul>
# </nav>

# Find all H2 and H3
# We need to capture ID and Content.
# Regex for H2: <section[^>]*id="([^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>
# Regex for H3: <h3[^>]*id="([^"]+)"[^>]*>(.*?)</h3> or <div id="([^"]+)" ...><h3 ...>(.*?)</h3>?
# The file structure seems to use:
# Section ID -> H2 inside section
# H3 inside section often has ID on the H3 tag itself? Or generated ID?

# Let's simple scan for IDs and Headers.
# Most reliable way given the file structure:
# Scan document order.
# Match <section id="..."> ... <h2 ...>
# Match <h3 id="..."> ... </h3>  (The previous script added IDs to H3s)
# OR match <h3 ...> ... </h3> and check if previous line or parent has ID?

# Actually, the file uses <section id="XYZ"> ... <h2>TITLE</h2> ...
# And for H3: <h3 id="XYZ-1">TITLE</h3> (based on previous turns)

# Let's extract them in order.
headers = []
# We iterate through the file looking for matches.
# But regex findall on the whole content might lose hierarchy if not careful.
# However, H2s are main sections. H3s come after H2.

# Let's find all H2 and H3 with their IDs.
# We assume H2 is ` <h2 ...> ... </h2>` inside a `<section id="...">`
# But verifying the exact pattern:
# Section: <section id="provincial-core" ...> ... <h2 ...> <span ...> TITLE </span> </h2>
# The ID is on the section.
# The previous scripts might have made sure of this.

# Let's just Regex for all tags relevant.
# We need execution order.

# Pattern for Section Start: <section id="(\w+)"
# Pattern for H2: <h2 ...>(.*?)</h2>
# Pattern for H3: <h3 ... id="([\w-]+)" ...>(.*?)</h3>  <-- Note: H3 has ID directly on it now?
# Or maybe the ID is elsewhere? Let's check the previous `reorganize_toc.py` logic if possible, or just assume standard.
# Looking at file view:
# <h3 id="integration-recommendations-1" class="text-2xl font-serif font-bold mb-2">

# So H3 has ID.
# H2 is typically:
# <section id="base-overview" ...> ... <h2>...</h2>
# So for H2, we take the ID from the preceding <section> tag.

toc_items = []
current_h2 = None

# We can parse looking for tags.
# This approach with regex on big string is slightly fragile but workable if patterns are consistent.

# Let's use a tokenizer approach or just `re.finditer` with multiple patterns combined?
# Regex: (<section[^>]+id="([^"]+)")|(<h2[^>]*>([\s\S]*?)</h2>)|(<h3[^>]+id="([^"]+)"[^>]*>([\s\S]*?)</h3>)

pattern = re.compile(
    r'(<section[^>]+id="([^"]+)")|'  # Group 1,2: Section ID
    r'(<h2[^>]*>([\s\S]*?)</h2>)|'    # Group 3,4: H2 Content
    r'(<h3[^>]*id="([^"]+)"[^>]*>([\s\S]*?)</h3>)', # Group 5,6,7: H3 ID, H3 Content
    re.IGNORECASE
)

last_section_id = None

for match in pattern.finditer(content):
    if match.group(1): # Section ID
        last_section_id = match.group(2)
    elif match.group(3): # H2
        # Clean tags from Title
        raw_title = match.group(4)
        # Remove tags
        clean_title = re.sub(r'<[^>]+>', '', raw_title).strip()
        if last_section_id and clean_title and clean_title != "执行摘要" and "目录" not in clean_title:
             # Add H2
             toc_items.append({
                 'level': 2,
                 'id': last_section_id,
                 'title': clean_title,
                 'children': []
             })
             current_h2 = toc_items[-1]
    elif match.group(5): # H3
        h3_id = match.group(6)
        raw_title = match.group(7)
        clean_title = re.sub(r'<[^>]+>', '', raw_title).strip()
        
        # Filter out Footer H3 which might match. "南昌鲸鱼..." title in footer is H3.
        # Footer ID is integration-recommendations-1 (wait, that is an ID!)
        # But if it's the Footer Title, we might not want it in TOC?
        # The Footer H3 ID "integration-recommendations-1" looks like a TOC item ID!
        # Let's check if the footer H3 is actually INTENDED to be in TOC?
        # In the file view:
        # <h3 id="integration-recommendations-1" ...>
        # This ID suggests it WAS part of the TOC logic previously (auto-generated ID).
        # But if it's the FOOTER title, should it be in TOC? Prior TOC (line 330) shows:
        # 13.1 江西省科技体验场馆深度调研报告 (integration-recommendations-1)
        # Verify if "南昌鲸鱼..." (the new title) replaced that text?
        # The user's manual edit in the footer:
        # <h3 id="integration-recommendations-1" ...>南昌鲸鱼...</h3>
        # So yes, the footer title IS the target of that ID.
        # If the user renamed it, the TOC should reflect the new name.
        
        if h3_id and clean_title and current_h2:
            current_h2['children'].append({
                'level': 3,
                'id': h3_id,
                'title': clean_title
            })

# Build HTML
toc_html = '<nav class="toc-fixed">\n        <h3 class="text-base font-bold text-primary mb-3 border-b border-gray-200 pb-2">目录</h3>\n        <ul class="space-y-1 text-xs max-h-[calc(100vh-8rem)] overflow-y-auto pr-2">\n'

for item in toc_items:
    toc_html += f'            <li>\n                <a href="#{item["id"]}"\n                    class="text-primary hover:text-accent transition-colors block py-0.5">{item["title"]}</a>\n'
    toc_html += '            </li>\n'

toc_html += '        </ul>\n    </nav>'

# Replace TOC in content
# Regex for existing TOC: <nav class="toc-fixed"> ... </nav>
content = re.sub(
    r'<nav class="toc-fixed">.*?</nav>',
    toc_html,
    content,
    flags=re.DOTALL
)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Title and TOC updated.")
