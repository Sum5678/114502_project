import ast

# 指定 views.py 的完整路徑
views_path = r"C:\Users\wusun\myproject\myapp\views.py"

# 讀取並解析
with open(views_path, 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

# 統計函式與類別
func_count = 0
class_count = 0

for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        func_count += 1
    elif isinstance(node, ast.ClassDef):
        class_count += 1

print(f"函式型 View: {func_count}")
print(f"類別型 View: {class_count}")
