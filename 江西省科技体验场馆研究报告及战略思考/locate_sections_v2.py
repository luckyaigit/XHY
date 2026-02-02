filename = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
for i, line in enumerate(lines):
    if "硬件设施规划建议" in line:
        output.append(f"Hardware Section found at line {i+1}: {line.strip()}")
    if "展品内容设计框架" in line:
        output.append(f"Content Framework found at line {i+1}: {line.strip()}")

with open("section_locations.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
