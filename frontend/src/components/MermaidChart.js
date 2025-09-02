import React, { useEffect, useRef } from "react";

const MermaidChart = ({ chart }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!chart || typeof chart !== "string" || !chart.trim()) {
      console.error("Invalid chart data: chart must be a non-empty string", chart);
      if (containerRef.current) {
        containerRef.current.innerHTML = "<p>Invalid diagram data</p>";
      }
      return;
    }

    let isMounted = true;

    const renderMermaid = async () => {
      try {
        const mermaidModule = await import("mermaid/dist/mermaid.esm.min.mjs");
        const mermaid = mermaidModule.default || mermaidModule;

        if (!containerRef.current) return;

        mermaid.initialize({
          startOnLoad: false,
          theme: "default",
          flowchart: { useMaxWidth: true },
          securityLevel: "strict" // inline styles, avoids external resource CORS issues
        });

        const chartId = "mermaid-" + Math.floor(Math.random() * 1000000);
        const { svg } = await mermaid.render(chartId, chart);
        if (isMounted && containerRef.current) {
          containerRef.current.innerHTML = svg;
        }
      } catch (err) {
        console.error("Mermaid render error:", err.message, chart);
        if (isMounted && containerRef.current) {
          containerRef.current.innerHTML = `<p>Error rendering diagram: ${err.message}</p>`;
        }
      }
    };

    renderMermaid();

    return () => {
      isMounted = false;
    };
  }, [chart]);

  return <div ref={containerRef}></div>;
};

export default MermaidChart;
