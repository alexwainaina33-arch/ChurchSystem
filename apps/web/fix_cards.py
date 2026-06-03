txt = open('/app/frontend/pages/dashboard.tsx').read()

# Fix stat card definitions to use solid Tailwind v4 compatible colors
old = """const statCard = [
  {
    key: 'members',   label: 'Total Members',  href: '/members',
    icon: Users,       bg: 'bg-sky-500/10',    border: 'border-sky-500/20',
    icon_bg: 'bg-sky-500/15', icon_color: 'text-sky-400', val_color: 'text-sky-300',
  },
  {
    key: 'giving',    label: 'Total Giving',   href: '/giving',
    icon: DollarSign,  bg: 'bg-emerald-500/10', border: 'border-emerald-500/20',
    icon_bg: 'bg-emerald-500/15', icon_color: 'text-emerald-400', val_color: 'text-emerald-300',
  },
  {
    key: 'projects',  label: 'Active Projects', href: '/projects',
    icon: FolderOpen,  bg: 'bg-amber-500/10',   border: 'border-amber-500/20',
    icon_bg: 'bg-amber-500/15', icon_color: 'text-amber-400', val_color: 'text-amber-300',
  },
  {
    key: 'attendance', label: 'Last Attendance', href: '/attendance',
    icon: CalendarCheck, bg: 'bg-violet-500/10', border: 'border-violet-500/20',
    icon_bg: 'bg-violet-500/15', icon_color: 'text-violet-400', val_color: 'text-violet-300',
  },
]"""

new = """const statCard = [
  {
    key: 'members',   label: 'Total Members',  href: '/members',
    icon: Users,       bg: 'bg-sky-50',    border: 'border-sky-200',
    icon_bg: 'bg-sky-100', icon_color: 'text-sky-600', val_color: 'text-sky-700',
  },
  {
    key: 'giving',    label: 'Total Giving',   href: '/giving',
    icon: DollarSign,  bg: 'bg-emerald-50', border: 'border-emerald-200',
    icon_bg: 'bg-emerald-100', icon_color: 'text-emerald-600', val_color: 'text-emerald-700',
  },
  {
    key: 'projects',  label: 'Active Projects', href: '/projects',
    icon: FolderOpen,  bg: 'bg-amber-50',   border: 'border-amber-200',
    icon_bg: 'bg-amber-100', icon_color: 'text-amber-600', val_color: 'text-amber-700',
  },
  {
    key: 'attendance', label: 'Last Attendance', href: '/attendance',
    icon: CalendarCheck, bg: 'bg-violet-50', border: 'border-violet-200',
    icon_bg: 'bg-violet-100', icon_color: 'text-violet-600', val_color: 'text-violet-700',
  },
]"""

txt = txt.replace(old, new)
open('/app/frontend/pages/dashboard.tsx', 'w').write(txt)
print('done')
