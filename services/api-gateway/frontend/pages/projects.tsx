'use client'
import { useEffect, useState, useRef } from 'react'
import Sidebar from '../../components/Sidebar'
import api from '../../lib/api'
import Link from 'next/link'
import { Plus, FolderOpen, ChevronRight, X, Target, TrendingUp } from 'lucide-react'

const CHURCH_ID = '00000000-0000-0000-0000-000000000001'
const BRANCH_ID = '00000000-0000-0000-0000-000000000002'

const STATUS_COLORS: Record<string,string> = {
  active:    'bg-emerald-50 text-emerald-700 border-emerald-200',
  completed: 'bg-indigo-50 text-indigo-700 border-indigo-200',
  paused:    'bg-amber-50 text-amber-700 border-amber-200',
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading]   = useState(true)
  const [saving, setSaving]     = useState(false)
  const formRef = useRef<HTMLFormElement>(null)

  const load = () => {
    setLoading(true)
    api.get('/projects/?church_id=' + CHURCH_ID)
      .then(r => setProjects(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const save = async () => {
    const form = formRef.current
    if (!form) return
    const d: any = Object.fromEntries(new FormData(form))
    if (!d.name) return alert('Project name is required')
    if (!d.target_amount_kes || Number(d.target_amount_kes) <= 0) return alert('Enter a target amount')
    setSaving(true)
    try {
      await api.post('/projects/', {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        name: d.name, description: d.description || '',
        target_amount_kes: Number(d.target_amount_kes),
        start_date: d.start_date || null,
        end_date: d.end_date || null
      })
      setShowForm(false); form.reset(); load()
    } catch(e: any) {
      alert('Error: ' + (e.response?.data?.detail || e.message))
    } finally { setSaving(false) }
  }

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
                <span className="text-gray-600 font-medium">Projects</span>
              </div>
              <h1 className="text-gray-900 font-bold text-lg leading-tight">
                Projects
                <span className="ml-2 text-sm font-normal text-gray-400">{projects.length} total</span>
              </h1>
            </div>
            <button onClick={() => setShowForm(true)}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700
                         text-white px-3 md:px-4 py-2 rounded-xl text-sm font-semibold
                         shadow-sm shadow-indigo-200 transition-all active:scale-95">
              <Plus className="w-4 h-4" />
              <span className="hidden sm:inline">New Project</span>
              <span className="sm:hidden">New</span>
            </button>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-7xl mx-auto">
          {loading ? (
            <div className="flex items-center justify-center py-32 gap-3">
              <div className="w-7 h-7 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
              <span className="text-gray-400 text-sm">Loading projects...</span>
            </div>
          ) : projects.length === 0 ? (
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm py-20 text-center">
              <FolderOpen className="w-10 h-10 text-gray-200 mx-auto mb-3" />
              <p className="text-gray-400 text-sm mb-3">No projects yet</p>
              <button onClick={() => setShowForm(true)}
                className="text-indigo-600 text-sm font-semibold hover:text-indigo-800">
                + Create First Project
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {projects.map((p: any) => {
                const pct = Math.min(p.progress_percent || 0, 100)
                const remaining = p.target_amount_kes - p.collected_amount_kes
                return (
                  <div key={p.id}
                    className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 md:p-6
                               hover:shadow-md hover:border-indigo-100 transition-all duration-200">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <div className="w-8 h-8 rounded-xl bg-indigo-50 flex items-center justify-center shrink-0">
                            <FolderOpen className="w-4 h-4 text-indigo-600" />
                          </div>
                          <h3 className="font-bold text-gray-900 text-base truncate">{p.name}</h3>
                        </div>
                        {p.description && (
                          <p className="text-sm text-gray-500 ml-10 line-clamp-2">{p.description}</p>
                        )}
                      </div>
                      <span className={`shrink-0 ml-3 text-xs px-2.5 py-1 rounded-full border font-semibold capitalize
                        ${STATUS_COLORS[p.status] || STATUS_COLORS.active}`}>
                        {p.status}
                      </span>
                    </div>

                    {/* Progress bar */}
                    <div className="mb-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-500 font-medium">{pct}% funded</span>
                        <span className="text-xs text-gray-400">
                          KES {remaining > 0 ? remaining.toLocaleString() + ' remaining' : 'Goal reached!'}
                        </span>
                      </div>
                      <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-700
                            ${pct >= 100 ? 'bg-emerald-500' : 'bg-gradient-to-r from-indigo-500 to-purple-500'}`}
                          style={{ width: pct + '%' }}
                        />
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="flex items-center gap-4 mb-4">
                      <div className="flex items-center gap-1.5">
                        <Target className="w-3.5 h-3.5 text-gray-400" />
                        <div>
                          <p className="text-xs text-gray-400">Target</p>
                          <p className="text-sm font-bold text-gray-800">
                            KES {p.target_amount_kes.toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <TrendingUp className="w-3.5 h-3.5 text-emerald-500" />
                        <div>
                          <p className="text-xs text-gray-400">Collected</p>
                          <p className="text-sm font-bold text-emerald-600">
                            KES {p.collected_amount_kes.toLocaleString()}
                          </p>
                        </div>
                      </div>
                    </div>

                    <Link href="/giving"
                      className="flex items-center justify-center gap-2 w-full
                                 border border-indigo-200 text-indigo-600 hover:bg-indigo-50
                                 py-2.5 rounded-xl text-sm font-semibold transition-colors active:scale-[0.98]">
                      <Plus className="w-4 h-4" /> Record Contribution
                    </Link>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Modal */}
        {showForm && (
          <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center p-0 md:p-4">
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowForm(false)} />
            <div className="relative bg-white w-full md:max-w-lg rounded-t-3xl md:rounded-2xl
                            shadow-2xl max-h-[92vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4
                              flex items-center justify-between rounded-t-3xl md:rounded-t-2xl">
                <div>
                  <h2 className="text-base font-bold text-gray-900">New Project</h2>
                  <p className="text-xs text-gray-400 mt-0.5">Create a fundraising project</p>
                </div>
                <button onClick={() => setShowForm(false)}
                  className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100
                             hover:bg-gray-200 transition-colors">
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
              <div className="p-6">
                <form ref={formRef}>
                  <div className="space-y-4">
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Project Name *</label>
                      <input type="text" name="name" placeholder="e.g. Building Fund"
                        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                   focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Description</label>
                      <textarea name="description" rows={2} placeholder="What is this project for?"
                        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                   focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50 resize-none" />
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 font-medium mb-1.5 block">Target Amount (KES) *</label>
                      <input type="number" name="target_amount_kes" min="1" placeholder="500000"
                        className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                   focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-500 font-medium mb-1.5 block">Start Date</label>
                        <input type="date" name="start_date"
                          className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                     focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                      </div>
                      <div>
                        <label className="text-xs text-gray-500 font-medium mb-1.5 block">End Date</label>
                        <input type="date" name="end_date"
                          className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm
                                     focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-gray-50/50" />
                      </div>
                    </div>
                  </div>
                </form>
                <div className="flex gap-3 mt-6">
                  <button onClick={() => setShowForm(false)}
                    className="flex-1 border border-gray-200 text-gray-600 py-3 rounded-xl text-sm
                               font-medium hover:bg-gray-50 transition-colors">Cancel</button>
                  <button onClick={save} disabled={saving}
                    className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl
                               text-sm font-semibold shadow-sm shadow-indigo-200 transition-all
                               disabled:opacity-50 active:scale-[0.98]">
                    {saving ? 'Saving...' : 'Create Project →'}
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
