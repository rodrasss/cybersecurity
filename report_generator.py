import sys, json, html

def load_json(path):
    try:
        with open(path,'r',encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

semgrep = load_json(sys.argv[1]) if len(sys.argv)>1 else None
snyk = load_json(sys.argv[2]) if len(sys.argv)>2 else None
dast_html_path = sys.argv[3] if len(sys.argv)>3 else None
out = sys.argv[4] if len(sys.argv)>4 else 'report.html'

parts = []
parts.append('<html><head><meta charset="utf-8"><title>Security Report</title></head><body>')
parts.append('<h1>Security Report (generated)</h1>')

parts.append('<h2>Semgrep (SAST)</h2>')
if semgrep and 'errors' not in semgrep:
    findings = semgrep.get('results', []) if isinstance(semgrep, dict) else []
    if findings:
        parts.append('<ul>')
        for r in findings:
            msg = html.escape(r.get('check_id','')) + ' - ' + html.escape(r.get('extra',{}).get('message',''))
            parts.append(f'<li>{msg}</li>')
        parts.append('</ul>')
    else:
        parts.append('<p>No findings (semgrep)</p>')
else:
    parts.append('<p>Semgrep output not available or could not be parsed.</p>')

parts.append('<h2>Snyk (SCA)</h2>')
if snyk:
    # Try to present top-level info
    parts.append('<pre>'+html.escape(json.dumps(snyk, indent=2, ensure_ascii=False))+'</pre>')
else:
    parts.append('<p>Snyk output not available.</p>')

parts.append('<h2>DAST (simple curl fallback)</h2>')
if dast_html_path:
    try:
        with open(dast_html_path,'r',encoding='utf-8') as f:
            body = f.read()
        # crude check for our script payload
        if '<script>alert(1)</script>' in body:
            parts.append('<p><b>Reflected XSS payload found in response (payload appears unescaped).</b></p>')
        parts.append('<h3>DAST Response (snippet)</h3>')
        parts.append('<pre>'+html.escape(body[:1000])+'</pre>')
    except Exception as e:
        parts.append(f'<p>Could not read DAST response: {e}</p>')
else:
    parts.append('<p>No DAST response saved.</p>')

parts.append('</body></html>')
with open(out,'w',encoding='utf-8') as f:
    f.write('\n'.join(parts))
print(f'Generated report: {out}')
