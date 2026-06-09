"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState("");

  const [rawText, setRawText] = useState("");
  const [repairedText, setRepairedText] = useState("");

  const [analysis, setAnalysis] = useState<any>(null);
  const [smartSummary, setSmartSummary] = useState("");



  const [inputMode, setInputMode] = useState<"image" | "text">("image");

  const [inputText, setInputText] = useState("");

  const [structuredData, setStructuredData] = useState<any>(null);

  const [loading, setLoading] = useState(false);

  const [ocrStats, setOcrStats] = useState<any>(null);

  const [status, setStatus] = useState("");

  const [toast, setToast] = useState("");

  const [progress, setProgress] = useState(0);

  const showToast = (message: string) => {
    setToast(message);

    setTimeout(() => {
      setToast("");
    }, 3000);
  };

  const handleFileSelect = (selected: File) => {
    setFile(selected);

    const preview = URL.createObjectURL(selected);

    setImagePreview(preview);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();

    const droppedFile = e.dataTransfer.files?.[0];

    if (!droppedFile) return;

    handleFileSelect(droppedFile);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setProgress(10);
    setStatus("Extracting OCR Text...");

    try {
      const formData = new FormData();

      formData.append("file", file);

      const ocrResponse = await fetch(
        "https://structify-ai-backend.onrender.com/api/v1/ocr/extract",
        {
          method: "POST",
          body: formData,
        }
      );

      const ocrData = await ocrResponse.json();

      setProgress(40);

      setRawText(ocrData.raw_text || "");

      setOcrStats({
        averageConfidence: ocrData.average_confidence,
        totalOcrBlocks: ocrData.total_blocks,
      });

      setStatus("Repairing OCR Errors...");

      setProgress(60);

      setStatus("Building Document Structure...");

      const structureResponse = await fetch(
        "https://structify-ai-backend.onrender.com/api/v1/structure/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ocr_data: ocrData,
            enable_repair: true,
            doc_type: "auto",
          }),
        }
      );

      const structure = await structureResponse.json();

      setStructuredData(structure);

      if (structure.analysis) {
        setAnalysis(structure.analysis);
        setSmartSummary(
          structure.smart_summary || ""
        );
      }

      const repaired =
        structure.blocks
          ?.map((block: any) => block.text)
          .join("\n") || "";

      setRepairedText(repaired);

      setProgress(100);

      showToast("Document Processed Successfully");
    } catch (err) {
      console.error(err);

      showToast("Something went wrong");
    }

    setStatus("");
    setLoading(false);
  };

  const handleTextAnalysis = async () => {
    if (!inputText.trim()) return;

    setLoading(true);

    try {
      const response = await fetch(
        "https://structify-ai-backend.onrender.com/api/v1/text/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: inputText,
          }),
        }
      );

      const data = await response.json();

      setRawText(data.raw_text);

      setRepairedText(data.repaired_text);

      setStructuredData(
        data.structured_document
      );

      setAnalysis(data.analysis);
      setSmartSummary(data.smart_summary || "");

    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  const exportFile = async (format: string) => {
    if (!structuredData) return;

    try {
      const response = await fetch(
        `https://structify-ai-backend.onrender.com/api/v1/export?format_type=${format}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(structuredData),
        }
      );

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;
      a.download = `structify.${format}`;

      document.body.appendChild(a);

      a.click();

      a.remove();

      window.URL.revokeObjectURL(url);

      showToast(`${format.toUpperCase()} Download Started`);
    } catch (err) {
      console.error(err);
    }
  };

  const exportJSON = () => {
    if (!structuredData) return;

    const blob = new Blob(
      [JSON.stringify(structuredData, null, 2)],
      {
        type: "application/json",
      }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "structify.json";

    a.click();

    URL.revokeObjectURL(url);

    showToast("JSON Download Started");
  };

  const copyRepairedText = async () => {
    if (!repairedText) return;

    await navigator.clipboard.writeText(
      repairedText
    );

    showToast("Text Copied");
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-8 py-10">

        {/* HERO */}

        <div className="text-center mb-14">

          <div className="inline-flex px-4 py-2 rounded-full bg-slate-900 border border-slate-700 text-slate-300 text-sm mb-6">
            OCR → AI Repair → Structure Detection → Export
          </div>

          <h1 className="text-6xl md:text-7xl font-extrabold mb-4 tracking-tight">
            Structify AI
          </h1>

          <h2 className="text-2xl md:text-3xl font-semibold text-slate-200 mb-5">
            Turn messy OCR text into structured documents
          </h2>

          <p className="text-slate-400 text-lg md:text-xl max-w-3xl mx-auto leading-8">
            Extract text, repair OCR mistakes, recover document structure, and export clean documents in multiple formats.
          </p>

          <div className="flex flex-wrap justify-center gap-3 mt-8">

            <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg">
              📄 OCR Extraction
            </div>

            <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg">
              ✨ AI Repair
            </div>

            <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg">
              🧩 Structure Detection
            </div>

            <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg">
              📤 Multi-format Export
            </div>

          </div>

        </div>

        {/* UPLOAD */}

        <div className="border border-slate-800 rounded-xl p-6 mb-8">

          <div className="flex gap-3 mb-5">

            <button
              onClick={() => setInputMode("image")}
              className={`px-4 py-2 rounded-lg ${inputMode === "image"
                ? "bg-blue-600"
                : "bg-slate-800"
                }`}
            >
              Image Upload
            </button>

            <button
              onClick={() => setInputMode("text")}
              className={`px-4 py-2 rounded-lg ${inputMode === "text"
                ? "bg-blue-600"
                : "bg-slate-800"
                }`}
            >
              Paste Text
            </button>

          </div>

          <h2 className="text-2xl font-semibold mb-5">
            Upload Document
          </h2>

          {inputMode === "image" ? (
            <>

              <div
                onDragOver={(e) =>
                  e.preventDefault()
                }
                onDrop={handleDrop}
                className="
          border-2
          border-dashed
          border-slate-700
          rounded-xl
          min-h-[220px]
          flex
          flex-col
          items-center
          justify-center
          text-center
          bg-slate-900
          mb-5
        "
              >

                <p className="text-xl font-semibold mb-2">
                  📂 Drag & Drop Image Here
                </p>

                <p className="text-slate-400 mb-4">
                  or click below to browse files
                </p>

                <p className="text-xs text-slate-500 mb-4">
                  PNG • JPG • JPEG • Max Size: 10 MB
                </p>
                <div className="flex justify-center">
                  <label className="cursor-pointer bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded">
                    Choose File
                    <input
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={(e) => {
                        const selected = e.target.files?.[0];
                        if (!selected) return;
                        handleFileSelect(selected);
                      }}
                    />
                  </label>
                </div>

                {file && (
                  <p className="text-center text-green-400 mt-2">
                    {file.name}
                  </p>
                )}

              </div>

              <button
                onClick={handleUpload}
                disabled={loading || !file}
                className="
          bg-blue-600
          hover:bg-blue-700
          px-6
          py-3
          rounded-lg
          font-semibold
        "
              >
                {loading
                  ? status
                  : "Run OCR"}
              </button>

            </>
          ) : (
            <>

              <textarea
                value={inputText}
                onChange={(e) =>
                  setInputText(
                    e.target.value
                  )
                }
                placeholder="
Paste document content here...

Example:

Project Title: Smart Traffic System

Problem Statement

Current urban traffic systems are inefficient
        "
                className="
          w-full
          h-56
          bg-slate-900
          border
          border-slate-700
          rounded-xl
          p-4
          mb-5
          resize-none
        "
              />

              <button
                onClick={handleTextAnalysis}
                disabled={
                  loading ||
                  !inputText.trim()
                }
                className="
          bg-green-600
          hover:bg-green-700
          px-6
          py-3
          rounded-lg
          font-semibold
        "
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze Text"}
              </button>

            </>
          )}

          {loading && (
            <div className="mt-5">

              <div className="h-3 bg-slate-800 rounded-full overflow-hidden">

                <div
                  className="
            h-full
            bg-blue-500
            transition-all
            duration-500
          "
                  style={{
                    width: `${progress}%`,
                  }}
                />

              </div>

              <p className="mt-2 text-sm text-slate-400">
                {progress}% Complete
              </p>

            </div>
          )}

        </div>
        {/* OCR PANELS */}

        <div className="grid lg:grid-cols-2 gap-6 mb-8">

          {/* IMAGE PREVIEW */}

          <div className="border border-slate-800 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-4">
              Uploaded Image
            </h2>

            <div className="h-72 bg-slate-900 rounded-lg overflow-hidden flex items-center justify-center">

              {imagePreview ? (
                <img
                  src={imagePreview}
                  alt="preview"
                  className="max-h-full max-w-full object-contain"
                />
              ) : (
                <span className="text-slate-500">
                  Image preview will appear here
                </span>
              )}

            </div>

          </div>

          {/* RAW OCR */}

          <div className="border border-slate-800 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-4">
              Extracted Text
            </h2>

            <div className="h-72 overflow-auto bg-slate-900 rounded-lg p-4 whitespace-pre-wrap text-sm leading-7">
              {rawText || "OCR output will appear here"}
            </div>

          </div>

        </div>

        <div className="grid lg:grid-cols-2 gap-6 mb-8">

          {/* REPAIRED */}

          <div className="border border-slate-800 rounded-xl p-6">

            <div className="flex items-center justify-between mb-4">

              <h2 className="text-xl font-semibold">
                Cleaned Text
              </h2>

              {repairedText && (
                <button
                  onClick={copyRepairedText}
                  className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg text-sm"
                >
                  Copy Text
                </button>
              )}

            </div>

            <div className="h-72 overflow-auto bg-slate-900 rounded-lg p-4 whitespace-pre-wrap text-sm leading-7">
              {repairedText || "Repaired output will appear here"}
            </div>

          </div>

          {/* STRUCTURED */}

          <div className="border border-slate-800 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-4">
              Structured Output
            </h2>

            <div className="h-72 overflow-auto bg-slate-900 rounded-lg p-4 text-sm leading-7">

              {structuredData?.blocks?.length ? (
                structuredData.blocks.map(
                  (
                    block: any,
                    index: number
                  ) => (
                    <div
                      key={index}
                      className="mb-4 border-l-4 border-green-500 pl-3"
                    >
                      <span className="inline-block px-2 py-1 bg-green-950 text-green-300 rounded text-xs font-semibold mr-2">
                        {block.type}
                      </span>

                      <span>
                        {block.text}
                      </span>
                    </div>
                  )
                )
              ) : (
                <p className="text-slate-500">
                  Structured output will appear here
                </p>
              )}

            </div>

          </div>

        </div>

        {/* ANALYTICS */}

        {structuredData && (
          <div className="border border-slate-800 rounded-xl p-6 mb-8">

            <h2 className="text-2xl font-semibold mb-5">
              Document Analytics
            </h2>

            {analysis?.summary && (
              <div className="border border-slate-800 rounded-xl p-6 mb-8">

                <h2 className="text-2xl font-semibold mb-4">
                  AI Summary
                </h2>

                <div className="bg-slate-900 rounded-lg p-5 leading-7">

                  {smartSummary || analysis?.summary}

                </div>

              </div>
            )}
            <div className="grid md:grid-cols-4 gap-4">

              <div className="bg-slate-900 rounded-lg p-4">
                <p className="text-slate-400 text-sm">
                  Document Type
                </p>

                <p className="text-xl font-bold mt-2">
                  {structuredData.document_type || "Unknown"}
                </p>
              </div>

              <div className="bg-slate-900 rounded-lg p-4">
                <p className="text-slate-400 text-sm">
                  Word Count
                </p>

                <p className="text-xl font-bold mt-2">
                  {analysis?.word_count || 0}
                </p>
              </div>

              <div className="bg-slate-900 rounded-lg p-4">
                <p className="text-slate-400 text-sm">
                  Read Time
                </p>

                <p className="text-xl font-bold mt-2">
                  {analysis?.estimated_read_time || "0 min"}
                </p>
              </div>

            </div>

          </div>
        )}

        {/* EXPORT */}

        {structuredData && (
          <div className="border border-slate-800 rounded-xl p-6">

            <h2 className="text-2xl font-semibold mb-5">
              Export Document
            </h2>

            <div className="flex gap-4 flex-wrap">

              <button
                onClick={() =>
                  exportFile("markdown")
                }
                className="bg-slate-800 hover:bg-slate-700 px-5 py-3 rounded-lg"
              >
                Download Markdown
              </button>

              <button
                onClick={() =>
                  exportFile("docx")
                }
                className="bg-slate-800 hover:bg-slate-700 px-5 py-3 rounded-lg"
              >
                Download DOCX
              </button>

              <button
                onClick={() =>
                  exportFile("pdf")
                }
                className="bg-slate-800 hover:bg-slate-700 px-5 py-3 rounded-lg"
              >
                Download PDF
              </button>

              <button
                onClick={exportJSON}
                className="bg-slate-800 hover:bg-slate-700 px-5 py-3 rounded-lg"
              >
                Download JSON
              </button>

            </div>

          </div>
        )}

      </div>

      <footer className="mt-16 text-center text-slate-500 text-sm border-t border-slate-800 pt-6">
        Structify AI • Turn messy OCR text into structured documents
      </footer>

      {
        toast && (
          <div className="fixed bottom-5 right-5 bg-green-600 px-5 py-3 rounded-lg shadow-lg z-50">
            {toast}
          </div>
        )
      }

    </main >
  );
}
