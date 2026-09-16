import type { Metadata } from "next";
import "./globals.css";
import { uiText } from "@/lib/text";

export const metadata: Metadata = {
  title: uiText.meta.title,
  description: uiText.meta.description,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
