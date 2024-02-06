import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

import Navigation from "./components/Navigation";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "JR&Co Bid Board",
  description: "Centralized bid board for JR&Co",
};

// Assuming Navigation is correctly imported
export default function RootLayout({ children }: { children: React.ReactNode; }) {
  return (
    <>
      <Navigation /> {/* This will be included on all pages using this layout */}
      <div>{children}</div>
    </>
  );
}
