import os
os.makedirs('/app/frontend', exist_ok=True)
txt = '''"use client";
import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import api from "../lib/api";
import { Users, DollarSign, FolderOpen, CalendarCheck } from "lucide-react";
import Link from "next/link";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [giving, setGiving] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/dashboard/hq/?church_id=" + CHURCH_ID),
      api.get("/giving/summary/?church_id=" + CHURCH_ID),
      api.get("/attendance/sessions/?church_id=" + CHURCH_ID),
    ]).then(([d, g, s]) => {
      setData(d.data);
      setGiving(g.data);
      setSessions(s.data);
    }).finally(() => setLoading(false));
  }, []);

  const totalGiving = giving.reduce((s, g) => s + g.total_kes, 0);
  const lastSession = sessions[0];

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">HQ Dashboard</h1>
          <p className="text-gray-500 text-sm">Grace Community Church</p>
        </div>
        {loading ? <p className="text-gray-400">Loading...</p> : (
          <>
            <div className="grid grid-cols-4 gap-4 mb-8">
              <Link href="/members" className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4 hover:shadow-md transition-shadow">
                <div className="bg-blue-500 p-3 rounded-lg"><Users className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Total Members</p><p className="text-2xl font-bold text-gray-800">{data?.total_members || 0}</p><p className="text-xs text-indigo-500 mt-0.5">View all</p></div>
              </Link>
              <Link href="/giving" className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4 hover:shadow-md transition-shadow">
                <div className="bg-green-500 p-3 rounded-lg"><DollarSign className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Total Giving</p><p className="text-2xl font-bold text-gray-800">KES {totalGiving.toLocaleString()}</p><p className="text-xs text-indigo-500 mt-0.5">View records</p></div>
              </Link>
              <Link href="/projects" className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4 hover:shadow-md transition-shadow">
                <div className="bg-yellow-500 p-3 rounded-lg"><FolderOpen className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Active Projects</p><p className="text-2xl font-bold text-gray-800">{data?.active_projects || 0}</p><p className="text-xs text-indigo-500 mt-0.5">View projects</p></div>
              </Link>
              <Link href="/attendance" className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4 hover:shadow-md transition-shadow">
                <div className="bg-purple-500 p-3 rounded-lg"><CalendarCheck className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Last Attendance</p><p className="text-2xl font-bold text-gray-800">{lastSession ? lastSession.total_count : 0}</p><p className="text-xs text-indigo-500 mt-0.5">View sessions</p></div>
              </Link>
            </div>

            <div className="grid grid-cols-3 gap-6 mb-6">
              <div className="col-span-2 bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-sm font-semibold text-gray-700 mb-4">Giving by Category</h2>
                {giving.length === 0 ? <p className="text-gray-400 text-sm text-center py-8">No giving records yet</p> : (
                  <div className="space-y-3">
                    {giving.map(g => {
                      const pct = totalGiving > 0 ? Math.round(g.total_kes / totalGiving * 100) : 0;
                      return (
                        <div key={g.category}>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600 font-medium">{g.category}</span>
                            <span className="text-gray-800 font-bold">KES {g.total_kes.toLocaleString()} <span className="text-gray-400 font-normal">({pct}%)</span></span>
                          </div>
                          <div className="w-full bg-gray-100 rounded-full h-2">
                            <div className="bg-indigo-500 h-2 rounded-full" style={{width: pct + "%"}} />
                          </div>
                        </div>
                      );
                    })}
                    <div className="pt-3 border-t border-gray-100 flex justify-between">
                      <span className="text-sm font-bold text-gray-700">Total</span>
                      <span className="text-sm font-bold text-green-600">KES {totalGiving.toLocaleString()}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-sm font-semibold text-gray-700 mb-4">Last Sunday Report</h2>
                {!lastSession ? <p className="text-gray-400 text-sm text-center py-8">No sessions yet</p> : (
                  <div className="space-y-3">
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Date</span><span className="text-sm font-medium text-gray-700">{lastSession.session_date}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Total</span><span className="text-sm font-bold text-gray-800">{lastSession.total_count}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Adults</span><span className="text-sm text-gray-600">{lastSession.adult_count}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Children</span><span className="text-sm text-gray-600">{lastSession.child_count}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">First Timers</span><span className="text-sm font-medium text-orange-500">{lastSession.first_time_visitors}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Salvations</span><span className="text-sm font-medium text-green-600">{lastSession.salvations}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Offering</span><span className="text-sm font-bold text-green-600">KES {lastSession.total_offering_kes.toLocaleString()}</span></div>
                    <div className="flex justify-between"><span className="text-xs text-gray-400">Tithe</span><span className="text-sm font-bold text-green-600">KES {lastSession.total_tithe_kes.toLocaleString()}</span></div>
                    <Link href="/attendance" className="block text-center text-xs text-indigo-600 hover:underline pt-2">View all sessions</Link>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-sm font-semibold text-gray-700 mb-4">Branch Overview</h2>
              <div className="grid grid-cols-2 gap-4">
                {data?.branches?.map(b => (
                  <div key={b.branch_id} className="border border-gray-100 rounded-lg p-4">
                    <p className="font-semibold text-gray-800">{b.branch_name}</p>
                    <p className="text-xs text-gray-500 mb-3">Pastor: {b.pastor || "Pastor John Kamau"}</p>
                    <div className="flex gap-6">
                      <div><p className="text-xs text-gray-400">Members</p><p className="font-bold text-gray-700">{b.total_members}</p></div>
                      <div><p className="text-xs text-gray-400">Total Giving</p><p className="font-bold text-green-600">KES {(b.total_giving_kes || 0).toLocaleString()}</p></div>
                    </div>
                    <Link href="/giving" className="text-xs text-indigo-500 hover:underline mt-2 block">View giving</Link>
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
'''
open('/app/frontend/dashboard.tsx', 'w').write(txt)
print('done')
