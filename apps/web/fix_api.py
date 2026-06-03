txt = open('/app/frontend/pages/dashboard.tsx').read()
txt = txt.replace("'../../lib/api'", "'../lib/api'")
open('/app/frontend/pages/dashboard.tsx', 'w').write(txt)
print('fixed')
