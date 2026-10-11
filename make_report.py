# Prompt3：生成交互式HTML报告，下拉切换、点击表头排序
import pandas as pd
import os

html_template = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Collocation Report 君子</title>
<style>
table {{border-collapse:collapse;width:100%;}}
th,td {{border:1px solid #ccc;padding:6px;}}
th {{cursor:pointer;background:#f0f0f0;}}
</style>
</head>
<body>
<h1>搭配词分析：君子（论语 / 周易）</h1>
<select id="fileSelect">
{{options}}
</select>
<div id="tableContainer"></div>
<script>
const data = {{json_data}};
const select = document.getElementById("fileSelect");
const container = document.getElementById("tableContainer");

function renderTable(name){{
    const df = data[name];
    let html = "<table><tr>";
    const cols = Object.keys(df[0]);
    cols.forEach(c=>html += `<th onclick="sortTable('${c}')">${c}</th>`);
    html += "</tr>";
    df.forEach(row=>{{
        html += "<tr>";
        cols.forEach(c=> html += `<td>${row[c]}</td>`);
        html += "</tr>";
    }})
    html += "</table>";
    container.innerHTML = html;
}}
let sortCol = null, sortAsc = true;
function sortTable(col){{
    const df = data[select.value];
    if (sortCol === col) {{ sortAsc = !sortAsc; }} else {{ sortCol = col; sortAsc = true; }}
    df.sort((a,b)=>{{
        const x = a[col], y = b[col];
        if (typeof x === "number" && typeof y === "number") return sortAsc ? x - y : y - x;
        return sortAsc ? String(x).localeCompare(String(y)) : String(y).localeCompare(String(x));
    }});
    renderTable(select.value);
}}
select.onchange = ()=> renderTable(select.value);
renderTable(select.options[0].value);
</script>
</body>
</html>
'''
# 读取output全部csv
csv_files = [f for f in os.listdir("output") if f.endswith(".csv")]
options_html = "\n".join([f'<option value="{f}">{f}</option>' for f in csv_files])
all_data = {}
for fn in csv_files:
    df = pd.read_csv(os.path.join("output",fn))
    all_data[fn] = df.to_dict("records")

import json
json_str = json.dumps(all_data, ensure_ascii=False)
# 模板不是 f-string，{{ }} 不会被还原，需手动替换为单大括号
final_html = html_template.replace("{{options}}",options_html).replace("{{json_data}}",json_str).replace("{{","{").replace("}}","}")
with open("output/results.html","w",encoding="utf-8") as fw:
    fw.write(final_html)
print("HTML报告已生成 output/results.html")