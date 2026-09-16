"use client";

import { useRef, useState } from "react";
import { uploadPdf } from "@/lib/api";
import { uiText } from "@/lib/text";

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function UploadPanel() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileInfo, setFileInfo] = useState<string>("");
  const [status, setStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = () => {
    const file = fileInputRef.current?.files?.[0];
    setFileInfo(file ? `已选择：${file.name}（${formatFileSize(file.size)}）` : "");
    setStatus("");
  };

  const handleUpload = async () => {
    const file = fileInputRef.current?.files?.[0];
    if (!file) {
      alert(uiText.upload.noFileAlert);
      return;
    }

    setStatus(uiText.upload.uploading);
    setIsUploading(true);

    try {
      const data = await uploadPdf(file);
      setStatus(data.message);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setStatus(uiText.upload.uploadFailedPrefix + message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="box">
      <h3>{uiText.upload.heading}</h3>
      <div className="upload-row">
        <input type="file" accept=".pdf" ref={fileInputRef} onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={isUploading}>
          {uiText.upload.uploadButton}
        </button>
      </div>
      {fileInfo && <p className="file-info">{fileInfo}</p>}
      {status && <p className="upload-status">{status}</p>}
    </div>
  );
}
