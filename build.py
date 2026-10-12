import json, html
from pathlib import Path
r=Path(__file__).parent
s=json.loads((r/'openapi.json').read_text())
def esc(x): return html.escape(str(x))
def block(value):
    text=json.dumps(value,indent=2) if isinstance(value,dict) else value
    return '<div class="code"><button type="button" class="copy">Copy</button><pre><code>'+esc(text)+'</code></pre></div>'
def schema(ref):
    result=s
    for part in ref.removeprefix('#/').split('/'): result=result[part]
    return result
parts=[]
for kind,label,description,reply in [
 ('events','Create Event','Creates a Counterpoint meeting and queues an Outlook appointment. In the sandbox, Outlook writes go to Jeff’s separate Counterpoint API Tests calendar, with no attendees.',{'counterpoint_meeting_id':12345,'salesforce_record_id':'00U000000000000001','calendar_status':'pending','reused':False}),
 ('tasks','Create Task','Creates a completed Counterpoint Sales Activity. No Outlook appointment is created. Pending follow-up reminders are not supported.',{'counterpoint_activity_id':'d40a8f6a-319c-4233-8899-c0cc94269916','salesforce_record_id':'00T000000000000001','activity_status':'Completed','calendar_status':'not_applicable','reused':False})]:
    op=s['paths']['/v1/'+kind]['post'];content=op['requestBody']['content']['application/json'];body=schema(content['schema']['$ref'])
    rows=[]
    for field,prop in body['properties'].items():
        constraints=[]
        if prop.get('description'): constraints.append(prop['description'])
        if prop.get('enum'): constraints.append('Values: '+', '.join(prop['enum']))
        if 'const' in prop: constraints.append('Required value: '+str(prop['const']))
        if prop.get('format'): constraints.append('Format: '+prop['format'])
        if prop.get('pattern'): constraints.append('Pattern: '+prop['pattern'])
        for key in ['minLength','maxLength']: 
            if key in prop: constraints.append(key+': '+str(prop[key]))
        rows.append('<tr><td><code>'+esc(field)+'</code></td><td>'+('Required' if field in body['required'] else 'Optional')+'</td><td>'+esc(prop.get('type',''))+'</td><td>'+esc('; '.join(constraints))+'</td></tr>')
    parts.append('<section id="'+kind+'"><h2>'+label+'</h2><p class="endpoint"><b>POST</b> /v1/'+kind+'</p><p>'+description+'</p><h3>Request JSON</h3>'+block(content['example'])+'<h3>Request fields</h3><div class="table-wrap"><table><thead><tr><th>Field</th><th>Required</th><th>Type</th><th>Rules</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div><h3>201 response <span class="muted">— illustrative IDs</span></h3>'+block(reply)+'<p><a href="reference.html#tag/'+('Events' if kind=='events' else 'Tasks')+'">Full '+kind+' schema and responses →</a></p></section>')
page=(r/'quickstart.template.html').read_text().replace('<!-- ENDPOINTS -->',''.join(parts)).replace('<!-- BASE -->',esc(s['servers'][0]['url']))
(r/'index.html').write_text(page)
