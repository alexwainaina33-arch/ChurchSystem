'use client'
import { useEffect, useState } from 'react'
import Sidebar from '../../components/Sidebar'
import api from '../../lib/api'
import { UserPlus, Search, ChevronRight, Users, X } from 'lucide-react'
import Link from 'next/link'

const CHURCH_ID = '00000000-0000-0000-0000-000000000001'
const BRANCH_ID = '00000000-0000-0000-0000-000000000002'

const STATUS_COLORS: Record<string,string> = {
  active:   'bg-emerald-50 text-emerald-700 border-emerald-200',
  inactive: 'bg-gray-100 text-gray-500 border-gray-200',
  visitor:  'bg-amber-50 text-amber-700 border-amber-200',
}

export default function MembersPage() {
  const [members, setMembers]   = useState<any[]>([])
  const [search, setSearch]     = useState('')
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading]   = useState(true)
  const [saving, setSaving]     = useState(false)
  const [form, setForm]         = useState({
    first_name:'', last_name:'', phone:'', email:'',
    gender:'male', marital_status:'single',
    membership_status:'active', occupation:''
  })

  const load = () => {
    setLoading(true)
    api.get('/members/?church_id=' + CHURCH_ID + (search ? '&search=' + search : ''))
      .then(r => setMembers(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [search])

  const save = async () => {
    if (!form.first_name || !form.last_name) return alert('First and last name required')
    setSaving(true)
    try {
      await api.post('/members/', { ...form, church_id: CHURCH_ID, branch_id: BRANCH_ID })
      setShowForm(false)
      setForm({ first_name:'', last_name:'', phone:'', email:'', gender:'male', marital_status:'single', membership_status:'active', occupation:'' })
      load()
    } finally { setSaving(false) }
  }

  const F = ({ k, l, span=false }: { k:string, l:string, span?:boolean }) => (
    <div className={span ? 'col-span-2' : ''}>
      <label className="text-xs text-gray-500 font-medium mb-1.5 block">{l}</label>
      <input className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                        focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400
                        bg-gray-50/50 transition-all"
        value={(form as any)[k]} onChange={e => setForm({...form, [k]: e.target.value})} />
    </div>
  )

  const S = ({ k, l, opts }: { k:string, l:string, opts:[string,string][] }) => (
    <div>
      <label className="text-xs text-gray-500 font-medium mb-1.5 block">{l}</label>
      <select className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                         focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50"
        value={(form as any)[k]} onChange={e => setForm({...form, [k]: e.target.value})}>
        {opts.map(([v,label]) => <option key={v} value={v}>{label}</option>)}
      </select>
    </div>
  )

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 min-w-0 pb-24 md:pb-0">

        {/* Header */}
        <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200
                           px-4 md:px-8 py-3.5 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="ml-12 md:ml-0">
              <div className="flex items-center gap-2 text-xs text-gray-400 mb-0.5">
                <Link href="/" className="hover:text-indigo-600 transition-colors">Dashboard</Link>
                <ChevronRight className="w-3 h-3" />
                <span className="text-gray-600 font-medium">Members</span>
              </div>
              <h1 className="text-gray-900 font-bold text-lg leading-tight">
                Members
                <span className="ml-2 text-sm font-normal text-gray-400">
                  {members.length} registered
                </span>
              </h1>
            </div>
            <button onClick={() => setShowForm(true)}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700
                         text-white px-3 md:px-4 py-2 rounded-xl text-sm font-semibold
                         shadow-sm shadow-indigo-200 transition-all active:scale-95">
              <UserPlus className="w-4 h-4" />
              <span className="hidden sm:inline">Register Member</span>
              <span className="sm:hidden">Register</span>
            </button>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-4">

          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-gray-400" />
            <input
              className="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm
                         focus:outline-none focus:ring-2 focus:ring-indigo-300 shadow-sm"
              placeholder="Search by name or phone..."
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>

          {/* Table */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            {loading ? (
              <div className="flex items-center justify-center py-20 gap-3">
                <div className="w-7 h-7 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
                <span className="text-gray-400 text-sm">Loading members...</span>
              </div>
            ) : members.length === 0 ? (
              <div className="py-20 text-center">
                <Users className="w-10 h-10 text-gray-200 mx-auto mb-3" />
                <p className="text-gray-400 text-sm mb-3">No members yet</p>
                <button onClick={() => setShowForm(true)}
                  className="text-indigo-600 text-sm font-semibold hover:text-indigo-800">
                  + Register First Member
                </button>
              </div>
            ) : (
              <div className="overflow-x-auto -webkit-overflow-scrolling-touch">
                <table className="w-full min-w-[600px]">
                  <thead className="bg-gray-50 border-b border-gray-100">
                    <tr>
                      {['Name','Phone','Gender','Status','Branch',''].map(h => (
                        <th key={h} className="text-left text-xs text-gray-500 font-semibold
                                               uppercase tracking-wide px-4 py-3">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {members.map((m: any) => (
                      <tr key={m.id} className="hover:bg-indigo-50/30 transition-colors group">
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2.5">
                            <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center
                                            text-xs font-bold text-indigo-600 shrink-0">
                              {m.first_name?.[0]}{m.last_name?.[0]}
                            </div>
                            <span className="text-sm font-semibold text-gray-800">
                              {m.first_name} {m.last_name}
                            </span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500">{m.phone || '—'}</td>
                        <td className="px-4 py-3 text-sm text-gray-500 capitalize">{m.gender || '—'}</td>
                        <td className="px-4 py-3">
                          <span className={`text-xs px-2.5 py-1 rounded-full border font-medium capitalize
                            ${STATUS_COLORS[m.membership_status] || STATUS_COLORS.inactive}`}>
                            {m.membership_status}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-400">Nairobi Main</td>
                        <td className="px-4 py-3">
                          <Link href={"/members/" + m.id}
                            className="flex items-center gap-1 text-indigo-600 text-xs font-semibold
                                       hover:text-indigo-800 opacity-0 group-hover:opacity-100
                                       transition-all whitespace-nowrap">
                            View <ChevronRight className="w-3 h-3" />
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

        {/* Modal */}
        {showForm && (
          <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center p-0 md:p-4">
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowForm(false)} />
            <div className="relative bg-white w-full md:max-w-lg rounded-t-3xl md:rounded-2xl
                            shadow-2xl max-h-[92vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between rounded-t-3xl md:rounded-t-2xl">
                <div>
                  <h2 className="text-base font-bold text-gray-900">Register New Member</h2>
                  <p className="text-xs text-gray-400 mt-0.5">All fields marked * are required</p>
                </div>
                <button onClick={() => setShowForm(false)}
                  className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100
                             hover:bg-gray-200 transition-colors">
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <F k="first_name" l="First Name *" />
                  <F k="last_name"  l="Last Name *" />
                  <F k="phone"      l="Phone" />
                  <F k="email"      l="Email" />
                  <F k="occupation" l="Occupation" span />
                  <S k="gender"           l="Gender"         opts={[['male','Male'],['female','Female']]} />
                  <S k="marital_status"   l="Marital Status" opts={[['single','Single'],['married','Married'],['widowed','Widowed'],['divorced','Divorced']]} />
                  <S k="membership_status" l="Status"        opts={[['active','Active'],['inactive','Inactive'],['visitor','Visitor']]} />
                </div>
                <div className="flex gap-3 mt-6">
                  <button onClick={() => setShowForm(false)}
                    className="flex-1 border border-gray-200 text-gray-600 py-3 rounded-xl text-sm
                               font-medium hover:bg-gray-50 transition-colors">
                    Cancel
                  </button>
                  <button onClick={save} disabled={saving}
                    className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl
                               text-sm font-semibold shadow-sm shadow-indigo-200 transition-all
                               disabled:opacity-50 active:scale-[0.98]">
                    {saving ? 'Saving...' : 'Save Member →'}
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
