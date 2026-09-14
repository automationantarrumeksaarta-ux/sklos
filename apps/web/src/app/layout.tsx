import type { Metadata } from "next";
import { Space_Grotesk, Inter } from "next/font/google";
import "./globals.css";
import LeftRail from "@/components/LeftRail";

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
  weight: ["500", "700"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "SKLOS — SmartEdu Kaizen Loop",
  description: "SmartEdu Kaizen Loop Operating System — local pilot",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body
        className={`${spaceGrotesk.variable} ${inter.variable} font-body antialiased`}
      >
        <div className="mx-auto flex min-h-screen max-w-6xl">
          <LeftRail />
          <main className="flex-1 px-5 py-8 md:px-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
