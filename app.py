import re
from flask import Flask, request
app = Flask(__name__)

CODES_DB = {
 "OB-PASTE-NG-001": {"code":"OB-PASTE-NG-001","batch":"NG-2026-001","size":"100g"},
 "OB-PASTE-LAG-150": {"code":"OB-PASTE-LAG-150","batch":"LAGOS-003","size":"150g"},
}

def verify_code(code):
    clean = re.sub(r'\s+', '', code).upper()
    m = re.search(r'OB-[A-Z0-9-]{4,}', clean)
    if m: clean = m.group(0)
    return CODES_DB.get(clean)

@app.route('/verify-vision', methods=['GET','POST'])
def verify_vision():
    result = ""
    if request.method == 'POST':
        code = request.form.get('code','')
        cd = verify_code(code) if code else None
        photo_name = ""
        if 'photo' in request.files and request.files['photo'].filename!='':
            photo_name = request.files['photo'].filename
            result += f'<div style="background:#cce5ff;padding:10px;border-radius:8px;margin-top:10px">📸 Photo received: {photo_name}<br><b>Mock AI:</b> No foil detected - Looks ORIGINAL (Real Oral-B has NO foil)</div>'
        if cd:
            result = f'<div style="background:#d4edda;padding:15px;border-radius:8px"><h3>✅ CODE VALID - {cd["code"]}</h3>Batch: {cd["batch"]}<br>ORIGINAL Oral-B - Safe!</div>' + result
        elif code:
            result = f'<div style="background:#f8d7da;padding:15px;border-radius:8px"><h3>❌ CODE INVALID - {code}</h3>Possible FAKE!</div>' + result
        if not code and not photo_name:
            result = '<div style="background:#fff3cd;padding:10px">Enter a code or upload a photo</div>'
    return f'''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{{font-family:Arial;max-width:500px;margin:20px auto;padding:15px;background:#f0f8ff}}
.card{{background:white;padding:20px;border-radius:12px;box-shadow:0 2px 8px #0002;margin-bottom:12px}}
input,select{{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:8px}}
button{{background:#0a4da1;color:white;padding:14px;width:100%;border:none;border-radius:8px;font-weight:bold}}
</style></head><body>
<h2 style="color:#0a4da1">Oral-B Guard 🪥</h2>
<div class="card">
<form method="POST" enctype="multipart/form-data">
<input name="code" placeholder="OB-PASTE-NG-001">
<select name="check_type"><option>Tube Top - Foil Check</option><option>Paste Texture</option></select>
<input type="file" name="photo" accept="image/*">
<button>🔍 VERIFY</button>
</form>
{result}
</div>
<div class="card" style="background:#fff3cd">
❌ Has foil seal = FAKE (Real has NO foil)<br>
❌ Opaque chalky white = FAKE<br>
✅ Real = Translucent greenish jelly, long slim tube
</div>
<p><small>Test code: OB-PASTE-NG-001</small></p>
</body></html>
'''
@app.route('/')
def home():
    return '<a href="/verify-vision">Go to verify-vision</a>'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
