'use client'
import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Sidebar from '@/components/Sidebar'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1'
const CID = '00000000-0000-0000-0000-000000000001'
const BID = '00000000-0000-0000-0000-000000000002'

export default function GivingPage() {
  const router = useRouter()
  const [records, setRecords] = useState<any[]>([])
  const [categories, setCategories] = useState<any[]>([])
  const [members, setMembers] = useState<any[]>([])
  const [filteredMembers, setFilteredMembers] = useState<any[]>([])
  const [showDropdown, setShowDropdown] = useState(false)
  const [selectedMember, setSelectedMember] = useState<any>(null)
  const [search, setSearch] = useState('')
  const [summary, setSummary] = useState<any>({})
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState('')
  const formRef = useRef<HTMLFormElement>(null)

  useEffect(() => { load() }, [])

  async function load() {
    try {
      const [r, c, m, s] = await Promise.all([
        fetch(`${API}/giving/records/?church_id=${CID}`).then(x => x.json()),
        fetch(`${API}/giving/categories/?church_id=${CID}`).then(x => x.json()),
        fetch(`${API}/members/?church_id=${CID}&limit=200`).then(x => x.json()),
        fetch(`${API}/giving/summary/?church_id=${CID}`).then(x => x.json()),
      ])
      setRecords(Array.isArray(r) ? r : [])
      setCategories(Array.isArray(c) ? c : [])
      setMembers(Array.isArray(m) ? m : [])
      setSummary(s || {})
    } catch(e: any) { console.error(e) }
  }

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
      church_id: CID,
      branch_id: BID,
      member_id: selectedMember.id,
      category_id: fd.get('category_id'),
      amount_kes: Number(fd.get('amount_kes')),
      payment_method: fd.get('payment_method'),
      mpesa_ref: fd.get('mpesa_ref') || null,
      envelope_number: fd.get('envelope_number') || null,
      notes: fd.get('notes') || null,
    }
    try {
      const res = await fetch(`${API}/giving/records/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) { const d = await res.json(); setMsg(d.detail || 'Error'); setSaving(false); return }
      setMsg('Saved!')
      setShowForm(false)
      setSelectedMember(null)
      setSearch('')
      formRef.current?.reset()
      load()
    } catch(e: any) { setMsg('Cannot connect to server') }
    setSaving(false)
  }

  const fmt = (n: number) => 'KES ' + (n || 0).toLocaleString()

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-5xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Giving</h1>
              <p className="text-gray-500 text-sm mt-0.5">Record and track member giving</p>
            </div>
            <button onClick={() => setShowForm(true)}
              className="px-4 py-2 rounded-xl text-white text-sm font-semibold shadow"
              style={{background:'linear-gradient(135deg,#4f46e5,#7c3aed)'}}>
              + Record Giving
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {[
              { label: 'Tithe', key: 'TITHE', color: '#4f46e5' },
              { label: 'Offering', key: 'OFFERING', color: '#0ea5e9' },
              { label: 'Project', key: 'PROJECT', color: '#f59e0b' },
              { label: 'Total', key: 'TOTAL', color: '#10b981' },
            ].map(({ label, key, color }) => (
              <div key={key} className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
                <p className="text-xs text-gray-500 mb-1">{label}</p>
                <p className="text-lg font-bold" style={{color}}>{fmt(summary[key] || summary.total || 0)}</p>
              </div>
            ))}
          </div>

          {msg && <div className="mb-4 px-4 py-3 rounded-xl bg-green-50 border border-green-200 text-green-700 text-sm">{msg}</div>}

          {showForm && (
            <div className="fixed inset-0 z-50 bg-black/60 flex items-end md:items-center justify-center p-0 md:p-4">
              <div className="bg-white w-full md:max-w-lg md:rounded-2xl rounded-t-2xl p-6 max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-base font-semibold text-gray-800">Record Giving</h2>
                  <button onClick={() => setShowForm(false)} className="text-gray-400 hover:text-gray-600 text-xl">x</button>
                </div>
                <form ref={formRef} onSubmit={handleSave}>
                  <div className="mb-4 relative">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Member</label>
                    <input
                      type="text" value={search}
                      onChange={e => searchMembers(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="Search member by name or phone" autoComplete="off" />
                    {showDropdown && filteredMembers.length > 0 && (
                      <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-lg z-10 mt-1">
                        {filteredMembers.map((m: any) => (
                          <button key={m.id} type="button" onClick={() => pickMember(m)}
                            className="w-full text-left px-3 py-2 text-sm hover:bg-purple-50 flex items-center gap-2">
                            <span className="w-7 h-7 rounded-full bg-purple-100 flex items-center justify-center text-purple-700 font-bold text-xs">
                              {m.first_name?.[0]}
                            </span>
                            <div>
                              <p className="font-medium text-gray-800">{m.first_name} {m.last_name}</p>
                              <p className="text-xs text-gray-400">{m.phone}</p>
                            </div>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                    <select name="category_id" required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500">
                      <option value="">Select category</option>
                      {categories.map((c: any) => <option key={c.id} value={c.id}>{c.name}</option>)}
                    </select>
                  </div>
                  <div className="grid grid-cols-2 gap-3 mb-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Amount (KES)</label>
                      <input name="amount_kes" type="number" required min="1"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="0" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
                      <select name="payment_method" required
                        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500">
                        <option value="mpesa">M-Pesa</option>
                        <option value="cash">Cash</option>
                        <option value="cheque">Cheque</option>
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3 mb-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">M-Pesa Ref</label>
                      <input name="mpesa_ref" type="text"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="e.g. QAB123XYZ" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Envelope No.</label>
                      <input name="envelope_number" type="text"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Optional" />
                    </div>
                  </div>
                  <div className="mb-5">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                    <input name="notes" type="text"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="Optional" />
                  </div>
                  {msg && <p className="text-red-600 text-sm mb-3">{msg}</p>}
                  <button type="submit" disabled={saving}
                    className="w-full py-3 rounded-xl text-white font-semibold text-sm"
                    style={{background: saving ? '#9ca3af' : 'linear-gradient(135deg,#4f46e5,#7c3aed)'}}>
                    {saving ? 'Saving...' : 'Save Giving Record'}
                  </button>
                </form>
              </div>
            </div>
          )}

          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100">
              <h2 className="text-sm font-semibold text-gray-700">Recent Giving Records</h2>
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
                  {records.length === 0 && (
                    <tr><td colSpan={6} className="text-center py-12 text-gray-400">No giving records yet — record the first one above</td></tr>
                  )}
                  {records.map((r: any) => (
                    <tr key={r.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 font-medium text-gray-800">
                        {r.member_name || (r.member ? r.member.first_name + ' ' + r.member.last_name : 'Unknown')}
                      </td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-700">
                          {r.category_name || r.category?.name || 'N/A'}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-semibold text-gray-800">{fmt(r.amount_kes)}</td>
                      <td className="px-4 py-3 text-gray-500 capitalize">{r.payment_method}</td>
                      <td className="px-4 py-3 text-gray-400 text-xs">{r.created_at?.slice(0,10)}</td>
                      <td className="px-4 py-3">
                        <button onClick={() => router.push('/members/' + r.member_id)}
                          className="text-xs text-purple-600 hover:underline font-medium">
                          View Member
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
