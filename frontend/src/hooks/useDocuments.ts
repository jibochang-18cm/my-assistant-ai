"use client";

import { useCallback, useEffect, useState } from "react";
import { fetchDocuments, type DocumentInfo } from "@/lib/api";

// 知识库里已有讲义的列表状态，上传成功后调用 refresh() 刷新
export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const docs = await fetchDocuments();
      setDocuments(docs);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { documents, isLoading, error, refresh };
}
