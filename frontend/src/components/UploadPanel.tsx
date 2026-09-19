"use client";

import { useRef, useState } from "react";
import { uploadPdf } from "@/lib/api";
import { uiText } from "@/lib/text";
import { useDocuments } from "@/hooks/useDocuments";
import { DocumentList } from "./DocumentList";

type FileStatus = "pending" | "uploading" | "success" | "error";

interface FileUploadState {
  file: File;
  status: FileStatus;
  message?: string;
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function UploadPanel() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploads, setUploads] = useState<FileUploadState[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const { documents, isLoading, error, refresh } = useDocuments();

  const handleFileChange = () => {
    const files = Array.from(fileInputRef.current?.files ?? []);
    setUploads(files.map((file) => ({ file, status: "pending" })));
  };

  const handleUpload = async () => {
    if (uploads.length === 0) {
      alert(uiText.upload.noFileAlert);
      return;
    }

    setIsUploading(true);

    // 逐个上传，避免同时给后端塞好几个大文件 / 并发跑 embedding 模型
    for (let i = 0; i < uploads.length; i++) {
      setUploads((prev) =>
        prev.map((u, idx) => (idx === i ? { ...u, status: "uploading" } : u))
      );

      try {
        await uploadPdf(uploads[i].file);
        setUploads((prev) =>
          prev.map((u, idx) => (idx === i ? { ...u, status: "success" } : u))
        );
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        setUploads((prev) =>
          prev.map((u, idx) => (idx === i ? { ...u, status: "error", message } : u))
        );
      }
    }

    setIsUploading(false);
    if (fileInputRef.current) fileInputRef.current.value = "";
    refresh();
  };

  return (
    <div className="box">
      <h3>{uiText.upload.heading}</h3>
      <div className="upload-row">
        <input type="file" accept=".pdf" multiple ref={fileInputRef} onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={isUploading}>
          {uiText.upload.uploadButton}
        </button>
      </div>

      {uploads.length > 0 && (
        <>
          <p className="file-info">{uiText.upload.selectedCount(uploads.length)}</p>
          <ul className="upload-file-list">
            {uploads.map((u, idx) => (
              <li key={idx} className={`upload-file-item status-${u.status}`}>
                <span className="upload-file-name">
                  {u.file.name}
                  <span className="upload-file-size">（{formatFileSize(u.file.size)}）</span>
                </span>
                <span className="upload-file-status">
                  {u.status === "pending" && uiText.upload.fileStatusPending}
                  {u.status === "uploading" && uiText.upload.fileStatusUploading}
                  {u.status === "success" && "✅"}
                  {u.status === "error" && `❌ ${u.message}`}
                </span>
              </li>
            ))}
          </ul>
        </>
      )}

      <h4 className="doc-list-heading">{uiText.documents.heading}</h4>
      <DocumentList documents={documents} isLoading={isLoading} error={error} />
    </div>
  );
}
