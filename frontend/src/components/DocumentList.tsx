"use client";

import type { DocumentInfo } from "@/lib/api";
import { uiText } from "@/lib/text";

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

interface DocumentListProps {
  documents: DocumentInfo[];
  isLoading: boolean;
  error: string | null;
}

export function DocumentList({ documents, isLoading, error }: DocumentListProps) {
  if (isLoading) {
    return <p className="doc-list-status">{uiText.documents.loading}</p>;
  }

  if (error) {
    return <p className="doc-list-status doc-list-error">{uiText.documents.loadFailedPrefix + error}</p>;
  }

  if (documents.length === 0) {
    return <p className="doc-list-status">{uiText.documents.empty}</p>;
  }

  return (
    <ul className="doc-list">
      {documents.map((doc) => (
        <li key={doc.name} className="doc-item">
          <span className="doc-icon" aria-hidden="true">📄</span>
          <div className="doc-info">
            <div className="doc-name">{doc.name}</div>
            <div className="doc-meta">
              {uiText.documents.chunkAndPageInfo(doc.chunk_count, doc.pages)}
              {doc.size != null ? ` · ${formatFileSize(doc.size)}` : ""}
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
}
