import os
txt = '''"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Church, Users, CalendarCheck, DollarSign, FolderOpen, MessageSquare, LayoutDashboard, TrendingUp, Settings } from "lucide-react";

const nav = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/members", label: "Members", icon: Users },
  { href: "/attendance", label: "Attendance", icon: CalendarCheck },
  { href: "/giving", label: "Giving", icon: DollarSign },
  { href: "/projects", label: "Projects", icon: FolderOpen },
  { href: "/messages", label: "Messages", icon: MessageSquare },
  { href: "/finance", label: "Finance", icon: TrendingUp },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  const path = usePathname();
  return (
    <aside className="w-64 min-h-screen bg-indigo-900 text-white flex flex-col">
      <div className="p-6 border-b border-indigo-700">
        <div className="flex items-center gap-2">
          <Church className="w-7 h-7 text-yellow-400" />
          <span className="text-xl font-bold">ChurchHub</span>
        </div>
        <p className="text-indigo-300 text-xs mt-1">Manage your church, your way.</p>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {nav.map(function(item) {
          const Icon = item.icon;
          return (
            <Link key={item.href} href={item.href} className={path === item.href ? "flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium bg-indigo-700 text-white" : "flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium text-indigo-200 hover:bg-indigo-800"}>
              <Icon className="w-4 h-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-indigo-700 text-xs text-indigo-400">Grace Community Church</div>
    </aside>
  );
}
'''
open('/app/frontend/Sidebar.tsx', 'w').write(txt)
print('done')
