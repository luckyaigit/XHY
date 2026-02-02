import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

new_title = "江西省科技体验场馆调研与南昌鲸鱼 AI 机器人科技体验馆筹建与资源整合设想"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update <title>
content = re.sub(
    r'<title>.*?</title>',
    f'<title>{new_title}</title>',
    content,
    flags=re.DOTALL
)

# 2. Update Hero H1
# The previous script might have left it as:
# <h1 ...> <span ... class="gradient-text ...">南昌鲸鱼AI机器人科技馆筹建与资源整合设想</span> </h1>
# We need to target the text inside the gradient-text span more robustly
# Or just reconstruct the whole H1 block again.

# Let's find the gradient span content
pattern_h1 = re.compile(
    r'(<span[^>]*class="gradient-text[^>]*>)(.*?)(</span>)',
    re.DOTALL
)

# We can replace the content of that span.
# But "南昌鲸鱼AI机器人...设想" is current text.
# We replace ANY text inside that specific gradient span with new title.
# WE BE CAREFUL not to match other gradient texts if any.
# The class 'bg-clip-text' is quite specific in this context.

def replace_h1_text(match):
    return match.group(1) + new_title + match.group(3)

content = pattern_h1.sub(replace_h1_text, content, count=1) 
# Assumes the first gradient text is the Title. Hero section is at top, so likely yes.

# 3. Update Footer H3
# <h3 id="integration-recommendations-1" class="...">南昌鲸鱼AI机器人科技馆筹建与资源整合设想</h3>
pattern_footer = re.compile(
    r'(<h3[^>]*id="integration-recommendations-1"[^>]*>)(.*?)(</h3>)',
    re.DOTALL | re.IGNORECASE
)

def replace_footer_text(match):
     return match.group(1) + f"\n                        {new_title}\n                    " + match.group(3)

content = pattern_footer.sub(replace_footer_text, content, count=1)


with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated title to: {new_title}")
