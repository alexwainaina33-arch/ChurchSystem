import os
txt = '''\'use client\'
import { useEffect, useState } from \'react\'
import Sidebar from \'../components/Sidebar\'
import api from \'../lib/api\'
import Link from \'next/link\'
import { ChevronRight, TrendingUp, TrendingDown, DollarSign, CheckCircle, AlertCircle } from \'lucide-react\'

const CHURCH_ID = \'00000000-0000-0000-0000-000000000001\'

export default function FinancePage() {
  const [data, setData]     = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get(\'/dashboard/finance/?church_id=\' + CHURCH_ID)
      .then(r => setData(r.data))
      .finally(() => setLoading(false))
  }, [])

  const assets    = data ? data.accounts.filter((a:any) => a.type === \'asset\')   : []
  const income    = data ? data.accounts.filter((a:any) => a.type === \'income\')  : []
  const expenses  = data ? data.accounts.filter((a:any) => a.type === \'expense\') : []
  const totalIncome   = income.reduce((s:number,  a:any) => s + a.balance_kes, 0)
  const totalExpenses = expenses.reduce((s:number, a:any) => s + a.balance_kes, 0)
  const netSurplus    = totalIncome - totalExpenses
  const totalDebits   = data ? data.accounts.filter((a:any) => a.type===\'asset\'||a.type===\'expense\').reduce((s:number,a:any) => s+a.balance_kes,0) : 0
  const totalCredits  = data ? data.accounts.filter((a:any) => a.type===\'income\'||a.type===\'liability\'||a.type===\'equity\').reduce((s:number,a:any) => s+a.balance_kes,0) : 0
  const balanced = totalDebits === totalCredits

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 min-w-0 pb-24 md:pb-0">

        <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200
                           px-4 md:px-8 py-3.5 shadow-sm">
          <div className="ml-12 md:ml-0">
            <div className="flex items-center gap-2 text-xs text-gray-400 mb-0.5">
              <Link href="/" className="hover:text-indigo-600 transition-colors">Dashboard</Link>
              <ChevronRight className="w-3 h-3" />
              <span className="text-gray-600 font-medium">Finance</span>
            </div>
            <h1 className="text-gray-900 font-bold text-lg leading-tight">Finance Dashboard</h1>
          </div>
        </header>

        <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-5">
          {loading ? (
            <div className="flex items-center justify-center py-32 gap-3">
              <div className="w-8 h-8 border-[3px] border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
              <span className="text-gray-400 text-sm">Loading financials...</span>
            </div>
          ) : !data ? (
            <p className="text-gray-400 text-sm">No data available.</p>
          ) : (<>

            {/* Summary cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 md:gap-4">
              <div className="bg-white rounded-2xl border border-emerald-100 shadow-sm p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-9 h-9 rounded-xl bg-emerald-50 flex items-center justify-center">
                    <TrendingUp className="w-4 h-4 text-emerald-600" />
                  </div>
                  <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">Total Income</p>
                </div>
                <p className="text-2xl font-black text-emerald-600">KES {totalIncome.toLocaleString()}</p>
              </div>
              <div className="bg-white rounded-2xl border border-red-100 shadow-sm p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-9 h-9 rounded-xl bg-red-50 flex items-center justify-center">
                    <TrendingDown className="w-4 h-4 text-red-500" />
                  </div>
                  <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">Total Expenses</p>
                </div>
                <p className="text-2xl font-black text-red-500">KES {totalExpenses.toLocaleString()}</p>
              </div>
              <div className={`bg-white rounded-2xl border shadow-sm p-5
                ${netSurplus >= 0 ? \'border-indigo-100\' : \'border-red-100\'}`}>
                <div className="flex items-center gap-3 mb-3">
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center
                    ${netSurplus >= 0 ? \'bg-indigo-50\' : \'bg-red-50\'}`}>
                    <DollarSign className={`w-4 h-4 ${netSurplus >= 0 ? \'text-indigo-600\' : \'text-red-500\'}`} />
                  </div>
                  <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">Net Surplus</p>
                </div>
                <p className={`text-2xl font-black ${netSurplus >= 0 ? \'text-indigo-600\' : \'text-red-600\'}`}>
                  KES {netSurplus.toLocaleString()}
                </p>
              </div>
            </div>

            {/* Trial Balance */}
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="flex items-center justify-between px-5 md:px-6 py-4 border-b border-gray-100">
                <div>
                  <h2 className="text-sm font-bold text-gray-900">Trial Balance</h2>
                  <p className="text-xs text-gray-400 mt-0.5">Auto-generated from GL transactions</p>
                </div>
                <span className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full
                                  font-semibold border
                  ${balanced
                    ? \'bg-emerald-50 text-emerald-700 border-emerald-200\'
                    : \'bg-red-50 text-red-700 border-red-200\'}`}>
                  {balanced
                    ? <><CheckCircle className="w-3.5 h-3.5" /> BALANCED</>
                    : <><AlertCircle className="w-3.5 h-3.5" /> UNBALANCED</>
                  }
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[500px]">
                  <thead className="bg-gray-50 border-b border-gray-100">
                    <tr>
                      {[\'Code\',\'Account Name\',\'Type\',\'Debit (KES)\',\'Credit (KES)\'].map((h,i) => (
                        <th key={h} className={`text-xs text-gray-500 font-semibold uppercase tracking-wide
                                                px-4 py-3 ${i >= 3 ? \'text-right\' : \'text-left\'}`}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {data.accounts.map((a:any) => {
                      const isDebit = a.type === \'asset\' || a.type === \'expense\'
                      return (
                        <tr key={a.code} className="hover:bg-gray-50/60 transition-colors">
                          <td className="px-4 py-3 text-sm text-gray-500 font-mono">{a.code}</td>
                          <td className="px-4 py-3 text-sm font-medium text-gray-800">{a.name}</td>
                          <td className="px-4 py-3">
                            <span className={`text-xs px-2 py-0.5 rounded-full font-medium capitalize
                              ${a.type===\'income\'  ? \'bg-emerald-50 text-emerald-700\' :
                                a.type===\'expense\' ? \'bg-red-50 text-red-600\' :
                                a.type===\'asset\'   ? \'bg-sky-50 text-sky-700\' :
                                \'bg-gray-100 text-gray-500\'}`}>
                              {a.type}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-right font-semibold text-gray-800">
                            {isDebit && a.balance_kes > 0 ? a.balance_kes.toLocaleString() : \'—\'}
                          </td>
                          <td className="px-4 py-3 text-sm text-right font-semibold text-emerald-600">
                            {!isDebit && a.balance_kes > 0 ? a.balance_kes.toLocaleString() : \'—\'}
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                  <tfoot className="border-t-2 border-gray-200 bg-gray-50">
                    <tr>
                      <td colSpan={3} className="px-4 py-3 text-sm font-bold text-gray-800">TOTAL</td>
                      <td className="px-4 py-3 text-sm font-black text-right text-gray-900">
                        {totalDebits.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-sm font-black text-right text-emerald-600">
                        {totalCredits.toLocaleString()}
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>

            {/* Recent GL Transactions */}
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="px-5 md:px-6 py-4 border-b border-gray-100">
                <h2 className="text-sm font-bold text-gray-900">Recent GL Transactions</h2>
                <p className="text-xs text-gray-400 mt-0.5">Double-entry — every transaction balanced</p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[550px]">
                  <thead className="bg-gray-50 border-b border-gray-100">
                    <tr>
                      {[\'Date\',\'DR Account\',\'CR Account\',\'Amount (KES)\',\'Description\'].map((h,i) => (
                        <th key={h} className="text-left text-xs text-gray-500 font-semibold
                                               uppercase tracking-wide px-4 py-3">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {data.recent_transactions.map((t:any, i:number) => (
                      <tr key={i} className="hover:bg-gray-50/60 transition-colors">
                        <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">{t.date?.slice(0,10)}</td>
                        <td className="px-4 py-3">
                          <span className="text-sm font-semibold text-red-500 whitespace-nowrap">DR {t.debit}</span>
                        </td>
                        <td className="px-4 py-3">
                          <span className="text-sm font-semibold text-emerald-600 whitespace-nowrap">CR {t.credit}</span>
                        </td>
                        <td className="px-4 py-3 text-sm font-black text-gray-900 whitespace-nowrap">
                          KES {t.amount_kes.toLocaleString()}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500">{t.description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </>)}
        </div>
      </main>
    </div>
  )
}
'''
open('/app/frontend/pages/finance.tsx', 'w').write(txt)
print('Finance done')
