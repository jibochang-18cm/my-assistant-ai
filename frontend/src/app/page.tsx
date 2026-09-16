import { UploadPanel } from "@/components/UploadPanel";
import { ChatPanel } from "@/components/ChatPanel";
import { uiText } from "@/lib/text";

export default function Home() {
  return (
    <main>
      <header className="app-header">
        <h2>{uiText.pageTitle}</h2>
        <p className="app-subtitle">{uiText.subtitle}</p>
      </header>
      <UploadPanel />
      <ChatPanel />
    </main>
  );
}
