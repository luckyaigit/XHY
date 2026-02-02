import re
import os

source_path = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科普教育基地（2024-2026年）调研报告\江西省科普教育基地可视化分类.html"
output_path = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\insert_content.html"

try:
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Section 1: Summary Table
    table1_match = re.search(r'<h2>一、核心数据维度统计</h2>\s*<table>(.*?)</table>', content, re.DOTALL)
    table1_content = table1_match.group(1) if table1_match else ""

    # Extract Section 3: Full Table Rows
    tbody_match = re.search(r'<table class="data-table" id="baseTable">.*?<tbody>(.*?)</tbody>', content, re.DOTALL)
    tbody_content = tbody_match.group(1) if tbody_match else ""

    # Build New HTML with Tailwind
    html = """
    <!-- Section 1.3: Overview of Science Education Bases -->
    <section id="base-overview" class="py-20 bg-gray-50">
        <div class="container mx-auto px-6">
            <h2 class="text-4xl font-serif font-bold text-primary mb-12 text-center">
                <span class="border-b-4 border-accent pb-2">1.3 江西省科普教育基地整体发展概况</span>
            </h2>

            <!-- Part 1: Core Data Stats -->
            <div class="mb-16">
                <h3 class="text-2xl font-bold text-primary mb-8 flex items-center">
                    <i class="fas fa-chart-pie text-accent mr-3"></i>核心数据统计
                </h3>
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="p-4 font-semibold text-primary border-b w-1/4">分类维度</th>
                                <th class="p-4 font-semibold text-primary border-b">核心类别及数量</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
    """
    
    # Process Table 1 rows
    rows1 = re.findall(r'<tr>(.*?)</tr>', table1_content, re.DOTALL)
    if not rows1:
        print("Warning: No rows found for Table 1")
        
    for row in rows1: # All rows, check for th vs td
        if '<th>' in row: continue # Skip header if extracted
        cols = re.findall(r'<td>(.*?)</td>', row, re.DOTALL)
        if len(cols) == 2:
            html += f"""
                            <tr class="hover:bg-gray-50 transition-colors">
                                <td class="p-4 font-medium text-secondary bg-gray-50/50">{cols[0].strip()}</td>
                                <td class="p-4 text-sm text-secondary">{cols[1].strip()}</td>
                            </tr>"""

    html += """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Part 2: Visualizations -->
            <div class="mb-16">
                <h3 class="text-2xl font-bold text-primary mb-8 flex items-center">
                    <i class="fas fa-images text-green-500 mr-3"></i>可视化图表分析
                </h3>
                <div class="grid md:grid-cols-2 gap-8">
    """

    # Process Charts
    section2_match = re.search(r'<h2>二、可视化图表展示</h2>(.*?)<div class="section">', content, re.DOTALL)
    if section2_match:
        sec2 = section2_match.group(1)
        charts = re.split(r'<h3>', sec2)[1:]
        for chart in charts:
            try:
                title_part = chart.split('</h3>')[0].strip()
                title = re.sub(r'^\d+\.\s*', '', title_part) # Remove numbering "1. "
                
                img_match = re.search(r'src="(.*?)"', chart)
                img_src = img_match.group(1) if img_match else ""
                
                text_match = re.search(r'<div class="interpretation">\s*(.*?)\s*</div>', chart, re.DOTALL)
                text = text_match.group(1).replace('<strong>解读：</strong>', '').strip() if text_match else ""
                
                html += f"""
                    <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300">
                        <h4 class="font-semibold text-primary mb-4 flex items-center">
                            <span class="w-8 h-8 rounded-full bg-blue-100 text-accent flex items-center justify-center mr-3 text-sm font-bold">
                                <i class="fas fa-chart-bar"></i>
                            </span>
                            {title}
                        </h4>
                        <div class="bg-gray-50 rounded-lg p-4 mb-4 flex items-center justify-center min-h-[250px]">
                            <img src="{img_src}" alt="{title}" class="max-w-full h-auto max-h-[300px] object-contain shadow-sm rounded-md hover:scale-105 transition-transform duration-500">
                        </div>
                        <div class="bg-blue-50/50 p-4 rounded-lg border-l-4 border-accent">
                            <p class="text-sm text-secondary leading-relaxed">
                                <span class="font-bold text-accent mr-1"><i class="fas fa-info-circle"></i> 解读:</span>
                                {text}
                            </p>
                        </div>
                    </div>
    """
            except Exception as e:
                print(f"Error processing chart: {e}")

    html += """
                </div>
            </div>

            <!-- Part 3: Full List -->
            <div class="mb-16">
                <h3 class="text-2xl font-bold text-primary mb-8 flex items-center">
                    <i class="fas fa-list-ol text-purple-500 mr-3"></i>科普教育基地名录（完整版）
                </h3>
                
                <div class="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
                    <div class="flex flex-wrap gap-4 mb-6 sticky top-0 bg-white z-20 pb-4 border-b border-gray-100">
                        <div class="flex-1 min-w-[200px] relative group">
                            <i class="fas fa-search absolute left-3 top-3.5 text-gray-400 group-hover:text-accent transition-colors"></i>
                            <input type="text" id="base-searchInput" 
                                class="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all bg-gray-50 focus:bg-white" 
                                placeholder="搜索基地名称、地区或类型...">
                        </div>
                        <div class="relative">
                            <i class="fas fa-filter absolute left-3 top-3.5 text-gray-400"></i>
                            <select id="base-batchFilter" 
                                class="pl-10 pr-8 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent bg-gray-50 focus:bg-white appearance-none cursor-pointer">
                                <option value="">所有认定批次</option>
                                <option value="2023年申报评审">2023年申报评审</option>
                                <option value="2020年命名到期评估认定">2020年命名到期评估认定</option>
                                <option value="special">AI、机器人、VR 专项</option>
                            </select>
                            <i class="fas fa-chevron-down absolute right-3 top-4 text-gray-400 text-xs pointer-events-none"></i>
                        </div>
                    </div>

                    <div class="overflow-hidden border border-gray-200 rounded-lg shadow-inner">
                        <div class="max-h-[600px] overflow-y-auto custom-scrollbar">
                            <table class="min-w-full divide-y divide-gray-200 relative" id="base-baseTable">
                                <thead class="bg-gray-100 sticky top-0 z-10 shadow-sm">
                                    <tr>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider w-16">序号</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">基地名称</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider w-32">所属地区</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider w-40">认定批次</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider w-32">基地类型</th>
                                        <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">备注</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
    """

    # Process Table 3 Rows
    table_rows = re.findall(r'<tr(.*?)>(.*?)</tr>', tbody_content, re.DOTALL)
    if not table_rows:
         print("Warning: No rows found for Table 3")
         
    for attrs, content_row in table_rows:
        is_special = 'data-is-special="true"' in attrs
        special_class = "bg-yellow-50" if is_special else ""
        
        html += f'<tr {attrs} class="hover:bg-blue-50 transition-colors border-b last:border-b-0 {special_class}">'
        cols = re.findall(r'<td>(.*?)</td>', content_row, re.DOTALL)
        if len(cols) >= 6:
            html += f'<td class="px-6 py-4 text-sm font-medium text-gray-500">{cols[0].strip()}</td>'
            html += f'<td class="px-6 py-4 text-sm font-bold text-primary">{cols[1].strip()}</td>'
            
            # Badge for region
            region = cols[2].strip()
            html += f'<td class="px-6 py-4 text-sm text-secondary"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">{region}</span></td>'
            
            # Batch text small
            batch = cols[3].strip()
            batch_short = batch.replace("年申报评审", "申报").replace("年命名到期评估认定", "续评")
            html += f'<td class="px-6 py-4 text-sm text-muted" title="{batch}">{batch_short}</td>'
            
            # Type badge
            type_text = cols[4].strip()
            color_class = "bg-blue-100 text-blue-800"
            if "科技" in type_text: color_class = "bg-indigo-100 text-indigo-800"
            elif "农业" in type_text: color_class = "bg-green-100 text-green-800"
            elif "医学" in type_text: color_class = "bg-red-100 text-red-800"
            elif "青少年" in type_text: color_class = "bg-yellow-100 text-yellow-800"
            
            html += f'<td class="px-6 py-4 text-sm text-secondary"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {color_class}">{type_text}</span></td>'
            
            html += f'<td class="px-6 py-4 text-sm text-secondary italic">{cols[5].strip()}</td>'
        html += '</tr>'

    html += """
                        </tbody>
                    </table>
                    <div id="base-noResult" class="hidden flex flex-col items-center justify-center p-12 text-center text-gray-500">
                        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                            <i class="fas fa-search text-2xl text-gray-400"></i>
                        </div>
                        <h5 class="text-lg font-medium text-gray-900 mb-1">未找到匹配的基地</h5>
                        <p class="text-sm">请尝试调整关键词或筛选条件</p>
                    </div>
                </div>
                <div class="mt-4 text-right text-xs text-muted">
                    <span class="inline-block px-2 py-1 bg-yellow-50 text-yellow-700 rounded mr-2">注</span>带黄色背景的为AI/机器人/VR专项相关基地
                </div>
            </div>
        </div>
    </section>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")

except Exception as e:
    print(f"Error: {e}")
