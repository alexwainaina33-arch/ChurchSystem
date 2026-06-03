import os
txt = open('/app/frontend/pages/dashboard.tsx').read()
txt = txt.replace("'../../components/Sidebar'", "'../components/Sidebar'")
open('/app/frontend/pages/dashboard.tsx', 'w').write(txt)
print('fixed')
