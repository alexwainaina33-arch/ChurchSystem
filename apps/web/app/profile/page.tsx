'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ProfilePage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [role, setRole] = useState('')
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setName(localStorage.getItem('user_name') || '')
    setUsername(localStorage.getItem('username') || '')
    setRole(localStorage.getItem('user_role') || '')
  }, [])

  function logout() {
    localStorage.clear()
    document.cookie = 'token=; path=/; max-age=0'
    router.push('/login')
  }

  async function handleChangePassword(e: React.FormEvent) {
    e.preventDefault()
    setMsg(''); setErr('')
    if (newPassword !== confirm) { setErr('New passwords do not match'); return }
    if (newPassword.length < 6) { setErr('Password must be at least 6 characters'); return }
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8001/api/v1/auth/change-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, old_password: oldPassword, new_password: newPassword })
      })
      const data = await res.json()
      if (!res.ok) { setErr(data.detail || 'Failed'); setLoading(false); return }
      setMsg('Password changed successfully')
      setOldPassword(''); setNewPassword(''); setConfirm('')
    } catch(e) {
      setErr('Cannot connect to server')
    }
    setLoading(false)
  }

  const roleLabel = { hq_admin: 'HQ Admin', pastor: 'Pastor', branch_admin: 'Branch Admin', treasurer: 'Treasurer' }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => router.back()} className="text-gray-500 hover:text-gray-800 text-sm flex items-center gap-1">
            ← Back
          </button>
          <span className="text-gray-300">/</span>
          <span className="text-gray-700 font-medium">My Profile</span>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold text-white" style={{background:'linear-gradient(135deg,#4f46e5,#7c3aed)'}}>
              {name.charAt(0).toUpperCase()}
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">{name}</h1>
              <p className="text-gray-500 text-sm">@{username}</p>
              <span className="inline-block mt-1 px-3 py-0.5 rounded-full text-xs font-medium text-white" style={{background:'#4f46e5'}}>
                {roleLabel[role] || role}
              </span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-gray-400 text-xs mb-1">Username</p>
              <p className="font-medium text-gray-700">{username}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-gray-400 text-xs mb-1">Role</p>
              <p className="font-medium text-gray-700">{roleLabel[role] || role}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-gray-400 text-xs mb-1">Church</p>
              <p className="font-medium text-gray-700">Grace Community Church</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-gray-400 text-xs mb-1">Branch</p>
              <p className="font-medium text-gray-700">Nairobi Main Branch</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
          <h2 className="text-base font-semibold text-gray-800 mb-4">Change Password</h2>
          {msg && <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4 text-sm">{msg}</div>}
          {err && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">{err}</div>}
          <form onSubmit={handleChangePassword}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
              <input type="password" value={oldPassword} onChange={e => setOldPassword(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter current password" required />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
              <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter new password" required />
            </div>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
              <input type="password" value={confirm} onChange={e => setConfirm(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Confirm new password" required />
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-3 rounded-lg text-white font-semibold text-sm"
              style={{background: loading ? '#9ca3af' : 'linear-gradient(135deg,#4f46e5,#7c3aed)'}}>
              {loading ? 'Updating...' : 'Update Password'}
            </button>
          </form>
        </div>

        <button onClick={logout}
          className="w-full py-3 rounded-lg border-2 border-red-200 text-red-600 font-semibold text-sm hover:bg-red-50 transition-colors">
          Sign Out
        </button>
      </div>
    </div>
  )
}
