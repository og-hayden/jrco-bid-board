'use client'

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="bg-accent-color text-white flex justify-between items-center p-4">
      <ul className="flex">
        <li className={`${pathname === "/bids" ? "text-red-950" : ""} hover:underline mr-6`}>
          <Link href="/bids" legacyBehavior><a className="font-semibold">Bids</a></Link>
        </li>
        <li className={`${pathname === "/calendar" ? "text-red-950" : ""} hover:underline mr-6`}>
          <Link href="/calendar" legacyBehavior><a className="font-semibold">Calendar</a></Link>
        </li>
        <li className={`${pathname === "/archived" ? "text-red-950" : ""} hover:underline`}>
          <Link href="/archived" legacyBehavior><a className="font-semibold">Archived</a></Link>
        </li>
      </ul>
      <ul>
        <li className={`${pathname === "/admin" ? "text-red-950" : ""} hover:underline`}>
          <Link href="/admin" legacyBehavior><a className="font-semibold">Admin</a></Link>
        </li>
      </ul>
    </nav>
  );
}



