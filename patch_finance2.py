import os
txt = '''"use client";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import Link from "next/link";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";

export default function FinancePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/finance/?church_id=" + CHURCH_ID)
      .then(r => setData(r.data))
      .finally(() => setLoading(false));
  }, []);

  const assets = data ? data.accounts.filter(a => a.type === "asset") : [];
  const income = data ? data.accounts.filter(a => a.type === "income") : [];
  const expenses = data ? data.accounts.filter(a => a.type === "expense") : [];
  const totalIncome = income.reduce((s, a) => s + a.balance_kes, 0);
  const totalExpenses = expenses.reduce((s, a) => s + a.balance_kes, 0);
  const netSurplus = totalIncome - totalExpenses;
  const totalDebits = data ? data.accounts.filter(a => a.type === "asset" || a.type === "expense").reduce((s,a) => s + a.balance_kes, 0) : 0;
  const totalCredits = data ? data.accounts.filter(a => a.type === "income" || a.type === "liability" || a.type === "equity").reduce((s,a) => s + a.balance_kes, 0) : 0;
  const balanced = totalDebits === totalCredits;

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <div className="flex items-center gap-2 mb-1">
          <Link href="/" className="text-indigo-500 text-sm hover:underline">Back to Dashboard</Link>
          <span className="text-gray-300">/</span>
          <span className="text-sm text-gray-600">Finance</span>
        </div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Finance Dashboard</h1>
            <p className="text-gray-500 text-sm">Double-entry GL — Auto-generated from transactions</p>
          </div>
        </div>

        {loading ? <p className="text-gray-400">Loading...</p> : !data ? <p className="text-gray-400">No data</p> : (
          <>
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-white rounded-xl shadow-sm p-5">
                <p className="text-xs text-gray-400 mb-1">Total Income</p>
                <p className="text-2xl font-bold text-green-600">KES {totalIncome.toLocaleString()}</p>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-5">
                <p className="text-xs text-gray-400 mb-1">Total Expenses</p>
                <p className="text-2xl font-bold text-red-500">KES {totalExpenses.toLocaleString()}</p>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-5">
                <p className="text-xs text-gray-400 mb-1">Net Surplus</p>
                <p className={"text-2xl font-bold " + (netSurplus >= 0 ? "text-indigo-600" : "text-red-600")}>KES {netSurplus.toLocaleString()}</p>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Trial Balance</h2>
                <span className={"text-xs px-3 py-1 rounded-full font-semibold " + (balanced ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700")}>
                  {balanced ? "BALANCED" : "UNBALANCED"}
                </span>
              </div>
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left text-xs text-gray-500 font-medium px-4 py-2">Code</th>
                    <th className="text-left text-xs text-gray-500 font-medium px-4 py-2">Account Name</th>
                    <th className="text-left text-xs text-gray-500 font-medium px-4 py-2">Type</th>
                    <th className="text-right text-xs text-gray-500 font-medium px-4 py-2">Debit (KES)</th>
                    <th className="text-right text-xs text-gray-500 font-medium px-4 py-2">Credit (KES)</th>
                  </tr>
                </thead>
                <tbody>
                  {data.accounts.map(a => {
                    const isDebit = a.type === "asset" || a.type === "expense";
                    return (
                      <tr key={a.code} className="border-b border-gray-50 hover:bg-gray-50">
                        <td className="px-4 py-2 text-sm text-gray-500">{a.code}</td>
                        <td className="px-4 py-2 text-sm text-gray-800">{a.name}</td>
                        <td className="px-4 py-2 text-xs capitalize text-gray-500">{a.type}</td>
                        <td className="px-4 py-2 text-sm text-right font-medium text-gray-800">{isDebit && a.balance_kes > 0 ? a.balance_kes.toLocaleString() : "—"}</td>
                        <td className="px-4 py-2 text-sm text-right font-medium text-green-600">{!isDebit && a.balance_kes > 0 ? a.balance_kes.toLocaleString() : "—"}</td>
                      </tr>
                    );
                  })}
                </tbody>
                <tfoot className="border-t-2 border-gray-300 bg-gray-50">
                  <tr>
                    <td colSpan={3} className="px-4 py-3 text-sm font-bold text-gray-800">TOTAL</td>
                    <td className="px-4 py-3 text-sm font-bold text-right text-gray-800">{totalDebits.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm font-bold text-right text-green-600">{totalCredits.toLocaleString()}</td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-sm font-semibold text-gray-700 mb-4 uppercase tracking-wide">Recent GL Transactions</h2>
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-100">
                  <tr>
                    {["Date","DR Account","CR Account","Amount (KES)","Description"].map(h => (
                      <th key={h} className="text-left text-xs text-gray-500 font-medium px-4 py-2">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.recent_transactions.map((t, i) => (
                    <tr key={i} className="border-b border-gray-50 hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-500">{t.date?.slice(0,10)}</td>
                      <td className="px-4 py-3 text-sm font-medium text-red-500">DR {t.debit}</td>
                      <td className="px-4 py-3 text-sm font-medium text-green-600">CR {t.credit}</td>
                      <td className="px-4 py-3 text-sm font-bold text-gray-800">KES {t.amount_kes.toLocaleString()}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">{t.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
'''
open('/app/frontend/finance.tsx', 'w').write(txt)
print('done')
