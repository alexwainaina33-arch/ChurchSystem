txt = open('/app/frontend/pages/giving.tsx').read()

old = '''    <div className="flex min-h-screen bg-gray-50">
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
        </div>'''

new = '''    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">
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
            <button onClick={exportCSV} className="flex items-center gap-2 border border-gray-200 text-gray-600 px-3 py-2 rounded-lg text-sm hover:bg-gray-50">
              <Download className="w-4 h-4" /><span className="hidden md:inline"> Export CSV</span>
            </button>
            <button onClick={() => setShowForm(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
              <Plus className="w-4 h-4" /><span className="hidden md:inline"> Record Giving</span><span className="md:hidden">Record</span>
            </button>
          </div>
        </div>'''

txt = txt.replace(old, new)

old2 = '''        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
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
        </div>'''

new2 = '''        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {loading ? <p className="p-6 text-gray-400 text-sm">Loading...</p> : records.length === 0 ? (
            <div className="p-12 text-center">
              <DollarSign className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400 mb-3">No giving records yet</p>
              <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-medium">+ Record First Giving</button>
            </div>
          ) : (
            <div className="overflow-x-auto">
            <table className="w-full min-w-[600px]">
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
            </div>
          )}
        </div>'''

txt = txt.replace(old2, new2)
open('/app/frontend/pages/giving.tsx', 'w').write(txt)
print('done')
