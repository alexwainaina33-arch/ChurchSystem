import os
txt = open('/app/app/routers/../../../apps/web/components/Sidebar.tsx', 'r').read() if False else ""

txt = """'use client'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import {
  Church, Users, CalendarCheck, DollarSign,
  FolderOpen, MessageSquare, LayoutDashboard,
  TrendingUp, Settings, Menu, X, ChevronRight, LogOut, UserCircle
} from 'lucide-react'

const nav = [
  { href: '/',           label: 'Dashboard',  icon: LayoutDashboard, color: 'text-violet-400' },
  { href: '/members',    label: 'Members',    icon: Users,           color: 'text-sky-400'    },
  { href: '/attendance', label: 'Attendance', icon: CalendarCheck,   color: 'text-emerald-400' },
  { href: '/giving',     label: 'Giving',     icon: DollarSign,      color: 'text-amber-400'  },
  { href: '/projects',   label: 'Projects',   icon: FolderOpen,      color: 'text-orange-400' },
  { href: '/messages',   label: 'Messages',   icon: MessageSquare,   color: 'text-pink-400'   },
  { href: '/finance',    label: 'Finance',    icon: TrendingUp,      color: 'text-teal-400'   },
  { href: '/settings',   label: 'Settings',   icon: Settings,        color: 'text-slate-400'  },
]

const bottomNav = nav.slice(0, 5)

export default function Sidebar() {
  const path = usePathname()
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const [userName, setUserName] = useState('')
  const [userRole, setUserRole] = useState('')

  useEffect(() => {
    setUserName(localStorage.getItem('user_name') || 'User')
    setUserRole(localStorage.getItem('user_role') || '')
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false) }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [])

  useEffect(() => { setOpen(false) }, [path])

  function logout() {
    localStorage.clear()
    document.cookie = 'token=; path=/; max-age=0'
    router.push('/login')
  }

  const isActive = (href: string) =>
    href === '/' ? path === '/' : path === href || path.startsWith(href + '/')

  const roleLabel: Record<string,string> = { hq_admin: 'HQ Admin', pastor: 'Pastor', branch_admin: 'Branch Admin', treasurer: 'Treasurer' }

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        aria-label="Open navigation"
        className="md:hidden fixed top-3.5 left-4 z-50 w-10 h-10 flex items-center justify-center
                   rounded-xl bg-indigo-900 border border-indigo-700 shadow-lg shadow-indigo-900
                   active:scale-95 transition-transform"
      >
        <Menu className="w-5 h-5 text-indigo-200" />
      </button>

      <div
        onClick={() => setOpen(false)}
        className={`fixed inset-0 z-40 bg-black/70 backdrop-blur-sm transition-opacity duration-300 md:hidden
                    ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
      />

      <aside className={`
        fixed top-0 left-0 z-50 h-full w-72 flex flex-col
        bg-indigo-900 border-r border-indigo-700
        shadow-2xl shadow-indigo-950
        transition-transform duration-300 ease-in-out
        md:static md:w-64 md:translate-x-0 md:z-auto md:shadow-none md:min-h-screen
        ${open ? 'translate-x-0' : '-translate-x-full'}
      `}>

        <div className="flex items-center justify-between px-5 py-5 border-b border-indigo-700">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-yellow-400 to-amber-500
                            flex items-center justify-center shadow-lg shadow-amber-900/40">
              <Church className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white font-bold text-sm leading-tight tracking-tight">ChurchHub</p>
              <p className="text-indigo-400 text-xs">Manage your church, your way.</p>
            </div>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="md:hidden w-8 h-8 flex items-center justify-center rounded-lg
                       text-indigo-400 hover:text-white hover:bg-indigo-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
          {nav.map(({ href, label, icon: Icon, color }) => {
            const active = isActive(href)
            return (
              <Link
                key={href}
                href={href}
                className={`
                  group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                  transition-all duration-150
                  ${active
                    ? 'bg-indigo-700 text-white shadow-sm shadow-indigo-900'
                    : 'text-indigo-300 hover:bg-indigo-800 hover:text-white'
                  }
                `}
              >
                <span className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0
                  transition-colors
                  ${active ? 'bg-indigo-700' : 'bg-indigo-800 group-hover:bg-indigo-800'}`}>
                  <Icon className={`w-3.5 h-3.5 ${active ? color : 'text-indigo-400 group-hover:' + color.replace('text-','')}`} />
                </span>
                <span className="flex-1">{label}</span>
                {active && <ChevronRight className="w-3.5 h-3.5 text-indigo-400" />}
              </Link>
            )
          })}
        </nav>

        <div className="px-3 py-4 border-t border-indigo-700 space-y-1">
          <Link href="/profile"
            className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                       text-indigo-300 hover:bg-indigo-800 hover:text-white transition-all">
            <span className="w-7 h-7 rounded-lg bg-indigo-800 flex items-center justify-center shrink-0">
              <UserCircle className="w-3.5 h-3.5 text-indigo-400" />
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-indigo-200 truncate">{userName}</p>
              <p className="text-xs text-indigo-500">{roleLabel[userRole] || userRole}</p>
            </div>
          </Link>
          <button onClick={logout}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                       text-indigo-300 hover:bg-red-900/40 hover:text-red-300 transition-all">
            <span className="w-7 h-7 rounded-lg bg-indigo-800 flex items-center justify-center shrink-0">
              <LogOut className="w-3.5 h-3.5 text-indigo-400" />
            </span>
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      <nav className="md:hidden fixed bottom-0 inset-x-0 z-40
                      bg-indigo-900/95 backdrop-blur-xl
                      border-t border-indigo-700
                      pb-safe">
        <div className="flex items-stretch">
          {bottomNav.map(({ href, label, icon: Icon, color }) => {
            const active = isActive(href)
            return (
              <Link
                key={href}
                href={href}
                className={`
                  flex-1 flex flex-col items-center justify-center py-2.5 gap-1
                  transition-all duration-150 active:scale-90
                  ${active ? 'text-white' : 'text-indigo-500 hover:text-indigo-300'}
                `}
              >
                <span className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all
                  ${active ? 'bg-indigo-700 shadow-sm shadow-indigo-900' : ''}`}>
                  <Icon className={`w-4 h-4 ${active ? color : ''}`} />
                </span>
                <span className="text-[10px] font-semibold tracking-wide leading-none">{label}</span>
              </Link>
            )
          })}
        </div>
      </nav>
    </>
  )
}
"""
open('/app/frontend/Sidebar.tsx', 'w').write(txt)
print('done')
