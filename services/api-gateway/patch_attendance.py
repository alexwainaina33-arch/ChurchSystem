import os
txt = '''\'use client\'
import { useEffect, useState, useRef } from \'react\'
import Sidebar from \'../components/Sidebar\'
import api from \'../lib/api\'
import Link from \'next/link\'
import { Plus, ChevronRight, Download, Calendar, X, Users, Heart, Car } from \'lucide-react\'

const CHURCH_ID = \'00000000-0000-0000-0000-000000000001\'
const BRANCH_ID = \'00000000-0000-0000-0000-000000000002\'

export default function AttendancePage() {
  const [sessions, setSessions] = useState<any[]>([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading]   = useState(true)
  const [saving, setSaving]     = useState(false)
  const formRef = useRef<HTMLFormElement>(null)

  const load = () => {
    setLoading(true)
    api.get(\'/attendance/sessions/?church_id=\' + CHURCH_ID)
      .then(r => setSessions(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const n = (v: any) => Number(v) || 0

  const save = async () => {
    const form = formRef.current
    if (!form) return
    const d: any = Object.fromEntries(new FormData(form))
    if (!d.session_date) return alert(\'Session date is required\')
    setSaving(true)
    try {
      await api.post(\'/attendance/sessions/\', {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        session_date: d.session_date, session_type: d.session_type,
        service_name: d.service_name || \'\',
        adult_count: n(d.adult_count), child_count: n(d.child_count),
        total_count: n(d.adult_count) + n(d.child_count),
        male_count: n(d.male_count), female_count: n(d.female_count),
        first_time_visitors: n(d.first_time_visitors), salvations: n(d.salvations),
        cars_count: n(d.cars_count), motorbikes_count: n(d.motorbikes_count),
        total_offering_kes: n(d.total_offering_kes),
        total_tithe_kes: n(d.total_tithe_kes),
        project_offering_kes: n(d.project_offering_kes),
        notes: d.notes || \'\'
      })
      setShowForm(false)
      load()
    } catch(e: any) {
      alert(\'Error: \' + (e.response?.data?.detail || e.message))
    } finally { setSaving(false) }
  }

  const exportCSV = () => {
    const headers = [\'Date\',\'Service\',\'Adults\',\'Children\',\'Total\',\'Male\',\'Female\',\'First Timers\',\'Salvations\',\'Cars\',\'Motorbikes\',\'Offering(KES)\',\'Tithe(KES)\',\'Project(KES)\']
    const rows = sessions.map((s: any) => [s.session_date, s.service_name||s.session_type, s.adult_count, s.child_count, s.total_count, s.male_count, s.female_count, s.first_time_visitors, s.salvations, s.cars_count, s.motorbikes_count, s.total_offering_kes, s.total_tithe_kes, s.project_offering_kes])
    const csv = [headers, ...rows].map(r => r.join(\',\')).join(\'\\n\')
    const a = document.createElement(\'a\')
    a.href = \'data:text/csv;charset=utf-8,\' + encodeURIComponent(csv)
    a.download = \'attendance_report.csv\'; a.click()
  }

  const NF = ({ label, name }: { label: string, name: string }) => (
    <div>
      <label className="text-xs text-gray-500 font-medium mb-1.5 block">{label}</label>
      <input type="number" min="0" name={name} placeholder="0"
        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                   focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
    </div>
  )

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 min-w-0 pb-24 md:pb-0">

        <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200
                           px-4 md:px-8 py-3.5 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="ml-12 md:ml-0">
              <div className="flex items-center gap-2 text-xs text-gray-400 mb-0.5">
                <Link href="/" className="hover:text-indigo-600 transition-colors">Dashboard</Link>
                <ChevronRight className="w-3 h-3" />
                <span className="text-gray-600 font-medium">Attendance</span>
              </div>
              <h1 className="text-gray-900 font-bold text-lg leading-tight">
                Attendance
                <span className="ml-2 text-sm font-normal text-gray-400">{sessions.length} sessions</span>
              </h1>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={exportCSV}
                className="flex items-center gap-1.5 border border-gray-200 text-gray-600
                           px-3 py-2 rounded-xl text-sm hover:bg-gray-50 transition-colors">
                <Download className="w-4 h-4" />
                <span className="hidden sm:inline">Export</span>
              </button>
              <button onClick={() => setShowForm(true)}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700
                           text-white px-3 md:px-4 py-2 rounded-xl text-sm font-semibold
                           shadow-sm shadow-indigo-200 transition-all active:scale-95">
                <Plus className="w-4 h-4" />
                <span className="hidden sm:inline">New Session</span>
                <span className="sm:hidden">New</span>
              </button>
            </div>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-7xl mx-auto">
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            {loading ? (
              <div className="flex items-center justify-center py-20 gap-3">
                <div className="w-7 h-7 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
                <span className="text-gray-400 text-sm">Loading sessions...</span>
              </div>
            ) : sessions.length === 0 ? (
              <div className="py-20 text-center">
                <Calendar className="w-10 h-10 text-gray-200 mx-auto mb-3" />
                <p className="text-gray-400 text-sm mb-3">No sessions recorded yet</p>
                <button onClick={() => setShowForm(true)}
                  className="text-indigo-600 text-sm font-semibold hover:text-indigo-800">
                  + Record First Session
                </button>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full min-w-[750px]">
                  <thead className="bg-gray-50 border-b border-gray-100">
                    <tr>
                      {[\'Date\',\'Service\',\'Attendance\',\'First Timers\',\'Salvations\',\'Offering\',\'Tithe\',\'\'].map(h => (
                        <th key={h} className="text-left text-xs text-gray-500 font-semibold
                                               uppercase tracking-wide px-4 py-3">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {sessions.map((s: any) => (
                      <tr key={s.id} className="hover:bg-indigo-50/30 transition-colors group">
                        <td className="px-4 py-3 text-sm font-semibold text-gray-800 whitespace-nowrap">{s.session_date}</td>
                        <td className="px-4 py-3 text-sm text-gray-600">{s.service_name || s.session_type}</td>
                        <td className="px-4 py-3">
                          <span className="text-sm font-bold text-gray-800">{s.total_count}</span>
                          <span className="text-xs text-gray-400 ml-1.5">{s.adult_count}A / {s.child_count}C</span>
                        </td>
                        <td className="px-4 py-3">
                          <span className="inline-flex items-center gap-1 text-sm font-semibold text-amber-600">
                            <Users className="w-3.5 h-3.5" /> {s.first_time_visitors}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <span className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-600">
                            <Heart className="w-3.5 h-3.5" /> {s.salvations}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">
                          KES {s.total_offering_kes.toLocaleString()}
                        </td>
                        <td className="px-4 py-3 text-sm font-semibold text-indigo-700 whitespace-nowrap">
                          KES {s.total_tithe_kes.toLocaleString()}
                        </td>
                        <td className="px-4 py-3">
                          <Link href={"/giving?session_id=" + s.id}
                            className="flex items-center gap-1 text-indigo-600 text-xs font-semibold
                                       hover:text-indigo-800 whitespace-nowrap transition-colors
                                       opacity-60 group-hover:opacity-100">
                            Record Giving <ChevronRight className="w-3 h-3" />
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Modal — slides up on mobile, centered on desktop */}
        {showForm && (
          <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center p-0 md:p-4">
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowForm(false)} />
            <div className="relative bg-white w-full md:max-w-2xl rounded-t-3xl md:rounded-2xl
                            shadow-2xl max-h-[92vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4
                              flex items-center justify-between rounded-t-3xl md:rounded-t-2xl z-10">
                <div>
                  <h2 className="text-base font-bold text-gray-900">New Attendance Session</h2>
                  <p className="text-xs text-gray-400 mt-0.5">Sunday Report — fill all fields</p>
                </div>
                <button onClick={() => setShowForm(false)}
                  className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100
                             hover:bg-gray-200 transition-colors">
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
              <div className="p-6">
                <form ref={formRef}>
                  <div className="grid grid-cols-2 gap-4 mb-5">
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Date *</label>
                      <input type="date" name="session_date"
                        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                   focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Session Type</label>
                      <select name="session_type"
                        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                   focus:outline-none bg-gray-50/50">
                        <option value="sunday_service">Sunday Service</option>
                        <option value="midweek">Midweek Service</option>
                        <option value="special">Special Service</option>
                      </select>
                    </div>
                    <div className="col-span-2">
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Service Name</label>
                      <input type="text" name="service_name" placeholder="e.g. Sunday 1st Service"
                        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                   focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                    </div>
                  </div>

                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Head Count</p>
                  <div className="grid grid-cols-3 gap-3 mb-5">
                    <NF label="Adults" name="adult_count" />
                    <NF label="Children" name="child_count" />
                    <NF label="Male" name="male_count" />
                    <NF label="Female" name="female_count" />
                    <NF label="First Timers" name="first_time_visitors" />
                    <NF label="Salvations" name="salvations" />
                  </div>

                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Transport</p>
                  <div className="grid grid-cols-2 gap-3 mb-5">
                    <NF label="Cars" name="cars_count" />
                    <NF label="Motorbikes" name="motorbikes_count" />
                  </div>

                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Financials (KES)</p>
                  <div className="grid grid-cols-3 gap-3 mb-5">
                    <NF label="Total Offering" name="total_offering_kes" />
                    <NF label="Total Tithe" name="total_tithe_kes" />
                    <NF label="Project Offering" name="project_offering_kes" />
                  </div>

                  <div className="mb-2">
                    <label className="text-xs text-gray-500 font-medium mb-1.5 block">Notes</label>
                    <textarea name="notes" rows={2}
                      className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                 focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50 resize-none" />
                  </div>
                </form>
                <div className="flex gap-3 mt-5">
                  <button onClick={() => setShowForm(false)}
                    className="flex-1 border border-gray-200 text-gray-600 py-3 rounded-xl text-sm
                               font-medium hover:bg-gray-50 transition-colors">Cancel</button>
                  <button onClick={save} disabled={saving}
                    className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl
                               text-sm font-semibold shadow-sm shadow-indigo-200 transition-all
                               disabled:opacity-50 active:scale-[0.98]">
                    {saving ? \'Saving...\' : \'Save Session →\'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
'''
open('/app/frontend/pages/attendance.tsx', 'w').write(txt)
print('Attendance done')
