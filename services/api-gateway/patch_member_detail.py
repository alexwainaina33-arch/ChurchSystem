import os
os.makedirs('/app/frontend', exist_ok=True)
txt = '''"use client";
import { useEffect, useState } from "react";
import Sidebar from "../../../components/Sidebar";
import api from "../../../lib/api";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, DollarSign } from "lucide-react";

export default function MemberDetailPage() {
  const params = useParams();
  const id = params.id;
  const [member, setMember] = useState(null);
  const [giving, setGiving] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    Promise.all([
      api.get("/members/" + id),
      api.get("/members/" + id + "/giving")
    ]).then(([mr, gr]) => {
      setMember(mr.data);
      setGiving(gr.data);
    }).finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="flex min-h-screen bg-gray-50"><Sidebar /><main className="flex-1 p-8 text-gray-400">Loading...</main></div>;
  if (!member) return <div className="flex min-h-screen bg-gray-50"><Sidebar /><main className="flex-1 p-8 text-gray-400">Member not found.</main></div>;

  const total = giving.reduce((s, r) => s + r.amount_kes, 0);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="flex items-center gap-2 mb-4">
          <Link href="/members" className="flex items-center gap-1 text-indigo-500 text-sm hover:underline">
            <ArrowLeft className="w-4 h-4" /> Back to Members
          </Link>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">{member.first_name} {member.last_name}</h1>
              <p className="text-gray-500 text-sm mt-1">{member.phone || "No phone"} · {member.email || "No email"}</p>
            </div>
            <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium capitalize">{member.membership_status}</span>
          </div>
          <div className="grid grid-cols-4 gap-4 mt-6">
            <div><p className="text-xs text-gray-400">Gender</p><p className="text-sm font-medium text-gray-700 capitalize">{member.gender || "—"}</p></div>
            <div><p className="text-xs text-gray-400">Marital Status</p><p className="text-sm font-medium text-gray-700 capitalize">{member.marital_status || "—"}</p></div>
            <div><p className="text-xs text-gray-400">Occupation</p><p className="text-sm font-medium text-gray-700">{member.occupation || "—"}</p></div>
            <div><p className="text-xs text-gray-400">Member Since</p><p className="text-sm font-medium text-gray-700">{member.membership_date || "—"}</p></div>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 mb-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Giving History</h2>
            <span className="text-sm font-bold text-green-600">Total: KES {total.toLocaleString()}</span>
          </div>
          {giving.length === 0 ? (
            <div className="text-center py-8">
              <DollarSign className="w-8 h-8 text-gray-300 mx-auto mb-2" />
              <p className="text-gray-400 text-sm">No giving records yet</p>
              <Link href="/giving" className="text-indigo-600 text-sm hover:underline mt-1 block">+ Record Giving</Link>
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {["Date","Category","Amount (KES)","Method","M-Pesa Ref"].map(h => (
                    <th key={h} className="text-left text-xs text-gray-500 font-medium px-4 py-2">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {giving.map(r => (
                  <tr key={r.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-500">{r.created_at?.slice(0,10)}</td>
                    <td className="px-4 py-3"><span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{r.category_name}</span></td>
                    <td className="px-4 py-3 text-sm font-bold text-green-600">KES {r.amount_kes.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-gray-500 capitalize">{r.payment_method}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">{r.mpesa_ref || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        <div className="flex gap-3">
          <Link href="/giving" className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">+ Record Giving for this Member</Link>
          <Link href="/attendance" className="border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50">View Attendance →</Link>
        </div>
      </main>
    </div>
  );
}
'''
open('/app/frontend/member_detail.tsx', 'w').write(txt)
print('done')
