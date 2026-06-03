import os
os.makedirs('/app/frontend/pages', exist_ok=True)
txt = '''\'use client\'
import { useEffect, useState } from \'react\'
import Sidebar from \'../../components/Sidebar\'
import api from \'../../lib/api\'
import { Users, DollarSign, FolderOpen, CalendarCheck, ArrowUpRight, TrendingUp } from \'lucide-react\'
import Link from \'next/link\'

const CHURCH_ID = \'00000000-0000-0000-0000-000000000001\'

const statCard = [
  {
    key: \'members\',   label: \'Total Members\',  href: \'/members\',
    icon: Users,       bg: \'bg-sky-500/10\',    border: \'border-sky-500/20\',
    icon_bg: \'bg-sky-500/15\', icon_color: \'text-sky-400\', val_color: \'text-sky-300\',
  },
  {
    key: \'giving\',    label: \'Total Giving\',   href: \'/giving\',
    icon: DollarSign,  bg: \'bg-emerald-500/10\', border: \'border-emerald-500/20\',
    icon_bg: \'bg-emerald-500/15\', icon_color: \'text-emerald-400\', val_color: \'text-emerald-300\',
  },
  {
    key: \'projects\',  label: \'Active Projects\', href: \'/projects\',
    icon: FolderOpen,  bg: \'bg-amber-500/10\',   border: \'border-amber-500/20\',
    icon_bg: \'bg-amber-500/15\', icon_color: \'text-amber-400\', val_color: \'text-amber-300\',
  },
  {
    key: \'attendance\', label: \'Last Attendance\', href: \'/attendance\',
    icon: CalendarCheck, bg: \'bg-violet-500/10\', border: \'border-violet-500/20\',
    icon_bg: \'bg-violet-500/15\', icon_color: \'text-violet-400\', val_color: \'text-violet-300\',
  },
]

export default function DashboardPage() {
  const [data, setData]       = useState<any>(null)
  const [giving, setGiving]   = useState<any[]>([])
  const [sessions, setSessions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get(\'/dashboard/hq/?church_id=\' + CHURCH_ID),
      api.get(\'/giving/summary/?church_id=\' + CHURCH_ID),
      api.get(\'/attendance/sessions/?church_id=\' + CHURCH_ID),
    ]).then(([d, g, s]) => {
      setData(d.data); setGiving(g.data); setSessions(s.data)
    }).finally(() => setLoading(false))
  }, [])

  const totalGiving  = giving.reduce((s, g) => s + g.total_kes, 0)
  const lastSession  = sessions[0]

  const statValues: Record<string, string> = {
    members:    String(data?.total_members   ?? 0),
    giving:     \'KES \' + totalGiving.toLocaleString(),
    projects:   String(data?.active_projects ?? 0),
    attendance: lastSession ? String(lastSession.total_count) : \'0\',
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />

      <main className="flex-1 min-w-0 pb-24 md:pb-0">

        {/* Top bar */}
        <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200
                           px-4 md:px-8 py-3.5 flex items-center gap-3 shadow-sm">
          <div className="ml-12 md:ml-0">
            <h1 className="text-gray-900 font-bold text-lg leading-tight">HQ Dashboard</h1>
            <p className="text-gray-400 text-xs">Grace Community Church</p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <span className="hidden sm:inline-flex items-center gap-1.5 text-xs font-medium
                             text-emerald-700 bg-emerald-50 border border-emerald-200
                             px-2.5 py-1 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Live
            </span>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-6">

          {loading ? (
            <div className="flex flex-col items-center justify-center py-32 gap-3">
              <div className="w-10 h-10 border-[3px] border-indigo-200 border-t-indigo-600
                              rounded-full animate-spin" />
              <p className="text-gray-400 text-sm">Loading dashboard...</p>
            </div>
          ) : (<>

            {/* ── Stat Cards — 2 cols mobile, 4 desktop ── */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
              {statCard.map(({ key, label, href, icon: Icon, bg, border, icon_bg, icon_color, val_color }) => (
                <Link
                  key={key}
                  href={href}
                  className={`group relative rounded-2xl border ${border} ${bg}
                              p-4 md:p-5 hover:shadow-md transition-all duration-200
                              hover:-translate-y-0.5 active:scale-[0.98]`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className={`w-9 h-9 rounded-xl ${icon_bg} flex items-center justify-center`}>
                      <Icon className={`w-4 h-4 ${icon_color}`} />
                    </div>
                    <ArrowUpRight className="w-3.5 h-3.5 text-gray-300 group-hover:text-gray-500
                                            group-hover:translate-x-0.5 group-hover:-translate-y-0.5
                                            transition-all duration-150" />
                  </div>
                  <p className="text-gray-500 text-xs font-medium mb-1 leading-tight">{label}</p>
                  <p className={`font-black text-xl md:text-2xl leading-tight ${val_color}`}>
                    {statValues[key]}
                  </p>
                </Link>
              ))}
            </div>

            {/* ── Giving + Sunday Report ── */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

              {/* Giving by category */}
              <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 shadow-sm p-5 md:p-6">
                <div className="flex items-center justify-between mb-5">
                  <div>
                    <h2 className="text-gray-900 font-bold text-sm">Giving by Category</h2>
                    <p className="text-gray-400 text-xs mt-0.5">All-time totals</p>
                  </div>
                  <Link href="/giving"
                    className="text-xs font-semibold text-indigo-600 hover:text-indigo-800
                               flex items-center gap-1 transition-colors">
                    View all <ArrowUpRight className="w-3 h-3" />
                  </Link>
                </div>
                {giving.length === 0 ? (
                  <div className="py-14 text-center">
                    <DollarSign className="w-8 h-8 text-gray-200 mx-auto mb-2" />
                    <p className="text-gray-400 text-sm">No giving records yet</p>
                    <Link href="/giving"
                      className="inline-flex items-center gap-1 mt-3 text-xs font-semibold
                                 text-indigo-600 hover:text-indigo-800">
                      + Record First Giving
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {giving.map(g => {
                      const pct = totalGiving > 0 ? Math.round(g.total_kes / totalGiving * 100) : 0
                      return (
                        <div key={g.category}>
                          <div className="flex items-center justify-between text-sm mb-2">
                            <span className="text-gray-700 font-semibold">{g.category}</span>
                            <div className="text-right">
                              <span className="text-gray-900 font-bold">
                                KES {g.total_kes.toLocaleString()}
                              </span>
                              <span className="text-gray-400 text-xs ml-1.5">({pct}%)</span>
                            </div>
                          </div>
                          <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                            <div
                              className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-purple-500
                                         transition-all duration-700"
                              style={{ width: pct + \'%\' }}
                            />
                          </div>
                        </div>
                      )
                    })}
                    <div className="pt-4 mt-2 border-t border-gray-100 flex justify-between items-center">
                      <span className="text-sm font-bold text-gray-700 flex items-center gap-1.5">
                        <TrendingUp className="w-4 h-4 text-emerald-500" /> Grand Total
                      </span>
                      <span className="text-base font-black text-emerald-600">
                        KES {totalGiving.toLocaleString()}
                      </span>
                    </div>
                  </div>
                )}
              </div>

              {/* Last Sunday Report */}
              <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 md:p-6">
                <div className="flex items-center justify-between mb-5">
                  <div>
                    <h2 className="text-gray-900 font-bold text-sm">Last Sunday Report</h2>
                    <p className="text-gray-400 text-xs mt-0.5">{lastSession?.session_date ?? \'—\'}</p>
                  </div>
                  <Link href="/attendance"
                    className="text-xs font-semibold text-indigo-600 hover:text-indigo-800
                               flex items-center gap-1">
                    All <ArrowUpRight className="w-3 h-3" />
                  </Link>
                </div>
                {!lastSession ? (
                  <div className="py-14 text-center">
                    <CalendarCheck className="w-8 h-8 text-gray-200 mx-auto mb-2" />
                    <p className="text-gray-400 text-sm">No sessions yet</p>
                    <Link href="/attendance"
                      className="inline-flex items-center gap-1 mt-3 text-xs font-semibold
                                 text-indigo-600 hover:text-indigo-800">
                      + Record First Session
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-0">
                    {[
                      { label: \'Total\',        value: lastSession.total_count,    highlight: \'font-black text-gray-900 text-base\' },
                      { label: \'Adults\',        value: lastSession.adult_count,    highlight: \'font-semibold text-gray-700\' },
                      { label: \'Children\',      value: lastSession.child_count,    highlight: \'font-semibold text-gray-700\' },
                      { label: \'First Timers\',  value: lastSession.first_time_visitors, highlight: \'font-bold text-amber-600\' },
                      { label: \'Salvations\',    value: lastSession.salvations,     highlight: \'font-bold text-emerald-600\' },
                      { label: \'Offering\',      value: \'KES \' + (lastSession.total_offering_kes||0).toLocaleString(), highlight: \'font-bold text-indigo-600\' },
                      { label: \'Tithe\',         value: \'KES \' + (lastSession.total_tithe_kes||0).toLocaleString(),    highlight: \'font-bold text-indigo-600\' },
                    ].map(({ label, value, highlight }) => (
                      <div key={label}
                        className="flex justify-between items-center py-2.5
                                   border-b border-gray-50 last:border-0">
                        <span className="text-xs text-gray-400 font-medium">{label}</span>
                        <span className={`text-sm ${highlight}`}>{value}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* ── Branch Overview ── */}
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 md:p-6">
              <div className="flex items-center justify-between mb-5">
                <div>
                  <h2 className="text-gray-900 font-bold text-sm">Branch Overview</h2>
                  <p className="text-gray-400 text-xs mt-0.5">All branches performance</p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {data?.branches?.map((b: any) => (
                  <div key={b.branch_id}
                    className="group border border-gray-100 rounded-xl p-4
                               hover:border-indigo-200 hover:bg-indigo-50/40
                               transition-all duration-200 cursor-pointer">
                    <div className="flex items-start justify-between mb-1">
                      <p className="font-bold text-gray-900 text-sm">{b.branch_name}</p>
                      <ArrowUpRight className="w-3.5 h-3.5 text-gray-300 group-hover:text-indigo-500
                                              transition-colors" />
                    </div>
                    <p className="text-xs text-gray-400 mb-4">
                      Pastor: {b.pastor || \'Pastor John Kamau\'}
                    </p>
                    <div className="flex gap-5 mb-3">
                      <div>
                        <p className="text-xs text-gray-400 font-medium mb-0.5">Members</p>
                        <p className="font-black text-gray-900 text-xl">{b.total_members}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-400 font-medium mb-0.5">Total Giving</p>
                        <p className="font-black text-emerald-600 text-xl">
                          KES {(b.total_giving_kes || 0).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <Link href="/giving"
                      className="text-xs font-semibold text-indigo-600 hover:text-indigo-800
                                 flex items-center gap-1 transition-colors">
                      View giving <ArrowUpRight className="w-3 h-3" />
                    </Link>
                  </div>
                ))}
              </div>
            </div>

          </>)}
        </div>
      </main>
    </div>
  )
}
'''
open('/app/frontend/pages/dashboard.tsx', 'w').write(txt)
print('Dashboard done')
