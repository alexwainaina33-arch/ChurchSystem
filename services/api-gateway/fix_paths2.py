import os

# app/page.tsx is at apps/web/app/ → needs ../components/Sidebar and ../lib/api
dash = '/app/frontend/pages/dashboard.tsx'
if os.path.exists(dash):
    txt = open(dash).read()
    txt = txt.replace("'../../components/Sidebar'", "'../components/Sidebar'")
    txt = txt.replace("'../../lib/api'", "'../lib/api'")
    txt = txt.replace("'../components/Sidebar'", "'../components/Sidebar'")
    txt = txt.replace("'../lib/api'", "'../lib/api'")
    open(dash, 'w').write(txt)
    print('dashboard ok')

# app/members/page.tsx etc are at apps/web/app/members/ → needs ../../components/Sidebar
subpages = [
    '/app/frontend/pages/members.tsx',
    '/app/frontend/pages/attendance.tsx',
    '/app/frontend/pages/finance.tsx',
    '/app/frontend/pages/projects.tsx',
]
for f in subpages:
    if os.path.exists(f):
        txt = open(f).read()
        txt = txt.replace("'../components/Sidebar'", "'../../components/Sidebar'")
        txt = txt.replace("'../lib/api'", "'../../lib/api'")
        open(f, 'w').write(txt)
        print('fixed: ' + f)
