"use client";
import { useEffect, useState, useRef } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import Link from "next/link";
import { Plus, Download, DollarSign } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";
const BRANCH_ID = "00000000-0000-0000-0000-000000000002";

function GivingContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const [records, setRecords] = useState([]);
  const [members, setMembers] = useState([]);
  const [categories, setCategories] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [search, setSearch] = useState("");
  const [filteredMembers, setFilteredMembers] = useState([]);
  const [selectedMember, setSelectedMember] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const formRef = useRef(null);

  const load = () => {
    setLoading(true);
    api.get("/giving/records/?church_id=" + CHURCH_ID)
      .then(r => setRecords(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    api.get("/members/?church_id=" + CHURCH_ID).then(r => setMembers(r.data));
    api.get("/giving/categories/?church_id=" + CHURCH_ID).then(r => setCategories(r.data));
    if (sessionId) setShowForm(true);
  }, []);

  useEffect(() => {
    if (search.length < 1) { setFilteredMembers([]); return; }
    setFilteredMembers(members.filter(m =>
      (m.first_name + " " + m.last_name).toLowerCase().includes(search.toLowerCase()) ||
      (m.phone || "").includes(search)
    ).slice(0, 6));
    setShowDropdown(true);
  }, [search, members]);

  const save = async () => {
    const form = formRef.current;
    if (!form) return;
    const d = Object.fromEntries(new FormData(form));
    if (!d.category_id) return alert("Select a giving category");
    if (!d.amount_kes || Number(d.amount_kes) <= 0) return alert("Enter a valid amount");
    setSaving(true);
    try {
      await api.post("/giving/records/", {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        member_id: selectedMember ? selectedMember.id : null,
        session_id: sessionId || null,
        category_id: d.category_id,
        amount_kes: Number(d.amount_kes),
        payment_method: d.payment_method,
        mpesa_ref: d.mpesa_ref || null,
        envelope_number: d.envelope_number || null,
        notes: d.notes || null
      });
      setShowForm(false);
      setSelectedMember(null);
      setSearch("");
      form.reset();
      load();
    } catch(e) {
      alert("Error: " + (e.response?.data?.detail || e.message));
    } finally { setSaving(false); }
  };

  const exportCSV = () => {
    const headers = ["Date","Member","Category","Amount(KES)","Method","M-Pesa Ref"];
    const rows = records.map(r => [r.created_at?.slice(0,10), r.member_name||"Anonymous", r.category_name, r.amount_kes, r.payment_method, r.mpesa_ref||""]);
    const csv = [headers, ...rows].map(r => r.join(",")).join("\n");
    const a = document.createElement("a");
    a.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
    a.download = "giving_records.csv"; a.click();
  };

  const total = records.reduce((s, r) => s + r.amount_kes, 0);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="flex items-center gap-2 mb-1">
          <Link href="/attendance" className="text-indigo-500 text-sm hover:underline">← Attendance</Link>
          <span className="text-gray-300">/</span>
          <span className="text-sm text-gray-600">Giving</span>
        </div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Giving Records</h1>
            <p className="text-gray-500 text-sm">{records.length} records · Total: <span className="font-semibold text-green-600">KES {total.toLocaleString()}</span></p>
          </div>
          <div className="flex gap-2">
            <button onClick={exportCSV} className="flex items-center gap-2 border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50">
              <Download className="w-4 h-4" /> Export CSV
            </button>
            <button onClick={() => setShowForm(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
              <Plus className="w-4 h-4" /> Record Giving
            </button>
          </div>
        </div>

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-lg max-h-screen overflow-y-auto">
              <h2 className="text-lg font-bold text-gray-800 mb-1">Record Giving</h2>
              {sessionId && <p className="text-xs text-indigo-500 mb-4">Linked to today's session</p>}
              <form ref={formRef}>
                <div className="mb-4 relative">
                  <label className="text-xs text-gray-500 mb-1 block">Member (leave blank for anonymous)</label>
                  <input type="text" placeholder="Search by name or phone..."
                    value={selectedMember ? selectedMember.first_name + " " + selectedMember.last_name : search}
                    onChange={e => { setSearch(e.target.value); setSelectedMember(null); }}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  {showDropdown && filteredMembers.length > 0 && !selectedMember && (
                    <div className="absolute z-10 w-full bg-white border border-gray-200 rounded-lg shadow-lg mt-1">
                      {filteredMembers.map(m => (
                        <div key={m.id} onClick={() => { setSelectedMember(m); setSearch(""); setShowDropdown(false); }}
                          className="px-4 py-2 text-sm hover:bg-indigo-50 cursor-pointer">
                          {m.first_name} {m.last_name} · {m.phone || "no phone"}
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="col-span-2">
                    <label className="text-xs text-gray-500 mb-1 block">Category</label>
                    <select name="category_id" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none">
                      <option value="">-- Select Category --</option>
                      {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                    </select>
                  </div>
                  <div className="col-span-2">
                    <label className="text-xs text-gray-500 mb-1 block">Amount (KES)</label>
                    <input type="number" name="amount_kes" min="1" placeholder="0"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Payment Method</label>
                    <select name="payment_method" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none">
                      <option value="cash">Cash</option>
                      <option value="mpesa">M-Pesa</option>
                      <option value="bank_transfer">Bank Transfer</option>
                      <option value="cheque">Cheque</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">M-Pesa Ref</label>
                    <input type="text" name="mpesa_ref" placeholder="e.g. QK8X9Y"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Envelope No.</label>
                    <input type="text" name="envelope_number" placeholder="Optional"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Notes</label>
                    <input type="text" name="notes" placeholder="Optional"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                </div>
              </form>
              <div className="flex gap-3">
                <button onClick={() => { setShowForm(false); setSelectedMember(null); setSearch(""); }}
                  className="flex-1 border border-gray-200 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
                <button onClick={save} disabled={saving}
                  className="flex-1 bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? "Saving..." : "Save & Post GL →"}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {loading ? <p className="p-6 text-gray-400 text-sm">Loading...</p> : records.length === 0 ? (
            <div className="p-12 text-center">
              <DollarSign className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400 mb-3">No giving records yet</p>
              <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-medium">+ Record First Giving</button>
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {["Date","Member","Category","Amount (KES)","Method","M-Pesa Ref","→ Member"].map(h => (
                    <th key={h} className="text-left text-xs text-gray-500 font-medium px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {records.map(r => (
                  <tr key={r.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-600">{r.created_at?.slice(0,10)}</td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-800">{r.member_name || <span className="text-gray-400 italic">Anonymous</span>}</td>
                    <td className="px-4 py-3"><span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{r.category_name}</span></td>
                    <td className="px-4 py-3 text-sm font-bold text-green-600">KES {r.amount_kes.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-gray-500 capitalize">{r.payment_method}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">{r.mpesa_ref || "—"}</td>
                    <td className="px-4 py-3">
                      {r.member_id && <Link href={"/members/" + r.member_id} className="text-indigo-600 text-xs hover:underline">View Member →</Link>}
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

export default function GivingPage() {
  return <Suspense fallback={<div className="p-8 text-gray-400">Loading...</div>}><GivingContent /></Suspense>;
}
