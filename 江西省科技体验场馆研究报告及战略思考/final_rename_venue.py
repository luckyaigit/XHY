import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "南昌鲸鱼" with "鲸鱼" everywhere to be safe and consistent.
updated_content = content.replace("南昌鲸鱼", "鲸鱼")

if content != updated_content:
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Replaced '南昌鲸鱼' with '鲸鱼'.")
else:
    print("No instances of '南昌鲸鱼' found.")
