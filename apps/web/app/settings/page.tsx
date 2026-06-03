"use client";
import { useEffect, useState, useRef } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import Link from "next/link";
import { Settings, GitBranch, Plus } from "lucide-react";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";

export default function SettingsPage() {
  const [church, setChurch] = useState<any>(null);
  const [branches, setBranches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showBranchForm, setShowBranchForm] = useState(false);
  const branchRef = useRef<HTMLFormElement>(null);

  const load = () => {
    Promise.all([
      api.get("/churches/" + CHURCH_ID),
      api.get("/branches/?church_id=" + CHURCH_ID)
    ]).then(([c, b]) => {
      setChurch(c.data);
      setBranches(b.data);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const saveChurch = async (e) => {
    const form = e.target.closest("form");
    const d = Object.fromEntries(new FormData(form));
    setSaving(true);
    try {
      await api.put("/churches/" + CHURCH_ID, d);
      alert("Church details saved!");
      load();
    } catch(err) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally { setSaving(false); }
  };

  const saveBranch = async () => {
    const form = branchRef.current;
    if (!form) return;
    const d = Object.fromEntries(new FormData(form));
    if (!d.name) return alert("Branch name required");
    setSaving(true);
    try {
      await api.post("/branches/", { ...d, church_id: CHURCH_ID });
      setShowBranchForm(false);
      form.reset();
      load();
    } catch(err) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally { setSaving(false); }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">
        <div className="flex items-center gap-2 mb-1">
          <Link href="/" className="text-indigo-500 text-sm hover:underline">Back to Dashboard</Link>
          <span className="text-gray-300">/</span>
          <span className="text-sm text-gray-600">Settings</span>
        </div>
        <div className="flex items-center gap-3 mb-6">
          <Settings className="w-6 h-6 text-gray-600" />
          <h1 className="text-2xl font-bold text-gray-800">Church Settings</h1>
        </div>

        {loading ? <p className="text-gray-400">Loading...</p> : (
          <>
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">Church Profile</h2>
              <form>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Church Name</label>
                    <input type="text" name="name" defaultValue={church?.name || ""}
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Denomination</label>
                    <input type="text" name="denomination" defaultValue={church?.denomination || ""}
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">City</label>
                    <input type="text" name="city" defaultValue={church?.city || ""}
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Phone</label>
                    <input type="text" name="phone" defaultValue={church?.phone || ""}
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Email</label>
                    <input type="text" name="email" defaultValue={church?.email || ""}
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Country</label>
                    <input type="text" name="country" defaultValue={church?.country || "Kenya"}
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                </div>
                <button type="button" onClick={saveChurch} disabled={saving}
                  className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? "Saving..." : "Save Church Details"}
                </button>
              </form>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <GitBranch className="w-4 h-4 text-gray-600" />
                  <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Branches ({branches.length})</h2>
                </div>
                <button onClick={() => setShowBranchForm(true)}
                  className="flex items-center gap-2 bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-medium hover:bg-indigo-700">
                  <Plus className="w-3 h-3" /> Add Branch
                </button>
              </div>

              {showBranchForm && (
                <div className="bg-indigo-50 rounded-lg p-4 mb-4">
                  <h3 className="text-sm font-semibold text-gray-700 mb-3">New Branch</h3>
                  <form ref={branchRef}>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Branch Name</label>
                        <input type="text" name="name" placeholder="e.g. Westlands Branch"
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                      </div>
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Pastor Name</label>
                        <input type="text" name="pastor_name" placeholder="e.g. Pastor Jane Wanjiku"
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                      </div>
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Phone</label>
                        <input type="text" name="phone" placeholder="07XXXXXXXX"
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                      </div>
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Address</label>
                        <input type="text" name="address" placeholder="e.g. Westlands, Nairobi"
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                      </div>
                    </div>
                    <div className="flex gap-2 mt-3">
                      <button type="button" onClick={() => setShowBranchForm(false)}
                        className="border border-gray-200 text-gray-600 px-4 py-1.5 rounded-lg text-xs hover:bg-gray-50">Cancel</button>
                      <button type="button" onClick={saveBranch} disabled={saving}
                        className="bg-indigo-600 text-white px-4 py-1.5 rounded-lg text-xs font-medium hover:bg-indigo-700 disabled:opacity-50">
                        {saving ? "Saving..." : "Create Branch"}
                      </button>
                    </div>
                  </form>
                </div>
              )}

              <div className="space-y-3">
                {branches.map(b => (
                  <div key={b.id} className="flex items-center justify-between border border-gray-100 rounded-lg p-4">
                    <div>
                      <p className="font-medium text-gray-800">{b.name}</p>
                      <p className="text-xs text-gray-500">Pastor: {b.pastor_name || "—"} · {b.phone || "No phone"} · {b.address || "No address"}</p>
                    </div>
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">Active</span>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
