'use client'
import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Sidebar from '../../components/Sidebar'
import api from '../../lib/api'
import Link from 'next/link'
import { Download, FileText, ChevronRight, X } from 'lucide-react'

const CID = '00000000-0000-0000-0000-000000000001'
const BID = '00000000-0000-0000-0000-000000000002'

export default function GivingPage() {
  const router = useRouter()
  const [records, setRecords]                   = useState<any[]>([])
  const [categories, setCategories]             = useState<any[]>([])
  const [members, setMembers]                   = useState<any[]>([])
  const [filteredMembers, setFilteredMembers]   = useState<any[]>([])
  const [showDropdown, setShowDropdown]         = useState(false)
  const [selectedMember, setSelectedMember]     = useState<any>(null)
  const [search, setSearch]                     = useState('')
  const [summary, setSummary]                   = useState<any[]>([])
  const [showForm, setShowForm]                 = useState(false)
  const [saving, setSaving]                     = useState(false)
  const [msg, setMsg]                           = useState('')
  const [showExport, setShowExport]             = useState(false)
  const [dateFrom, setDateFrom]                 = useState('')
  const [dateTo, setDateTo]                     = useState('')
  const formRef = useRef<HTMLFormElement>(null)

  useEffect(() => { load() }, [])

  async function load() {
    try {
      const [r, c, m, s] = await Promise.all([
        api.get('/giving/records/?church_id=' + CID).then(x => x.data),
        api.get('/giving/categories/?church_id=' + CID).then(x => x.data),
        api.get('/members/?church_id=' + CID + '&limit=200').then(x => x.data),
        api.get('/giving/summary/?church_id=' + CID).then(x => x.data),
      ])
      setRecords(Array.isArray(r) ? r : [])
      setCategories(Array.isArray(c) ? c : [])
      setMembers(Array.isArray(m) ? m : [])
      setSummary(Array.isArray(s) ? s : [])
    } catch(e: any) { console.error(e) }
  }

  const filteredRecords = records.filter((r: any) => {
    const d = r.created_at?.slice(0,10) || ''
    if (dateFrom && d < dateFrom) return false
    if (dateTo   && d > dateTo)   return false
    return true
  })

  const totalFiltered = filteredRecords.reduce((s, r) => s + r.amount_kes, 0)
  const grandTotal    = records.reduce((s, r) => s + r.amount_kes, 0)

  const summaryMap: Record<string,number> = {}
  summary.forEach((s: any) => { summaryMap[s.category?.toUpperCase()] = s.total_kes })

  function searchMembers(v: string) {
    setSearch(v)
    setSelectedMember(null)
    if (v.length < 1) { setFilteredMembers([]); return }
    setFilteredMembers(members.filter((m: any) =>
      (m.first_name + ' ' + m.last_name).toLowerCase().includes(v.toLowerCase()) ||
      (m.phone || '').includes(v)
    ).slice(0, 6))
    setShowDropdown(true)
  }

  function pickMember(m: any) {
    setSelectedMember(m)
    setSearch(m.first_name + ' ' + m.last_name)
    setShowDropdown(false)
    setFilteredMembers([])
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    if (!selectedMember) { setMsg('Please select a member'); return }
    setSaving(true); setMsg('')
    const fd = new FormData(formRef.current!)
    const body = {
      church_id: CID, branch_id: BID,
      member_id: selectedMember.id,
      category_id: fd.get('category_id'),
      amount_kes: Number(fd.get('amount_kes')),
      payment_method: fd.get('payment_method'),
      mpesa_ref: fd.get('mpesa_ref') || null,
      envelope_number: fd.get('envelope_number') || null,
      notes: fd.get('notes') || null,
    }
    try {
      const res = await api.post('/giving/records/', body)
      setMsg('Saved!')
      setShowForm(false)
      setSelectedMember(null)
      setSearch('')
      formRef.current?.reset()
      load()
    } catch(e: any) {
      setMsg(e.response?.data?.detail || 'Cannot connect to server')
    }
    setSaving(false)
  }

  const exportCSV = () => {
    const headers = ['Date','Member','Category','Amount (KES)','Method','M-Pesa Ref']
    const rows = filteredRecords.map((r: any) => [
      r.created_at?.slice(0,10)||'', r.member_name||'', r.category_name||'',
      r.amount_kes, r.payment_method||'', r.mpesa_ref||''
    ])
    const csv = [headers, ...rows].map(r => r.map((v:any) => '"' + String(v).replace(/"/g,'""') + '"').join(',')).join('\n')
    const a = document.createElement('a')
    a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv)
    a.download = 'giving_' + new Date().toISOString().slice(0,10) + '.csv'
    a.click()
    setShowExport(false)
  }

  const exportExcel = () => {
    const headers = ['Date','Member','Category','Amount (KES)','Method','M-Pesa Ref']
    const rows = filteredRecords.map((r: any) => [
      r.created_at?.slice(0,10)||'', r.member_name||'', r.category_name||'',
      r.amount_kes, r.payment_method||'', r.mpesa_ref||''
    ])
    const tsv = [headers, ...rows].map(r => r.join('\t')).join('\n')
    const a = document.createElement('a')
    a.href = 'data:application/vnd.ms-excel;charset=utf-8,' + encodeURIComponent(tsv)
    a.download = 'giving_' + new Date().toISOString().slice(0,10) + '.xls'
    a.click()
    setShowExport(false)
  }

  const printReport = () => {
    const periodLabel = dateFrom || dateTo
      ? 'Period: ' + (dateFrom||'All') + ' to ' + (dateTo||'All')
      : 'All-time giving report'
    const rows = filteredRecords.map((r: any) =>
      '<tr><td>' + (r.created_at?.slice(0,10)||'—') + '</td><td>' + (r.member_name||'—') + '</td><td>' + (r.category_name||'—') + '</td><td style="font-weight:bold;color:#16a34a">KES ' + r.amount_kes.toLocaleString() + '</td><td style="text-transform:capitalize">' + (r.payment_method||'—') + '</td><td>' + (r.mpesa_ref||'—') + '</td></tr>'
    ).join('')
    const win = window.open('','_blank')
    if (!win) return
    win.document.write('<!DOCTYPE html><html><head><title>Giving Report</title><style>body{font-family:Arial,sans-serif;padding:30px;color:#333}h1{color:#4338ca;font-size:22px;margin:0 0 4px}.sub{color:#6366f1;font-size:13px;margin:0 0 16px}.period{background:#f0f0ff;border:1px solid #c7d2fe;border-radius:6px;padding:6px 12px;display:inline-block;font-size:12px;color:#4338ca;font-weight:600;margin-bottom:16px}table{width:100%;border-collapse:collapse}th{background:#4338ca;color:#fff;padding:9px 10px;text-align:left;font-size:11px;text-transform:uppercase}td{padding:9px 10px;border-bottom:1px solid #eee;font-size:12px}tr:nth-child(even){background:#f8f8ff}.total{background:#e8f5e9;font-weight:bold;font-size:13px}.footer{margin-top:24px;text-align:center;font-size:11px;color:#aaa;border-top:1px solid #eee;padding-top:12px}</style></head><body><h1>ChurchHub &mdash; Giving Report</h1><p class="sub">Grace Community Church &mdash; Nairobi, Kenya</p><div class="period">' + periodLabel + '</div><table><thead><tr><th>Date</th><th>Member</th><th>Category</th><th>Amount</th><th>Method</th><th>M-Pesa Ref</th></tr></thead><tbody>' + rows + '<tr class="total"><td colspan="3"><strong>TOTAL (' + filteredRecords.length + ' records)</strong></td><td colspan="3"><strong style="color:#16a34a">KES ' + totalFiltered.toLocaleString() + '</strong></td></tr></tbody></table><div class="footer">Generated by ChurchHub &mdash; ' + new Date().toLocaleString() + '</div></body></html>')
    win.document.close()
    win.print()
    setShowExport(false)
  }

  const fmt = (n: number) => 'KES ' + (n || 0).toLocaleString()

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
                <span className="text-gray-600 font-medium">Giving</span>
              </div>
              <h1 className="text-gray-900 font-bold text-lg leading-tight">
                Giving
                <span className="ml-2 text-sm font-normal text-gray-400">{records.length} records</span>
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
                  <div className="absolute right-0 top-full mt-1 bg-white border border-gray-200 rounded-xl shadow-lg z-50 w-44 overflow-hidden">
                    <button onClick={exportCSV} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2 transition-colors">
                      <FileText className="w-4 h-4" /> Export CSV
                    </button>
                    <button onClick={exportExcel} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2 transition-colors">
                      <FileText className="w-4 h-4" /> Export Excel
                    </button>
                    <button onClick={printReport} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2 transition-colors">
                      <FileText className="w-4 h-4" /> Print PDF Report
                    </button>
                  </div>
                )}
              </div>
              <button onClick={() => setShowForm(true)}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-3 md:px-4 py-2 rounded-xl text-sm font-semibold shadow-sm shadow-indigo-200 transition-all active:scale-95">
                + <span className="hidden sm:inline">Record Giving</span>
                <span className="sm:hidden">Record</span>
              </button>
            </div>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-5xl mx-auto space-y-5">

          {/* Summary cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
            {[
              { label: 'Tithe',    key: 'TITHE',      color: 'text-indigo-700' },
              { label: 'Offering', key: 'OFFERING',   color: 'text-sky-700'    },
              { label: 'Project',  key: 'PROJECT',    color: 'text-amber-700'  },
              { label: 'Total',    key: '__TOTAL__',  color: 'text-emerald-700' },
            ].map(({ label, key, color }) => (
              <div key={key} className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
                <p className="text-xs text-gray-500 mb-1 font-medium">{label}</p>
                <p className={'text-lg font-bold ' + color}>
                  {fmt(key === '__TOTAL__' ? grandTotal : (summaryMap[key] || 0))}
                </p>
              </div>
            ))}
          </div>

          {/* Date range filter */}
          <div className="flex items-center gap-3 flex-wrap bg-white border border-gray-100 rounded-2xl px-4 py-3 shadow-sm">
            <span className="text-xs text-gray-500 font-semibold uppercase tracking-wide">Filter by date</span>
            <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2">
              <span className="text-xs text-gray-400">From</span>
              <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)}
                className="text-sm text-gray-700 bg-transparent focus:outline-none" />
            </div>
            <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2">
              <span className="text-xs text-gray-400">To</span>
              <input type="date" value={dateTo} onChange={e => setDateTo(e.target.value)}
                className="text-sm text-gray-700 bg-transparent focus:outline-none" />
            </div>
            {(dateFrom || dateTo) && (
              <>
                <span className="text-xs font-bold text-emerald-600">
                  {filteredRecords.length} records · {fmt(totalFiltered)}
                </span>
                <button onClick={() => { setDateFrom(''); setDateTo('') }}
                  className="text-xs text-red-500 font-medium hover:text-red-700">Clear</button>
              </>
            )}
          </div>

          {msg && (
            <div className="px-4 py-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm">{msg}</div>
          )}

          {/* Records table */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
              <h2 className="text-sm font-bold text-gray-700">
                {dateFrom || dateTo ? 'Filtered Records (' + filteredRecords.length + ')' : 'All Giving Records'}
              </h2>
              {(dateFrom || dateTo) && (
                <span className="text-xs font-bold text-emerald-600">Total: {fmt(totalFiltered)}</span>
              )}
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">Member</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">Category</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">Amount</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">Method</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">Date</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {filteredRecords.length === 0 && (
                    <tr><td colSpan={6} className="text-center py-12 text-gray-400 text-sm">
                      {records.length === 0 ? 'No giving records yet' : 'No records in this date range'}
                    </td></tr>
                  )}
                  {filteredRecords.map((r: any) => (
                    <tr key={r.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 font-medium text-gray-800">{r.member_name || 'Unknown'}</td>
                      <td className="px-4 py-3">
                        <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-700">
                          {r.category_name || 'N/A'}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-bold text-gray-800">{fmt(r.amount_kes)}</td>
                      <td className="px-4 py-3 text-gray-500 capitalize">{r.payment_method}</td>
                      <td className="px-4 py-3 text-gray-400 text-xs">{r.created_at?.slice(0,10)}</td>
                      <td className="px-4 py-3">
                        <button onClick={() => router.push('/members/' + r.member_id)}
                          className="text-xs text-indigo-600 hover:underline font-semibold flex items-center gap-1">
                          View Member <ChevronRight className="w-3 h-3" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Next step CTA */}
          {records.length > 0 && (
            <div className="flex items-center justify-between bg-emerald-50 border border-emerald-100 rounded-2xl px-5 py-3.5">
              <p className="text-sm text-emerald-700 font-medium">View giving statements per member</p>
              <Link href="/members"
                className="flex items-center gap-1.5 bg-emerald-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-emerald-700 transition-colors">
                Go to Members <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          )}
        </div>

        {/* Record Giving Modal */}
        {showForm && (
          <div className="fixed inset-0 z-50 bg-black/60 flex items-end md:items-center justify-center p-0 md:p-4">
            <div className="bg-white w-full md:max-w-lg md:rounded-2xl rounded-t-3xl p-6 max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-5">
                <div>
                  <h2 className="text-base font-bold text-gray-800">Record Giving</h2>
                  <p className="text-xs text-gray-400 mt-0.5">GL entry fires automatically on save</p>
                </div>
                <button onClick={() => setShowForm(false)}
                  className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200">
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
              <form ref={formRef} onSubmit={handleSave}>
                <div className="mb-4 relative">
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">Member *</label>
                  <input type="text" value={search} onChange={e => searchMembers(e.target.value)}
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                    placeholder="Search by name or phone" autoComplete="off" />
                  {showDropdown && filteredMembers.length > 0 && (
                    <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-xl shadow-lg z-10 mt-1 overflow-hidden">
                      {filteredMembers.map((m: any) => (
                        <button key={m.id} type="button" onClick={() => pickMember(m)}
                          className="w-full text-left px-3 py-2.5 text-sm hover:bg-indigo-50 flex items-center gap-3 transition-colors">
                          <span className="w-7 h-7 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-xs shrink-0">
                            {m.first_name?.[0]}
                          </span>
                          <div>
                            <p className="font-semibold text-gray-800">{m.first_name} {m.last_name}</p>
                            <p className="text-xs text-gray-400">{m.phone}</p>
                          </div>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">Category *</label>
                  <select name="category_id" required
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50">
                    <option value="">Select category</option>
                    {categories.map((c: any) => <option key={c.id} value={c.id}>{c.name}</option>)}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1.5">Amount (KES) *</label>
                    <input name="amount_kes" type="number" required min="1"
                      className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                      placeholder="0" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1.5">Payment Method *</label>
                    <select name="payment_method" required
                      className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50">
                      <option value="mpesa">M-Pesa</option>
                      <option value="cash">Cash</option>
                      <option value="cheque">Cheque</option>
                    </select>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1.5">M-Pesa Ref</label>
                    <input name="mpesa_ref" type="text"
                      className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                      placeholder="e.g. QAB123XYZ" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1.5">Envelope No.</label>
                    <input name="envelope_number" type="text"
                      className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                      placeholder="Optional" />
                  </div>
                </div>
                <div className="mb-5">
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">Notes</label>
                  <input name="notes" type="text"
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                    placeholder="Optional" />
                </div>
                {msg && <p className="text-red-600 text-sm mb-3">{msg}</p>}
                <button type="submit" disabled={saving}
                  className="w-full py-3 rounded-xl text-white font-semibold text-sm bg-indigo-600 hover:bg-indigo-700 transition-all disabled:opacity-50 active:scale-[0.98]">
                  {saving ? 'Saving...' : 'Save Giving Record →'}
                </button>
              </form>
            </div>
          </div>
        )}

        {showExport && <div className="fixed inset-0 z-40" onClick={() => setShowExport(false)} />}
      </main>
    </div>
  )
}
