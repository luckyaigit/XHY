import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Broad replace for the main title with possible line breaks/spaces
# We want to replace "南昌鲸鱼" with "鲸鱼" within the specific context.
# Or just replace all "南昌鲸鱼" with "鲸鱼"?
# The user's request is specific to the title, but usually consistency is better.
# Let's check for "南昌鲸鱼" occurrences.

# The user specifically asked to change:
# 江西省科技体验场馆调研与南昌鲸鱼 AI 机器人科技体验馆筹建、资源整合设想
# TO
# 江西省科技体验场馆调研与鲸鱼 AI 机器人科技体验馆筹建、资源整合设想

# We can use a regex that matches the split parts.
pattern = re.compile(r'江西省科技体验场馆调研与\s*南昌鲸鱼\s*AI 机器人科技体验馆筹建、资源整合设想', re.MULTILINE)
content = pattern.sub('江西省科技体验场馆调研与鲸鱼 AI 机器人科技体验馆筹建、资源整合设想', content)

# Also check for variations in the title (like with a dot or slash instead of comma)
# But standardizing on the user's provided string is best.

# Let's also do a general replace for "南昌鲸鱼 AI 机器人科技体验馆" -> "鲸鱼 AI 机器人科技体验馆"
content = content.replace('南昌鲸鱼 AI 机器人科技体验馆', '鲸鱼 AI 机器人科技体验馆')
content = content.replace('南昌鲸鱼AI机器人科技体验馆', '鲸鱼AI机器人科技体验馆') # no space
content = content.replace('南昌鲸鱼AI机器人科技馆', '鲸鱼AI机器人科技馆')

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete.")
