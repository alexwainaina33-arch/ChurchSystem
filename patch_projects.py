import os
os.makedirs('/app/frontend', exist_ok=True)
txt = '''"use client";
import { useEffect, useState, useRef } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import Link from "next/link";
import { Plus, FolderOpen } from "lucide-react";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";
const BRANCH_ID = "00000000-0000-0000-0000-000000000002";

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const formRef = useRef(null);

  const load = () => {
    setLoading(true);
    api.get("/projects/?church_id=" + CHURCH_ID)
      .then(r => setProjects(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const save = async () => {
    const form = formRef.current;
    if (!form) return;
    const d = Object.fromEntries(new FormData(form));
    if (!d.name) return alert("Project name is required");
    if (!d.target_amount_kes || Number(d.target_amount_kes) <= 0) return alert("Enter a target amount");
    setSaving(true);
    try {
      await api.post("/projects/", {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        name: d.name, description: d.description || "",
        target_amount_kes: Number(d.target_amount_kes),
        start_date: d.start_date || null,
        end_date: d.end_date || null
      });
      setShowForm(false); form.reset(); load();
    } catch(e) {
      alert("Error: " + (e.response?.data?.detail || e.message));
    } finally { setSaving(false); }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="flex items-center gap-2 mb-1">
          <Link href="/" className="text-indigo-500 text-sm hover:underline">Back to Dashboard</Link>
          <span className="text-gray-300">/</span>
          <span className="text-sm text-gray-600">Projects</span>
        </div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Projects</h1>
            <p className="text-gray-500 text-sm">{projects.length} projects</p>
          </div>
          <button onClick={() => setShowForm(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
            <Plus className="w-4 h-4" /> New Project
          </button>
        </div>

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-lg">
              <h2 className="text-lg font-bold text-gray-800 mb-4">New Project</h2>
              <form ref={formRef}>
                <div className="space-y-4">
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Project Name</label>
                    <input type="text" name="name" placeholder="e.g. Building Fund"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Description</label>
                    <textarea name="description" rows={2} placeholder="What is this project for?"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Target Amount (KES)</label>
                    <input type="number" name="target_amount_kes" min="1" placeholder="0"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">Start Date</label>
                      <input type="date" name="start_date"
                        className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">End Date</label>
                      <input type="date" name="end_date"
                        className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                    </div>
                  </div>
                </div>
              </form>
              <div className="flex gap-3 mt-6">
                <button onClick={() => setShowForm(false)} className="flex-1 border border-gray-200 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
                <button onClick={save} disabled={saving} className="flex-1 bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? "Saving..." : "Create Project"}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-4">
          {loading ? <p className="text-gray-400 text-sm">Loading...</p> : projects.length === 0 ? (
            <div className="bg-white rounded-xl shadow-sm p-12 text-center">
              <FolderOpen className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400 mb-3">No projects yet</p>
              <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-medium">+ Create First Project</button>
            </div>
          ) : projects.map(function(p) {
            var pct = Math.min(p.progress_percent || 0, 100);
            return (
              <div key={p.id} className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-gray-800 text-lg">{p.name}</h3>
                    {p.description && <p className="text-sm text-gray-500 mt-0.5">{p.description}</p>}
                  </div>
                  <span className="text-xs px-2 py-1 rounded-full font-medium bg-green-100 text-green-700">{p.status}</span>
                </div>
                <div className="flex items-center gap-6 mb-3 text-sm">
                  <span className="text-gray-500">Target: <span className="font-semibold text-gray-800">KES {p.target_amount_kes.toLocaleString()}</span></span>
                  <span className="text-gray-500">Collected: <span className="font-semibold text-green-600">KES {p.collected_amount_kes.toLocaleString()}</span></span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-3 mb-1">
                  <div className="bg-indigo-500 h-3 rounded-full" style={{width: pct + "%"}} />
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-gray-400">{pct}% funded</span>
                  <Link href="/giving" className="text-xs text-indigo-600 hover:underline">Record Contribution</Link>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}
'''
open('/app/frontend/projects.tsx', 'w').write(txt)
print('done')
