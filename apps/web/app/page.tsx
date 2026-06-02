"use client";
import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import api from "../lib/api";
import { Users, DollarSign, FolderOpen, GitBranch } from "lucide-react";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/hq/?church_id=" + CHURCH_ID)
      .then(r => setData(r.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">HQ Dashboard</h1>
        <p className="text-gray-500 text-sm mb-6">Grace Community Church — All Branches</p>
        {loading && <p className="text-gray-400">Loading...</p>}
        {data && (
          <>
            <div className="grid grid-cols-4 gap-4 mb-8">
              <div className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4">
                <div className="bg-blue-500 p-3 rounded-lg"><Users className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Total Members</p><p className="text-xl font-bold text-gray-800">{data.total_members}</p></div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4">
                <div className="bg-green-500 p-3 rounded-lg"><DollarSign className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Total Giving</p><p className="text-xl font-bold text-gray-800">KES {(data.total_giving_kes || 0).toLocaleString()}</p></div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4">
                <div className="bg-yellow-500 p-3 rounded-lg"><FolderOpen className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Active Projects</p><p className="text-xl font-bold text-gray-800">{data.active_projects}</p></div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-5 flex items-center gap-4">
                <div className="bg-purple-500 p-3 rounded-lg"><GitBranch className="w-5 h-5 text-white" /></div>
                <div><p className="text-xs text-gray-500">Branches</p><p className="text-xl font-bold text-gray-800">{data.total_branches}</p></div>
              </div>
            </div>
            <h2 className="text-lg font-semibold text-gray-700 mb-3">Branch Overview</h2>
            <div className="grid grid-cols-2 gap-4">
              {data.branches && data.branches.map((b) => (
                <div key={b.branch_id} className="bg-white rounded-xl shadow-sm p-5">
                  <p className="font-semibold text-gray-800">{b.branch_name}</p>
                  <p className="text-xs text-gray-500 mb-3">Pastor: {b.pastor || "—"}</p>
                  <div className="flex gap-6">
                    <div><p className="text-xs text-gray-400">Members</p><p className="font-bold text-gray-700">{b.total_members}</p></div>
                    <div><p className="text-xs text-gray-400">Total Giving</p><p className="font-bold text-green-600">KES {(b.total_giving_kes || 0).toLocaleString()}</p></div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
