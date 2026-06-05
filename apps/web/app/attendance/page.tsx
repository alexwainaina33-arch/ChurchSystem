'use client'
import { useEffect, useState, useRef } from 'react'
import Sidebar from '../../components/Sidebar'
import api from '../../lib/api'
import Link from 'next/link'
import { Plus, ChevronRight, Download, Calendar, X, Users, Heart, FileText, TrendingUp } from 'lucide-react'

const CHURCH_ID = '00000000-0000-0000-0000-000000000001'
const BRANCH_ID = '00000000-0000-0000-0000-000000000002'

function AttendanceTrendChart({ sessions }: { sessions: any[] }) {
  if (sessions.length < 2) return null
  const sorted = [...sessions].sort((a,b) => a.session_date.localeCompare(b.session_date)).slice(-10)
  const maxVal = Math.max(...sorted.map(s => s.total_count), 1)
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 md:p-6">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-sm font-bold text-gray-900">Attendance Trend</h2>
          <p className="text-xs text-gray-400 mt-0.5">Last {sorted.length} sessions</p>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-indigo-500 inline-block"/>Total</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-sky-400 inline-block"/>Adults</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-emerald-400 inline-block"/>Children</span>
        </div>
      </div>
      <div className="flex items-end gap-2 h-40 overflow-x-auto pb-2">
        {sorted.map((s, i) => {
          const totalH = Math.round((s.total_count / maxVal) * 140)
          const adultH = Math.round((s.adult_count / maxVal) * 140)
          const childH = Math.round((s.child_count  / maxVal) * 140)
          return (
            <div key={i} className="flex flex-col items-center gap-1 flex-1 min-w-[52px] group relative">
              <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs rounded-lg px-2.5 py-1.5 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 pointer-events-none shadow-lg">
                <p className="font-bold">{s.session_date}</p>
                <p>Total: {s.total_count}</p>
                <p>Adults: {s.adult_count} · Kids: {s.child_count}</p>
                {s.first_time_visitors > 0 && <p>First-timers: {s.first_time_visitors}</p>}
              </div>
              <div className="flex items-end gap-0.5 h-36">
                <div className="w-3 rounded-t-sm bg-indigo-500 transition-all duration-500" style={{height: totalH + 'px'}} />
                <div className="w-3 rounded-t-sm bg-sky-400 transition-all duration-500" style={{height: adultH + 'px'}} />
                <div className="w-3 rounded-t-sm bg-emerald-400 transition-all duration-500" style={{height: childH + 'px'}} />
              </div>
              <span className="text-[10px] text-gray-400 truncate w-full text-center">{s.session_date.slice(5)}</span>
            </div>
          )
        })}
      </div>
      <div className="mt-3 pt-3 border-t border-gray-100 grid grid-cols-3 gap-3 text-center">
        {[
          { label: 'Avg Attendance',   value: Math.round(sorted.reduce((s,x) => s+x.total_count,0)/sorted.length) },
          { label: 'Avg First-timers', value: Math.round(sorted.reduce((s,x) => s+x.first_time_visitors,0)/sorted.length) },
          { label: 'Total Salvations', value: sorted.reduce((s,x) => s+x.salvations,0) },
        ].map(({ label, value }) => (
          <div key={label}>
            <p className="text-lg font-black text-gray-800">{value}</p>
            <p className="text-xs text-gray-400">{label}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function AttendancePage() {
  const [sessions, setSessions]     = useState<any[]>([])
  const [showForm, setShowForm]     = useState(false)
  const [loading, setLoading]       = useState(true)
  const [saving, setSaving]         = useState(false)
  const [showExport, setShowExport] = useState(false)
  const [dateFrom, setDateFrom]     = useState('')
  const [dateTo, setDateTo]         = useState('')
  const formRef = useRef<HTMLFormElement>(null)

  const load = () => {
    setLoading(true)
    api.get('/attendance/sessions/?church_id=' + CHURCH_ID)
      .then(r => setSessions(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const filteredSessions = sessions.filter((s: any) => {
    const d = s.session_date || ''
    if (dateFrom && d < dateFrom) return false
    if (dateTo   && d > dateTo)   return false
    return true
  })

  const n = (v: any) => Number(v) || 0

  const save = async () => {
    const form = formRef.current
    if (!form) return
    const d: any = Object.fromEntries(new FormData(form))
    if (!d.session_date) return alert('Session date is required')
    setSaving(true)
    try {
      await api.post('/attendance/sessions/', {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        session_date: d.session_date, session_type: d.session_type,
        service_name: d.service_name || '',
        adult_count: n(d.adult_count), child_count: n(d.child_count),
        total_count: n(d.adult_count) + n(d.child_count),
        male_count: n(d.male_count), female_count: n(d.female_count),
        first_time_visitors: n(d.first_time_visitors), salvations: n(d.salvations),
        cars_count: n(d.cars_count), motorbikes_count: n(d.motorbikes_count),
        total_offering_kes: n(d.total_offering_kes),
        total_tithe_kes: n(d.total_tithe_kes),
        project_offering_kes: n(d.project_offering_kes),
        notes: d.notes || ''
      })
      setShowForm(false)
      load()
    } catch(e: any) {
      alert('Error: ' + (e.response?.data?.detail || e.message))
    } finally { setSaving(false) }
  }

  const exportCSV = () => {
    const headers = ['Date','Service','Adults','Children','Total','Male','Female','First Timers','Salvations','Cars','Motorbikes','Offering(KES)','Tithe(KES)','Project(KES)']
    const rows = filteredSessions.map((s: any) => [s.session_date, s.service_name||s.session_type, s.adult_count, s.child_count, s.total_count, s.male_count, s.female_count, s.first_time_visitors, s.salvations, s.cars_count, s.motorbikes_count, s.total_offering_kes, s.total_tithe_kes, s.project_offering_kes])
    const csv = [headers, ...rows].map(r => r.join(',')).join('\n')
    const a = document.createElement('a')
    a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv)
    a.download = 'attendance_' + new Date().toISOString().slice(0,10) + '.csv'
    a.click()
    setShowExport(false)
  }

  const printReport = () => {
    const periodLabel = dateFrom || dateTo ? 'Period: ' + (dateFrom||'All') + ' to ' + (dateTo||'All') : 'All sessions'
    const totalAttendance = filteredSessions.reduce((s,x) => s+x.total_count,0)
    const totalOffering   = filteredSessions.reduce((s,x) => s+x.total_offering_kes,0)
    const totalSalvations = filteredSessions.reduce((s,x) => s+x.salvations,0)
    const rows = filteredSessions.map((s: any) =>
      '<tr><td>' + s.session_date + '</td><td>' + (s.service_name||s.session_type) + '</td><td style="font-weight:bold">' + s.total_count + '</td><td>' + s.adult_count + ' / ' + s.child_count + '</td><td style="color:#d97706;font-weight:bold">' + s.first_time_visitors + '</td><td style="color:#16a34a;font-weight:bold">' + s.salvations + '</td><td>KES ' + s.total_offering_kes.toLocaleString() + '</td><td style="font-weight:bold;color:#4338ca">KES ' + s.total_tithe_kes.toLocaleString() + '</td></tr>'
    ).join('')
    const win = window.open('','_blank')
    if (!win) return
    win.document.write('<!DOCTYPE html><html><head><title>Attendance Report</title><style>body{font-family:Arial,sans-serif;padding:30px;color:#333}h1{color:#4338ca;font-size:22px;margin:0 0 4px}.meta{font-size:12px;color:#888;margin-bottom:6px}.period{background:#f0f0ff;border:1px solid #c7d2fe;border-radius:6px;padding:6px 12px;display:inline-block;font-size:12px;color:#4338ca;font-weight:600;margin-bottom:16px}.summary{display:flex;gap:24px;margin-bottom:20px}.stat{background:#f8f8ff;border:1px solid #e0e0ff;border-radius:8px;padding:10px 16px;min-width:120px}.stat .val{font-size:22px;font-weight:900;color:#4338ca}.stat .lbl{font-size:11px;color:#888;margin-top:2px}table{width:100%;border-collapse:collapse}th{background:#4338ca;color:#fff;padding:9px 10px;text-align:left;font-size:11px;text-transform:uppercase}td{padding:9px 10px;border-bottom:1px solid #eee;font-size:12px}tr:nth-child(even){background:#f8f8ff}.footer{margin-top:24px;text-align:center;font-size:11px;color:#aaa;border-top:1px solid #eee;padding-top:12px}</style></head><body><h1>ChurchHub &mdash; Attendance Report</h1><p class="meta">Grace Community Church &mdash; Nairobi, Kenya</p><div class="period">' + periodLabel + '</div><div class="summary"><div class="stat"><div class="val">' + totalAttendance.toLocaleString() + '</div><div class="lbl">Total Attendance</div></div><div class="stat"><div class="val">' + totalSalvations + '</div><div class="lbl">Salvations</div></div><div class="stat"><div class="val">KES ' + totalOffering.toLocaleString() + '</div><div class="lbl">Total Offering</div></div><div class="stat"><div class="val">' + filteredSessions.length + '</div><div class="lbl">Sessions</div></div></div><table><thead><tr><th>Date</th><th>Service</th><th>Total</th><th>Adult/Child</th><th>First Timers</th><th>Salvations</th><th>Offering</th><th>Tithe</th></tr></thead><tbody>' + rows + '</tbody></table><div class="footer">Generated by ChurchHub &mdash; ' + new Date().toLocaleString() + '</div></body></html>')
    win.document.close()
    win.print()
    setShowExport(false)
  }

  const NF = ({ label, name }: { label: string, name: string }) => (
    <div>
      <label className="text-xs text-gray-500 font-medium mb-1.5 block">{label}</label>
      <input type="number" min="0" name={name} placeholder="0"
        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
    </div>
  )

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 min-w-0 pb-24 md:pb-0">
        <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200 px-4 md:px-8 py-3.5 shadow-sm">
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
              <div className="relative">
                <button onClick={() => setShowExport(!showExport)}
                  className="flex items-center gap-1.5 border border-gray-200 text-gray-600 px-3 py-2 rounded-xl text-sm hover:bg-gray-50 transition-colors">
                  <Download className="w-4 h-4" />
                  <span className="hidden sm:inline">Export</span>
                </button>
                {showExport && (
                  <div className="absolute right-0 top-full mt-1 bg-white border border-gray-200 rounded-xl shadow-lg z-50 w-48 overflow-hidden">
                    <button onClick={exportCSV} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2">
                      <FileText className="w-4 h-4" /> Export CSV
                    </button>
                    <button onClick={printReport} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2">
                      <FileText className="w-4 h-4" /> Print Sunday Report
                    </button>
                  </div>
                )}
              </div>
              <button onClick={() => setShowForm(true)}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-3 md:px-4 py-2 rounded-xl text-sm font-semibold shadow-sm shadow-indigo-200 transition-all active:scale-95">
                <Plus className="w-4 h-4" />
                <span className="hidden sm:inline">New Session</span>
                <span className="sm:hidden">New</span>
              </button>
            </div>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-5">
          <AttendanceTrendChart sessions={sessions} />

          {sessions.length > 0 && (
            <div className="flex items-center gap-3 flex-wrap bg-white border border-gray-100 rounded-2xl px-4 py-3 shadow-sm">
              <span className="text-xs text-gray-500 font-semibold uppercase tracking-wide">Filter by date</span>
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2">
                <span className="text-xs text-gray-400">From</span>
                <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)} className="text-sm text-gray-700 bg-transparent focus:outline-none" />
              </div>
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2">
                <span className="text-xs text-gray-400">To</span>
                <input type="date" value={dateTo} onChange={e => setDateTo(e.target.value)} className="text-sm text-gray-700 bg-transparent focus:outline-none" />
              </div>
              {(dateFrom || dateTo) && (
                <button onClick={() => { setDateFrom(''); setDateTo('') }} className="text-xs text-red-500 font-medium hover:text-red-700">Clear</button>
              )}
            </div>
          )}

          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            {loading ? (
              <div className="flex items-center justify-center py-20 gap-3">
                <div className="w-7 h-7 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
                <span className="text-gray-400 text-sm">Loading sessions...</span>
              </div>
            ) : filteredSessions.length === 0 ? (
              <div className="py-20 text-center">
                <Calendar className="w-10 h-10 text-gray-200 mx-auto mb-3" />
                <p className="text-gray-400 text-sm mb-3">{sessions.length === 0 ? 'No sessions recorded yet' : 'No sessions in this date range'}</p>
                {sessions.length === 0 && (
                  <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-semibold hover:text-indigo-800">+ Record First Session</button>
                )}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full min-w-[750px]">
                  <thead className="bg-gray-50 border-b border-gray-100">
                    <tr>
                      {['Date','Service','Attendance','First Timers','Salvations','Offering','Tithe',''].map(h => (
                        <th key={h} className="text-left text-xs text-gray-500 font-semibold uppercase tracking-wide px-4 py-3">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {filteredSessions.map((s: any) => (
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
                        <td className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">KES {s.total_offering_kes.toLocaleString()}</td>
                        <td className="px-4 py-3 text-sm font-semibold text-indigo-700 whitespace-nowrap">KES {s.total_tithe_kes.toLocaleString()}</td>
                        <td className="px-4 py-3">
                          <Link href={"/giving?session_id=" + s.id} className="flex items-center gap-1 text-indigo-600 text-xs font-semibold hover:text-indigo-800 whitespace-nowrap transition-colors opacity-60 group-hover:opacity-100">
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

          {sessions.length > 0 && (
            <div className="flex items-center justify-between bg-indigo-50 border border-indigo-100 rounded-2xl px-5 py-3.5">
              <p className="text-sm text-indigo-700 font-medium">Record giving for the latest session</p>
              <Link href="/giving" className="flex items-center gap-1.5 bg-indigo-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-indigo-700 transition-colors">
                Record Giving <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          )}
        </div>

        {showForm && (
          <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center p-0 md:p-4">
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowForm(false)} />
            <div className="relative bg-white w-full md:max-w-2xl rounded-t-3xl md:rounded-2xl shadow-2xl max-h-[92vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between rounded-t-3xl md:rounded-t-2xl z-10">
                <div>
                  <h2 className="text-base font-bold text-gray-900">New Attendance Session</h2>
                  <p className="text-xs text-gray-400 mt-0.5">Sunday Report — fill all fields</p>
                </div>
                <button onClick={() => setShowForm(false)} className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200">
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
              <div className="p-6">
                <form ref={formRef}>
                  <div className="grid grid-cols-2 gap-4 mb-5">
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Date *</label>
                      <input type="date" name="session_date" className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Session Type</label>
                      <select name="session_type" className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none bg-gray-50/50">
                        <option value="sunday_service">Sunday Service</option>
                        <option value="midweek">Midweek Service</option>
                        <option value="special">Special Service</option>
                      </select>
                    </div>
                    <div className="col-span-2">
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Service Name</label>
                      <input type="text" name="service_name" placeholder="e.g. Sunday 1st Service" className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
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
                    <textarea name="notes" rows={2} className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50 resize-none" />
                  </div>
                </form>
                <div className="flex gap-3 mt-5">
                  <button onClick={() => setShowForm(false)} className="flex-1 border border-gray-200 text-gray-600 py-3 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors">Cancel</button>
                  <button onClick={save} disabled={saving} className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl text-sm font-semibold shadow-sm shadow-indigo-200 transition-all disabled:opacity-50 active:scale-[0.98]">
                    {saving ? 'Saving...' : 'Save Session →'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        {showExport && <div className="fixed inset-0 z-40" onClick={() => setShowExport(false)} />}
      </main>
    </div>
  )
}
