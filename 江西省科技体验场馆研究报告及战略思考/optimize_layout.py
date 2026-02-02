import re

target_file = r"c:\Users\lucky\Desktop\科技体验场所调研报告\汇报材料\江西省科技体验场馆研究报告及战略思考\江西省科技体验场馆研究报告及战略思考.html"

# We will replace the entire "mt-6" block with the new layout.
# Block starts at <div class="mt-6"> (Line 4161)
# Ends around 4212.

new_layout = '''                            <div class="mt-6">
                                <h4 class="text-lg font-semibold text-primary mb-4">金字塔三层架构</h4>
                                <div class="grid md:grid-cols-3 gap-4 mb-8">
                                    <div class="bg-blue-50 p-4 rounded-xl border-t-4 border-blue-500 shadow-sm hover:shadow-md transition-shadow">
                                        <div class="flex items-center justify-between mb-3">
                                            <div class="w-10 h-10 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center font-bold text-lg">基</div>
                                            <span class="text-2xl font-bold text-blue-600">40%</span>
                                        </div>
                                        <h5 class="font-bold text-primary mb-2">基础认知层</h5>
                                        <p class="text-secondary text-xs leading-relaxed">AI发展历史、基本概念、原理演示，构建科学认知基石</p>
                                    </div>

                                    <div class="bg-indigo-50 p-4 rounded-xl border-t-4 border-indigo-500 shadow-sm hover:shadow-md transition-shadow">
                                        <div class="flex items-center justify-between mb-3">
                                            <div class="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center font-bold text-lg">中</div>
                                            <span class="text-2xl font-bold text-indigo-600">35%</span>
                                        </div>
                                        <h5 class="font-bold text-primary mb-2">应用体验层</h5>
                                        <p class="text-secondary text-xs leading-relaxed">智能制造、医疗、农业、文化等应用场景深度体验</p>
                                    </div>

                                    <div class="bg-purple-50 p-4 rounded-xl border-t-4 border-purple-500 shadow-sm hover:shadow-md transition-shadow">
                                        <div class="flex items-center justify-between mb-3">
                                            <div class="w-10 h-10 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center font-bold text-lg">顶</div>
                                            <span class="text-2xl font-bold text-purple-600">25%</span>
                                        </div>
                                        <h5 class="font-bold text-primary mb-2">创造实践层</h5>
                                        <p class="text-secondary text-xs leading-relaxed">机器人组装、AI 模型训练、创新项目开发与实践</p>
                                    </div>
                                </div>

                                <h4 class="text-lg font-semibold text-primary mb-4">江西特色融入建议</h4>
                                <div class="grid md:grid-cols-3 gap-4">
                                    <div class="flex items-start p-4 bg-red-50 rounded-xl border border-red-100 hover:bg-red-100/50 transition-colors">
                                        <div class="w-10 h-10 rounded-full bg-red-100 flex-shrink-0 flex items-center justify-center mr-3">
                                            <i class="fas fa-flag text-red-500"></i>
                                        </div>
                                        <div>
                                            <h5 class="font-bold text-gray-800 text-sm mb-1">红色AI</h5>
                                            <p class="text-xs text-gray-600">革命文献智能分析<br>苏区经济模型重建</p>
                                        </div>
                                    </div>

                                    <div class="flex items-start p-4 bg-green-50 rounded-xl border border-green-100 hover:bg-green-100/50 transition-colors">
                                        <div class="w-10 h-10 rounded-full bg-green-100 flex-shrink-0 flex items-center justify-center mr-3">
                                            <i class="fas fa-leaf text-green-500"></i>
                                        </div>
                                        <div>
                                            <h5 class="font-bold text-gray-800 text-sm mb-1">绿色AI</h5>
                                            <p class="text-xs text-gray-600">鄱阳湖生态监测<br>稀土智能勘探</p>
                                        </div>
                                    </div>

                                    <div class="flex items-start p-4 bg-blue-50 rounded-xl border border-blue-100 hover:bg-blue-100/50 transition-colors">
                                        <div class="w-10 h-10 rounded-full bg-blue-100 flex-shrink-0 flex items-center justify-center mr-3">
                                            <i class="fas fa-palette text-blue-500"></i>
                                        </div>
                                        <div>
                                            <h5 class="font-bold text-gray-800 text-sm mb-1">古色AI</h5>
                                            <p class="text-xs text-gray-600">书院智能教育体系<br>方言识别与保护</p>
                                        </div>
                                    </div>
                                </div>
                            </div>'''

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the block
# Identify the block by <div class="mt-6"> ...content... </div>
# Since I just wrote it, I know the content structure roughly.
# But regex matching large blocks is safer with start/end markers.
# Start: <div class="mt-6">
# End: </div> <!-- end of mt-6 div -->
# Followed by: </div> <!-- end of bg-white div -->
# Followed by: </div> <!-- end of space-y-8 div -->
# Followed by: <div class="bg-white rounded-2xl shadow-lg p-8">

# Pattern:
# (<div class="mt-6">)([\s\S]*?)(</div>\s*</div>\s*</div>\s*<div class="bg-white)

pattern = re.compile(
    r'(<div class="mt-6">)([\s\S]*?)(</div>\s*</div>\s*</div>\s*<div class="bg-white)',
    re.MULTILINE
)

# Wait, `</div>\s*</div>\s*</div>` matches the closing of mt-6, bg-white, space-y-8.
# But the NEXT block starts with `<div class="bg-white`.
# So the lookahead part is correct.

# I will check if I can match unique content inside just to be sure.
# Inside is "金字塔三层架构" and "江西特色融入建议".

if "金字塔三层架构" not in content:
    print("Could not find the content to replace.")
    exit(1)

# Using a simpler replace on the known unique chunk might be safer than complex regex if the boundaries are ambiguous.
# I will try to match the EXACT previous content if I can reproduce it.
# Previous content:
# <div class="mt-6"> ... <h5 class="font-semibold text-primary text-sm mb-3">金字塔三层架构</h5> ... </div> (end of mt-6 is hard to guess indent)

# Let's use Regex.
new_content = re.sub(
    r'(<div class="mt-6">)([\s\S]*?)(</div>\s*</div>\s*</div>\s*<div class="bg-white)',
    f'{new_layout}\\3', # Keep the closing tags and next block
    content,
    count=1
)

if len(new_content) != len(content):
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Layout updated.")
else:
    print("Replacement failed (Regex match issue).")
