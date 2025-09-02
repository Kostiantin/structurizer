import React, { useState, useRef } from 'react';
import axios from 'axios';
import MermaidChart from './MermaidChart';
import 'bootstrap/dist/css/bootstrap.min.css';
import './DemoForm.css';
import meeting from '../assets/meeting3.jpeg';

const DemoForm = () => {
    const [text, setText] = useState('');
    const [summary, setSummary] = useState('');
    const [tasks, setTasks] = useState('');
    const [diagram, setDiagram] = useState('');
    const [loadingSummary, setLoadingSummary] = useState(false);
    const [loadingDiagram, setLoadingDiagram] = useState(false);
    const [loadingTasks, setLoadingTasks] = useState(false);
    const [error, setError] = useState('');
    const [tooltip, setTooltip] = useState({ message: '', visible: false });

    const diagramRef = useRef(null);

    const handleSubmit = async () => {
        setError('');
        setSummary('');
        setDiagram('');
        setTasks('');

        try {
            // Summarization
            setLoadingSummary(true);
            const summaryRes = await axios.post('http://localhost:8000/summarize/', { text });
            setSummary(summaryRes.data.summary);
            setLoadingSummary(false);

            // Diagram
            setLoadingDiagram(true);
            const diagramRes = await axios.post('http://localhost:8000/diagrams/', { text, diagram_type: 'flowchart' });
            setDiagram(diagramRes.data.diagram);
            setLoadingDiagram(false);

            // Tasks
            setLoadingTasks(true);
            const tasksRes = await axios.post('http://localhost:8000/tasks/', { text });
            setTasks(tasksRes.data.tasks);
            setLoadingTasks(false);
        } catch (err) {
            const errorMessage = err.response?.data?.detail || err.message;
            setError(`Error: ${errorMessage}`);
            console.error('Error in TaskFlowAI demo:', err, err.response?.data);
            setLoadingSummary(false);
            setLoadingDiagram(false);
            setLoadingTasks(false);
        }
    };

    const showTooltip = (message) => {
        setTooltip({ message, visible: true });
        setTimeout(() => setTooltip({ message: '', visible: false }), 2000); // hide after 2s
    };

    const copyToClipboard = (content) => {
        navigator.clipboard.writeText(content).then(() => {
            showTooltip("Copied!");
        });
    };

    const downloadDiagram = () => {
        if (!diagramRef.current) return;
        const svgEl = diagramRef.current.querySelector("svg");
        if (!svgEl) return;

        const svgData = new XMLSerializer().serializeToString(svgEl);
        const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = "diagram.svg";
        link.click();

        URL.revokeObjectURL(url);
        showTooltip("SVG Downloaded!");
    };

    return (
        <div className="container my-5">
            {/* Header */}
            <div className="text-center mb-6">
                <h1 className="app-logo">Structurizer</h1>
                <p className="lead over-image-text">
                    Structurizer helps you turn long, unorganized text into clear, actionable insights.
                    Perfect for meeting transcripts, brainstorming notes, sprint planning sessions, or project updates — it automatically creates concise summaries, visual workflow diagrams, and task lists so teams can stay aligned and productive.
                </p>
                <div className="meeting-image-holder">
                    <img src={meeting} alt="meeting" className="meeting-image"/>
                </div>
            </div>

            {/* Input Form */}
            <div className="card shadow-sm p-4 mb-6">
                <h4 className="mb-3">Enter Your Workshop / Plan</h4>
                <textarea
                    className="form-control mb-3"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="E.g., Sprint planning: Assign UI tasks to Alice, backend to Bob, deadline in 2 weeks."
                    rows={5}
                />
                <button
                    className="btn btn-primary w-100"
                    onClick={handleSubmit}
                    disabled={loadingSummary || loadingDiagram || loadingTasks}
                >
                    {loadingSummary || loadingDiagram || loadingTasks ? "Processing..." : "Generate Plan"}
                </button>
                {error && <div className="alert alert-danger mt-3">{error}</div>}
            </div>

            {/* Results */}
            <div className="row">
                {/* Summary */}
                <div className="col-md-12 mb-6">
                    <div className={`card h-100 shadow-sm p-3 ${summary ? 'has-content' : ''}`}>
                        <div className="d-flex justify-content-between align-items-center">
                            <h5 className="card-title">Sprint Summary</h5>
                            {summary && (
                                <button className="btn btn-sm btn-outline-secondary copy-btn"
                                        onClick={() => copyToClipboard(summary)}>
                                    Copy
                                </button>
                            )}
                        </div>
                        {loadingSummary ? <p className="text-muted">Loading summary...</p> : <p>{summary}</p>}
                    </div>
                </div>

                {/* Diagram */}
                <div className="col-md-12 mb-6">
                    <div className={`card h-100 shadow-sm p-3 ${diagram ? 'has-content' : ''}`} ref={diagramRef}>
                        <div className="d-flex justify-content-between align-items-center">
                            <h5 className="card-title">Workflow Diagram</h5>
                            {diagram && (
                                <button className="btn btn-sm btn-outline-secondary copy-btn"
                                        onClick={downloadDiagram}>
                                    Download
                                </button>
                            )}
                        </div>
                        {loadingDiagram ? (
                            <p className="text-muted">Loading diagram...</p>
                        ) : diagram && typeof diagram === 'string' && diagram.trim() ? (
                            <MermaidChart chart={diagram} />
                        ) : (
                            <p className="text-muted"></p>
                        )}
                    </div>
                </div>

                {/* Tasks */}
                <div className="col-md-12 mb-6">
                    <div className={`card h-100 shadow-sm p-3 ${tasks ? 'has-content' : ''}`}>
                        <div className="d-flex justify-content-between align-items-center">
                            <h5 className="card-title">Task List</h5>
                            {tasks && (
                                <button className="btn btn-sm btn-outline-secondary copy-btn"
                                        onClick={() => copyToClipboard(tasks)}>
                                    Copy
                                </button>
                            )}
                        </div>
                        {loadingTasks ? <p className="text-muted">Loading tasks...</p> : <pre>{tasks}</pre>}
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-lg-12 col-12">
                    <div className="author-me">
                        made by <a className="author-name" href="https://www.linkedin.com/in/kostiantyn-zavizion/"
                                   target="_blank">Kostiantyn Zavizion</a>
                    </div>
                </div>
            </div>

            {/* Tooltip */}
            {tooltip.visible && (
                <div className="tooltip-popup">
                    {tooltip.message}
                </div>
            )}
        </div>
    );
};

export default DemoForm;
