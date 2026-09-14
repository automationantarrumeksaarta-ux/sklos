"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/today", label: "My Day", stage: "Capture · Execute" },
  { href: "/team", label: "Team Room", stage: "Detect Gap" },
  { href: "/students", label: "Student Room", stage: "SEC Intelligence" },
  { href: "/admin", label: "Admin Import", stage: "Standardize" },
];

export default function LeftRail() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-56 shrink-0 border-r border-line py-8 pl-6 pr-4 md:block">
      <div className="mb-10">
        <p className="font-display text-lg font-bold leading-none text-ink">
          SKLOS
        </p>
        <p className="mt-1 text-xs text-ink-faint">SmartEduCafe pilot</p>
      </div>

      <nav className="loop-rule border-l-2 border-transparent pl-4">
        <ul className="space-y-6">
          {NAV.map((item) => {
            const active = pathname?.startsWith(item.href);
            return (
              <li key={item.href} className="relative -ml-[18px] pl-5">
                <span
                  className={`absolute left-0 top-1.5 h-2 w-2 rounded-full ${
                    active ? "bg-kaizen" : "bg-line"
                  }`}
                  aria-hidden
                />
                <Link
                  href={item.href}
                  className={`font-display text-sm font-medium ${
                    active ? "text-ink" : "text-ink-faint hover:text-ink"
                  }`}
                >
                  {item.label}
                </Link>
                <p className="text-[11px] text-ink-faint">{item.stage}</p>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="mt-12 rounded-card border border-line bg-white/60 p-3">
        <p className="text-[11px] uppercase tracking-normal text-ink-faint">
          Fase pilot
        </p>
        <p className="mt-1 text-sm text-ink">Execution Foundation</p>
      </div>
    </aside>
  );
}
