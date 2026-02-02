target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"
with open(target_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if "修水" in line:
            print(f"Line {i+1}: {line.strip()}")
