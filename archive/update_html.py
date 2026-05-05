import joblib
import re

print("Loading encoders...")
branches = list(joblib.load('branch_encoder.joblib').classes_)
categories = list(joblib.load('category_encoder.joblib').classes_)

branch_options = '<option value="" disabled selected>Select Branch</option>\n'
for b in branches:
    branch_options += f'                    <option value="{b}">{b}</option>\n'

branch_html = f'''            <div>
                <label class="label-text">Preferred Branch</label>
                <select id="branch" required class="input-field">
{branch_options}                </select>
            </div>'''

cat_options = '<option value="" disabled selected>Select Category</option>\n'
for c in categories:
    cat_options += f'                        <option value="{c}">{c}</option>\n'

cat_html = f'''                <div>
                    <label class="label-text">Category</label>
                    <select id="category" required class="input-field">
{cat_options}                    </select>
                </div>'''

print("Reading index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Updating index.html with dropdowns...")
# Replace branch input
content = re.sub(
    r'<div>\s*<label class="label-text">Preferred Branch</label>\s*<input type="text" id="branch"[^>]*>\s*</div>',
    branch_html,
    content
)

# Replace category input
content = re.sub(
    r'<div>\s*<label class="label-text">Category</label>\s*<input type="text" id="category"[^>]*>\s*</div>',
    cat_html,
    content
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully!")
