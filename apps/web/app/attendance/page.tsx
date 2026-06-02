"use client";
import { useEffect, useState, useRef } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import Link from "next/link";
import { Plus, ChevronRight, Download, Calendar } from "lucide-react";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";
const BRANCH_ID = "00000000-0000-0000-0000-000000000002";

export default function AttendancePage() {
  const [sessions, setSessions] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const formRef = useRef(null);

  const load = () => {
    setLoading(true);
    api.get("/attendance/sessions/?church_id=" + CHURCH_ID)
      .then(r => setSessions(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const n = (v) => Number(v) || 0;

  const save = async () => {
    const form = formRef.current;
    if (!form) return;
    const d = Object.fromEntries(new FormData(form));
    if (!d.session_date) return alert("Session date is required");
    setSaving(true);
    try {
      await api.post("/attendance/sessions/", {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        session_date: d.session_date,
        session_type: d.session_type,
        service_name: d.service_name || "",
        adult_count: n(d.adult_count), child_count: n(d.child_count),
        total_count: n(d.adult_count) + n(d.child_count),
        male_count: n(d.male_count), female_count: n(d.female_count),
        first_time_visitors: n(d.first_time_visitors), salvations: n(d.salvations),
        cars_count: n(d.cars_count), motorbikes_count: n(d.motorbikes_count),
        total_offering_kes: n(d.total_offering_kes),
        total_tithe_kes: n(d.total_tithe_kes),
        project_offering_kes: n(d.project_offering_kes),
        notes: d.notes || ""
      });
      setShowForm(false);
      load();
    } catch(e) {
      alert("Error saving: " + (e.response?.data?.detail || e.message));
    } finally { setSaving(false); }
  };

  const exportCSV = () => {
    const headers = ["Date","Service","Adults","Children","Total","Male","Female","First Timers","Salvations","Cars","Motorbikes","Offering(KES)","Tithe(KES)","Project(KES)"];
    const rows = sessions.map(s => [s.session_date, s.service_name||s.session_type, s.adult_count, s.child_count, s.total_count, s.male_count, s.female_count, s.first_time_visitors, s.salvations, s.cars_count, s.motorbikes_count, s.total_offering_kes, s.total_tithe_kes, s.project_offering_kes]);
    const csv = [headers, ...rows].map(r => r.join(",")).join("\n");
    const a = document.createElement("a");
    a.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
    a.download = "attendance_report.csv"; a.click();
  };

  const NF = ({label, name}) => (
    <div>
      <label className="text-xs text-gray-500 mb-1 block">{label}</label>
      <input type="number" min="0" name={name} placeholder="0"
        className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
    </div>
  );

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="flex items-center gap-2 mb-1">
          <Link href="/" className="text-indigo-500 text-sm hover:underline">← Dashboard</Link>
          <span className="text-gray-300">/</span>
          <span className="text-sm text-gray-600">Attendance</span>
        </div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Attendance</h1>
            <p className="text-gray-500 text-sm">{sessions.length} sessions recorded</p>
          </div>
          <div className="flex gap-2">
            <button onClick={exportCSV} className="flex items-center gap-2 border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50">
              <Download className="w-4 h-4" /> Export CSV
            </button>
            <button onClick={() => setShowForm(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
              <Plus className="w-4 h-4" /> New Session
            </button>
          </div>
        </div>

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl max-h-screen overflow-y-auto">
              <h2 className="text-lg font-bold text-gray-800 mb-1">New Attendance Session</h2>
              <p className="text-xs text-gray-400 mb-5">Sunday Report — fill all fields for complete records</p>
              <form ref={formRef}>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Date</label>
                    <input type="date" name="session_date" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Session Type</label>
                    <select name="session_type" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none">
                      <option value="sunday_service">Sunday Service</option>
                      <option value="midweek">Midweek Service</option>
                      <option value="special">Special Service</option>
                    </select>
                  </div>
                  <div className="col-span-2">
                    <label className="text-xs text-gray-500 mb-1 block">Service Name</label>
                    <input type="text" name="service_name" placeholder="e.g. Sunday 1st Service"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                </div>

                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Head Count</p>
                <div className="grid grid-cols-3 gap-4 mb-4">
                  <NF label="Adults" name="adult_count" />
                  <NF label="Children" name="child_count" />
                  <NF label="Male" name="male_count" />
                  <NF label="Female" name="female_count" />
                  <NF label="First Time Visitors" name="first_time_visitors" />
                  <NF label="Salvations" name="salvations" />
                </div>

                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Transport</p>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <NF label="Cars" name="cars_count" />
                  <NF label="Motorbikes" name="motorbikes_count" />
                </div>

                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Financials (KES)</p>
                <div className="grid grid-cols-3 gap-4 mb-4">
                  <NF label="Total Offering" name="total_offering_kes" />
                  <NF label="Total Tithe" name="total_tithe_kes" />
                  <NF label="Project Offering" name="project_offering_kes" />
                </div>

                <div className="mb-5">
                  <label className="text-xs text-gray-500 mb-1 block">Notes</label>
                  <textarea name="notes" rows={2} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                </div>
              </form>

              <div className="flex gap-3">
                <button onClick={() => setShowForm(false)} className="flex-1 border border-gray-200 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
                <button onClick={save} disabled={saving} className="flex-1 bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? "Saving..." : "Save Session →"}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {loading ? <p className="p-6 text-gray-400 text-sm">Loading...</p> : sessions.length === 0 ? (
            <div className="p-12 text-center">
              <Calendar className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400 mb-3">No sessions recorded yet</p>
              <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-medium">+ Record First Session</button>
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {["Date","Service","Attendance","First Timers","Salvations","Offering (KES)","Tithe (KES)",""].map(h => (
                    <th key={h} className="text-left text-xs text-gray-500 font-medium px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sessions.map(s => (
                  <tr key={s.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm font-medium text-gray-800">{s.session_date}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{s.service_name || s.session_type}</td>
                    <td className="px-4 py-3 text-sm text-gray-800 font-semibold">{s.total_count} <span className="text-xs text-gray-400">({s.adult_count}A / {s.child_count}C)</span></td>
                    <td className="px-4 py-3 text-sm text-orange-600 font-medium">{s.first_time_visitors}</td>
                    <td className="px-4 py-3 text-sm text-green-600 font-medium">{s.salvations}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">KES {s.total_offering_kes.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">KES {s.total_tithe_kes.toLocaleString()}</td>
                    <td className="px-4 py-3">
                      <Link href={"/giving?session_id=" + s.id} className="flex items-center gap-1 text-indigo-600 text-xs font-medium hover:underline whitespace-nowrap">
                        → Record Giving <ChevronRight className="w-3 h-3" />
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
