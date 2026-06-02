"use client";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import { UserPlus, Search, ChevronRight } from "lucide-react";
import Link from "next/link";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";
const BRANCH_ID = "00000000-0000-0000-0000-000000000002";

export default function MembersPage() {
  const [members, setMembers] = useState([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ first_name:"", last_name:"", phone:"", email:"", gender:"male", marital_status:"single", membership_status:"active", occupation:"" });

  const load = () => {
    setLoading(true);
    api.get("/members/?church_id=" + CHURCH_ID + (search ? "&search=" + search : ""))
      .then(r => setMembers(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [search]);

  const save = async () => {
    if (!form.first_name || !form.last_name) return alert("First and last name required");
    setSaving(true);
    try {
      await api.post("/members/", { ...form, church_id: CHURCH_ID, branch_id: BRANCH_ID });
      setShowForm(false);
      setForm({ first_name:"", last_name:"", phone:"", email:"", gender:"male", marital_status:"single", membership_status:"active", occupation:"" });
      load();
    } finally { setSaving(false); }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Members</h1>
            <p className="text-gray-500 text-sm">{members.length} registered members</p>
          </div>
          <button onClick={() => setShowForm(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
            <UserPlus className="w-4 h-4" /> Register Member
          </button>
        </div>

        <div className="relative mb-4">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
          <input className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
            placeholder="Search by name or phone..." value={search} onChange={e => setSearch(e.target.value)} />
        </div>

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-lg">
              <h2 className="text-lg font-bold text-gray-800 mb-4">Register New Member</h2>
              <div className="grid grid-cols-2 gap-4">
                {[["first_name","First Name"],["last_name","Last Name"],["phone","Phone"],["email","Email"],["occupation","Occupation"]].map(([k,l]) => (
                  <div key={k} className={k === "occupation" ? "col-span-2" : ""}>
                    <label className="text-xs text-gray-500 mb-1 block">{l}</label>
                    <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                      value={form[k]} onChange={e => setForm({...form, [k]: e.target.value})} />
                  </div>
                ))}
                <div>
                  <label className="text-xs text-gray-500 mb-1 block">Gender</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none"
                    value={form.gender} onChange={e => setForm({...form, gender: e.target.value})}>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs text-gray-500 mb-1 block">Marital Status</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none"
                    value={form.marital_status} onChange={e => setForm({...form, marital_status: e.target.value})}>
                    <option value="single">Single</option>
                    <option value="married">Married</option>
                    <option value="widowed">Widowed</option>
                    <option value="divorced">Divorced</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs text-gray-500 mb-1 block">Status</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none"
                    value={form.membership_status} onChange={e => setForm({...form, membership_status: e.target.value})}>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="visitor">Visitor</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button onClick={() => setShowForm(false)} className="flex-1 border border-gray-200 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
                <button onClick={save} disabled={saving} className="flex-1 bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? "Saving..." : "Save Member"}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {loading ? <p className="p-6 text-gray-400 text-sm">Loading...</p> : members.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-400 mb-3">No members yet</p>
              <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-medium">+ Register First Member</button>
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {["Name","Phone","Gender","Status","Branch",""].map(h => (
                    <th key={h} className="text-left text-xs text-gray-500 font-medium px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {members.map(m => (
                  <tr key={m.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm font-medium text-gray-800">{m.first_name} {m.last_name}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">{m.phone || "—"}</td>
                    <td className="px-4 py-3 text-sm text-gray-500 capitalize">{m.gender || "—"}</td>
                    <td className="px-4 py-3"><span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full capitalize">{m.membership_status}</span></td>
                    <td className="px-4 py-3 text-sm text-gray-500">Nairobi Main</td>
                    <td className="px-4 py-3">
                      <Link href={"/members/" + m.id} className="flex items-center gap-1 text-indigo-600 text-xs font-medium hover:underline">
                        View <ChevronRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>
    </div>
  );
}
