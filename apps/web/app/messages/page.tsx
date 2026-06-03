"use client";
import { useEffect, useState, useRef } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../lib/api";
import Link from "next/link";
import { Plus, MessageSquare } from "lucide-react";

const CHURCH_ID = "00000000-0000-0000-0000-000000000001";
const BRANCH_ID = "00000000-0000-0000-0000-000000000002";

export default function MessagesPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);

  const load = () => {
    setLoading(true);
    api.get("/messages/?church_id=" + CHURCH_ID)
      .then(r => setMessages(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const save = async () => {
    const form = formRef.current;
    if (!form) return;
    const d = Object.fromEntries(new FormData(form));
    if (!d.subject) return alert("Subject is required");
    if (!d.body) return alert("Message body is required");
    setSaving(true);
    try {
      await api.post("/messages/", {
        church_id: CHURCH_ID, branch_id: BRANCH_ID,
        subject: d.subject, body: d.body,
        channel: d.channel, audience: d.audience
      });
      setShowForm(false); form.reset(); load();
    } catch(e: any) {
      alert("Error: " + (e.response?.data?.detail || e.message));
    } finally { setSaving(false); }
  };

  const channelColor = (c) => {
    if (c === "sms") return "bg-green-100 text-green-700";
    if (c === "whatsapp") return "bg-emerald-100 text-emerald-700";
    if (c === "email") return "bg-blue-100 text-blue-700";
    return "bg-gray-100 text-gray-600";
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-4 md:p-8 pb-24 md:pb-8">
        <div className="flex items-center gap-2 mb-1">
          <Link href="/" className="text-indigo-500 text-sm hover:underline">Back to Dashboard</Link>
          <span className="text-gray-300">/</span>
          <span className="text-sm text-gray-600">Messages</span>
        </div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Messages</h1>
            <p className="text-gray-500 text-sm">{messages.length} messages sent</p>
          </div>
          <button onClick={() => setShowForm(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
            <Plus className="w-4 h-4" /> Compose Message
          </button>
        </div>

        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-lg">
              <h2 className="text-lg font-bold text-gray-800 mb-4">Compose Message</h2>
              <form ref={formRef}>
                <div className="space-y-4">
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Subject</label>
                    <input type="text" name="subject" placeholder="Message subject"
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Message</label>
                    <textarea name="body" rows={4} placeholder="Type your message here..."
                      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">Channel</label>
                      <select name="channel" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none">
                        <option value="in_app">In-App</option>
                        <option value="sms">SMS</option>
                        <option value="whatsapp">WhatsApp</option>
                        <option value="email">Email</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">Audience</label>
                      <select name="audience" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none">
                        <option value="all">All Members</option>
                        <option value="branch">This Branch</option>
                        <option value="individual">Individual</option>
                      </select>
                    </div>
                  </div>
                </div>
              </form>
              <div className="flex gap-3 mt-6">
                <button onClick={() => setShowForm(false)} className="flex-1 border border-gray-200 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
                <button onClick={save} disabled={saving} className="flex-1 bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? "Sending..." : "Send Message →"}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {loading ? <p className="p-6 text-gray-400 text-sm">Loading...</p> : messages.length === 0 ? (
            <div className="p-12 text-center">
              <MessageSquare className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400 mb-3">No messages sent yet</p>
              <button onClick={() => setShowForm(true)} className="text-indigo-600 text-sm font-medium">+ Send First Message</button>
            </div>
          ) : (
            <div className="overflow-x-auto"><table className="w-full min-w-[500px]">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {["Date","Subject","Channel","Audience","Status"].map(h => (
                    <th key={h} className="text-left text-xs text-gray-500 font-medium px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {messages.map(m => (
                  <tr key={m.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-500">{m.created_at?.slice(0,10)}</td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-800">{m.subject}</td>
                    <td className="px-4 py-3"><span className={"text-xs px-2 py-0.5 rounded-full font-medium " + channelColor(m.channel)}>{m.channel}</span></td>
                    <td className="px-4 py-3 text-sm text-gray-500 capitalize">{m.audience}</td>
                    <td className="px-4 py-3"><span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">{m.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table></div>
          )}
        </div>
      </main>
    </div>
  );
}
