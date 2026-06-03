import os

# Fix attendance table overflow
f = '/app/frontend/pages/attendance.tsx'
txt = open(f).read()
txt = txt.replace('<table className="w-full">', '<div className="overflow-x-auto"><table className="w-full min-w-[700px]">')
txt = txt.replace('</table>\n          )}\n        </div>', '</table></div>\n          )}\n        </div>')
txt = txt.replace('<main className="flex-1 p-8">', '<main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">')
open(f, 'w').write(txt)
print('attendance done')

# Fix messages table overflow
f2 = '/app/frontend/pages/messages.tsx'
txt2 = open(f2).read()
txt2 = txt2.replace('<table className="w-full">', '<div className="overflow-x-auto"><table className="w-full min-w-[500px]">')
txt2 = txt2.replace('</table>\n          )}\n        </div>', '</table></div>\n          )}\n        </div>')
txt2 = txt2.replace('<main className="flex-1 p-8">', '<main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">')
open(f2, 'w').write(txt2)
print('messages done')

# Fix finance table overflow
f3 = '/app/frontend/pages/finance.tsx'
txt3 = open(f3).read()
txt3 = txt3.replace('<table className="w-full">', '<div className="overflow-x-auto"><table className="w-full min-w-[500px]">')
txt3 = txt3.replace('<main className="flex-1 p-8">', '<main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">')
open(f3, 'w').write(txt3)
print('finance done')

