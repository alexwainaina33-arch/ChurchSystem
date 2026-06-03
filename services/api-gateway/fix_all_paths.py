import os
files = [
    '/app/frontend/pages/members.tsx',
    '/app/frontend/pages/attendance.tsx',
    '/app/frontend/pages/finance.tsx',
    '/app/frontend/pages/projects.tsx',
]
for f in files:
    if os.path.exists(f):
        txt = open(f).read()
        txt = txt.replace("'../../lib/api'", "'../lib/api'")
        txt = txt.replace("'../../components/Sidebar'", "'../components/Sidebar'")
        open(f, 'w').write(txt)
        print('fixed: ' + f)
