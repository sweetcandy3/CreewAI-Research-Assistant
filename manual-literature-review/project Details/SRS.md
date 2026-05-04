# Software Requirements Specification (SRS)
## InSight Forge — AI-Powered Academic Literature Review & Research Assistant

**Version:** 1.0  
**Date:** May 4, 2026  
**Project:** InSight Forge  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Specific Requirements](#3-specific-requirements)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [System Features](#5-system-features)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Use Cases](#7-use-cases)
8. [Data Requirements](#8-data-requirements)
9. [Constraints & Assumptions](#9-constraints--assumptions)
10. [Appendices](#10-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document provides a complete description of the functional and non-functional requirements for **InSight Forge**, an AI-powered academic literature review and research assistant. It is intended for developers, testers, project stakeholders, and academic users who will interact with or contribute to the system.

### 1.2 Scope

InSight Forge is a web-based research assistant that leverages agentic AI to conduct deep, PhD-level literature reviews on any topic. The system:

- Searches the web for real-time academic and research information using the Exa AI API
- Analyzes user-uploaded PDF research papers
- Synthesizes findings into structured, publication-ready Markdown reports
- Supports multiple LLM providers (OpenAI, GROQ, Ollama)

The system is deployed as a Streamlit web application and targets researchers, students, and academics who need comprehensive literature reviews.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|-----------|
| **LLM** | Large Language Model — an AI model capable of understanding and generating text |
| **CrewAI** | An agentic AI orchestration framework for building autonomous AI agents |
| **Exa AI** | A neural search API that provides web-based research with citation support |
| **Ollama** | A local LLM inference platform for running models offline |
| **GROQ** | A cloud-based LLM inference provider with high-speed model serving |
| **PDF** | Portable Document Format — a standard file format for documents |
| **API** | Application Programming Interface |
| **SRS** | Software Requirements Specification |
| **UI** | User Interface |

### 1.4 References

- [CrewAI Documentation](https://docs.crewai.com)
- [Exa AI API Documentation](https://docs.exa.ai)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Ollama Documentation](https://ollama.com)
- IEEE 830-1998 — Recommended Practice for Software Requirements Specifications

### 1.5 Overview

The remainder of this document covers the overall product description, detailed functional and non-functional requirements, external interfaces, use cases, data requirements, and system constraints.

---

## 2. Overall Description

### 2.1 Product Perspective

InSight Forge is a standalone web application that integrates three main external systems:

1. **LLM Providers** — OpenAI, GROQ, or Ollama for natural language understanding and generation
2. **Exa AI** — For real-time web-based research and citation retrieval
3. **CrewAI Framework** — For orchestrating the AI research agent and managing task execution

The system operates as a single-page Streamlit application with a sidebar for configuration and a main content area for input and results.

### 2.2 Product Functions

The system provides the following high-level functions:

- **F1:** Accept and process natural-language research queries
- **F2:** Upload and analyze multiple PDF research papers
- **F3:** Conduct automated web research using Exa AI
- **F4:** Generate structured, publication-quality research reports
- **F5:** Display real-time progress of the AI agent's work
- **F6:** Support multiple LLM providers and models
- **F7:** Allow download of generated reports in Markdown format

### 2.3 User Classes and Characteristics

| User Class | Description | Technical Proficiency |
|------------|-------------|----------------------|
| **Academic Researchers** | PhD students, postdocs, professors conducting literature reviews | Moderate |
| **Graduate Students** | Students needing research summaries for coursework or thesis | Low to Moderate |
| **Industry Professionals** | R&D professionals needing state-of-the-art surveys | Moderate |
| **Developers** | Contributors who maintain or extend the system | High |

### 2.4 Operating Environment

- **Client:** Any modern web browser (Chrome, Firefox, Safari, Edge)
- **Server:** Python 3.10+ runtime environment
- **Network:** Internet access required for OpenAI, GROQ, and Exa API access; Ollama runs locally
- **OS:** Linux, macOS, or Windows (with Python support)

### 2.5 Design and Implementation Constraints

- The application must run within Streamlit's execution model (re-run on interaction)
- PDF text extraction is limited to text-based PDFs (scanned/image-only PDFs are not supported)
- PDF content is truncated to 12,000 characters per file to stay within LLM context limits
- Ollama provider disables web search functionality due to limited function-calling support
- API keys are stored in-memory only (session-scoped, not persisted)

### 2.6 Assumptions and Dependencies

- Users have valid API keys for their chosen provider (OpenAI/GROQ) and Exa
- The Exa AI answer API endpoint (`https://api.exa.ai/answer`) is available and operational
- For Ollama usage, users have a locally running Ollama instance with pre-downloaded models
- The `pysqlite3-binary` package resolves ChromaDB SQLite compatibility issues
- Internet connectivity is available for cloud-based LLM providers

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### FR-01: Research Query Input
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-01 |
| **Description** | The system shall provide a text input area for users to enter their research query |
| **Input** | Free-text research query (string) |
| **Default Value** | "Research the latest AI Agent news in February 2025 and summarize each." |
| **Priority** | High |
| **Acceptance Criteria** | User can type a research query of any length into a multi-line text area |

#### FR-02: PDF Upload & Analysis
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-02 |
| **Description** | The system shall allow users to upload one or more PDF research papers for analysis |
| **Input** | One or more `.pdf` files |
| **Processing** | Files are saved to temporary storage; text is extracted using `pypdf`; content is truncated to 12,000 characters per PDF |
| **Priority** | High |
| **Acceptance Criteria** | Uploaded PDFs are readable by the AI agent; extracted text is incorporated into the research analysis |

#### FR-03: Multi-Provider LLM Support
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-03 |
| **Description** | The system shall support three LLM providers: OpenAI, GROQ, and Ollama |
| **OpenAI Models** | `gpt-4o-mini`, `gpt-4o`, `o1`, `o1-mini`, `o1-preview`, `o3-mini`, Custom |
| **GROQ Models** | `qwen-2.5-32b`, `deepseek-r1-distill-qwen-32b`, `deepseek-r1-distill-llama-70b`, `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, Custom |
| **Ollama Models** | Dynamically populated from local Ollama instance |
| **Priority** | High |
| **Acceptance Criteria** | Each provider connects successfully and returns valid LLM responses |

#### FR-04: Web Research via Exa AI
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-04 |
| **Description** | The system shall use the Exa AI answer API to perform web-based research with citations |
| **API Endpoint** | `https://api.exa.ai/answer` |
| **Authentication** | `x-api-key` header with user-provided EXA API key |
| **Output** | Answer text with numbered citations (title + URL) |
| **Condition** | Web search is disabled when using Ollama provider |
| **Priority** | High |
| **Acceptance Criteria** | Exa API returns relevant answers with citations for the given query |

#### FR-05: Structured Report Generation
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-05 |
| **Description** | The system shall generate a structured academic research report in Markdown format |
| **Report Sections** | Executive Summary, Key Findings, In-Depth Analysis, Research Gaps & Future Directions, Critique and Comparison of Research, Conclusion, Sources |
| **Output File** | `output/research_report.md` |
| **Priority** | High |
| **Acceptance Criteria** | Generated report follows the defined template and contains substantive, well-sourced content |

#### FR-06: Real-Time Progress Display
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-06 |
| **Description** | The system shall display the AI agent's thought process and actions in real-time during research |
| **Implementation** | Custom stdout capture redirected to a scrollable Streamlit container |
| **Filtering** | ANSI escape codes, LiteLLM debug messages, and duplicate lines are removed |
| **Priority** | Medium |
| **Acceptance Criteria** | Users can observe the agent's progress live without the page freezing |

#### FR-07: Report Download
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-07 |
| **Description** | The system shall provide a download button for the generated research report |
| **File Format** | Markdown (`.md`) |
| **File Name** | `research_report.md` |
| **Priority** | Medium |
| **Acceptance Criteria** | Clicking the download button saves a correctly formatted Markdown file to the user's machine |

#### FR-08: Sidebar Configuration Panel
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-08 |
| **Description** | The system shall provide a sidebar with model selection, API key entry, and an about section |
| **Sections** | Model Selection, API Keys, About |
| **API Key Storage** | In-memory only (environment variables); cleared when browser is closed |
| **Priority** | High |
| **Acceptance Criteria** | Users can configure provider, model, and API keys without leaving the main page |

#### FR-09: Custom Model Input
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-09 |
| **Description** | The system shall allow users to enter a custom model string for OpenAI and GROQ providers |
| **Trigger** | Selecting "Custom" from the model dropdown |
| **Priority** | Low |
| **Acceptance Criteria** | Custom model string is passed correctly to the LLM provider |

#### FR-10: Ollama Model Discovery
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-10 |
| **Description** | The system shall automatically discover and list available models from a local Ollama instance |
| **API Endpoint** | `http://localhost:11434/api/tags` |
| **Fallback** | Display a warning message if Ollama is unreachable or no models are found |
| **Priority** | Medium |
| **Acceptance Criteria** | All locally available Ollama models appear in the dropdown; graceful failure when Ollama is offline |

#### FR-11: API Key Validation
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-11 |
| **Description** | The system shall validate that required API keys are provided before allowing research to begin |
| **Rules** | OpenAI requires OpenAI + Exa keys; GROQ requires GROQ + Exa keys; Ollama requires no keys |
| **Priority** | High |
| **Acceptance Criteria** | A warning message is displayed and research is blocked if required keys are missing |

#### FR-12: Error Handling
| Attribute | Detail |
|-----------|--------|
| **ID** | FR-12 |
| **Description** | The system shall gracefully handle errors during research execution |
| **Behavior** | Display an error message with the exception details; update the status indicator to "Error" state |
| **Priority** | High |
| **Acceptance Criteria** | Errors do not crash the application; users receive informative error messages |

---

## 4. External Interface Requirements

### 4.1 User Interfaces

| Interface | Description |
|-----------|-------------|
| **Main Page** | Centered title, research query text area, PDF uploader, "Start Research" button, results display area, download button |
| **Sidebar** | Collapsible panel with model selection (radio + dropdown), API key inputs (password-masked), and an "About" expander |
| **Status Indicator** | Expandable status widget showing "Researching..." during execution, "Research completed!" on success, or "Error occurred" on failure |
| **Progress Container** | Scrollable, bordered container (300px height) displaying the agent's real-time output |

### 4.2 Hardware Interfaces

- No specialized hardware required
- Standard computing hardware with internet connectivity (for cloud providers)
- GPU optional (only relevant for local Ollama inference performance)

### 4.3 Software Interfaces

| External System | Interface Type | Purpose |
|----------------|---------------|---------|
| **OpenAI API** | REST API (HTTPS) | LLM inference for text generation |
| **GROQ API** | REST API (HTTPS) | LLM inference for text generation |
| **Ollama** | REST API (HTTP, localhost:11434) | Local LLM inference and model discovery |
| **Exa AI API** | REST API (HTTPS) | Web search and answer retrieval with citations |
| **File System** | Local I/O | Temporary PDF storage, report output to `output/` directory |

### 4.4 Communication Interfaces

- **HTTP/HTTPS:** All external API communication uses HTTP(S) with JSON payloads
- **Authentication:** API keys transmitted via headers (`x-api-key` for Exa, `Authorization` for OpenAI/GROQ)
- **Local Communication:** Ollama communicates over HTTP on `localhost:11434`

---

## 5. System Features

### 5.1 SF-01: AI-Powered Research Agent

**Description:** A Senior Academic Research Analyst AI agent that autonomously conducts research using web search and PDF analysis tools.

**Stimulus/Response:**
| Stimulus | Response |
|----------|----------|
| User clicks "Start Research" | Agent is created with the selected LLM, executes the research task, and returns a structured report |

**Functional Requirements:**
- The agent shall have the role of "Senior Academic Research Analyst"
- The agent shall have access to two tools: EXA Answer Tool and PDF Analysis Tool
- The agent shall operate in a single-agent, sequential process (no delegation)
- The agent shall produce verbose output for real-time progress tracking

### 5.2 SF-02: Web Research Tool (Exa)

**Description:** An integrated tool that queries the Exa AI answer API to retrieve web-based research with citations.

**Functional Requirements:**
- The tool shall accept a natural-language query string
- The tool shall return the answer text followed by numbered citations
- Each citation shall include a title and URL
- The tool shall authenticate using the `EXA_API_KEY` environment variable

### 5.3 SF-03: PDF Analysis Tool

**Description:** An integrated tool that extracts and returns text content from uploaded PDF research papers.

**Functional Requirements:**
- The tool shall accept a file path to a PDF document
- The tool shall extract text from all pages using `pypdf.PdfReader`
- The tool shall truncate extracted text to 12,000 characters
- The tool shall return a descriptive error message on failure

### 5.4 SF-04: Real-Time Output Streaming

**Description:** A custom stdout capture mechanism that redirects the CrewAI agent's verbose output to the Streamlit UI.

**Functional Requirements:**
- The system shall replace `sys.stdout` during agent execution
- The system shall clean ANSI escape codes and LiteLLM debug messages from output
- The system shall deduplicate repeated output lines
- The system shall restore `sys.stdout` after execution completes

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| **NFR-01** | Application startup time | < 5 seconds |
| **NFR-02** | Sidebar rendering and interaction | < 1 second response time |
| **NFR-03** | PDF text extraction | < 3 seconds per PDF (for standard-length papers) |
| **NFR-04** | Report generation time | Dependent on LLM provider (typically 30 seconds – 5 minutes) |
| **NFR-05** | Real-time output update frequency | Updates display within 500ms of new agent output |

### 6.2 Usability Requirements

| ID | Requirement |
|----|-------------|
| **NFR-06** | The UI shall follow a clean, centered layout with clear visual hierarchy |
| **NFR-07** | All API key inputs shall be password-masked for privacy |
| **NFR-08** | The application shall provide contextual help text for all configuration options |
| **NFR-09** | Users shall be able to complete a full research workflow in ≤ 5 interactions (select provider → enter keys → type query → upload PDFs → click research) |
| **NFR-10** | Warning messages shall be displayed for missing configurations before the user can start research |

### 6.3 Security Requirements

| ID | Requirement |
|----|-------------|
| **NFR-11** | API keys shall be stored only in-memory as environment variables; they shall NOT be persisted to disk |
| **NFR-12** | API keys shall be transmitted over HTTPS (for cloud providers) |
| **NFR-13** | API key input fields shall use password masking (type="password") |
| **NFR-14** | No user data or research results shall be transmitted to third parties beyond the selected LLM and Exa providers |

### 6.4 Reliability Requirements

| ID | Requirement |
|----|-------------|
| **NFR-15** | The system shall gracefully handle API failures (network errors, invalid keys, rate limits) without crashing |
| **NFR-16** | The system shall gracefully handle Ollama being offline (display warning, allow other providers) |
| **NFR-17** | The system shall handle malformed or unreadable PDF files with descriptive error messages |
| **NFR-18** | The stdout capture mechanism shall always restore original stdout, even on exceptions |

### 6.5 Compatibility Requirements

| ID | Requirement |
|----|-------------|
| **NFR-19** | The application shall be compatible with Python 3.10 and above |
| **NFR-20** | The application shall work in Chrome, Firefox, Safari, and Edge browsers |
| **NFR-21** | The `pysqlite3-binary` patching shall handle ChromaDB's SQLite dependency transparently |

### 6.6 Scalability Requirements

| ID | Requirement |
|----|-------------|
| **NFR-22** | The system shall support uploading and analyzing multiple PDF files in a single research session |
| **NFR-23** | The system is designed for single-user, single-session operation (Streamlit's default model) |

---

## 7. Use Cases

### UC-01: Conduct a Web-Based Literature Review

| Attribute | Detail |
|-----------|--------|
| **Actor** | Researcher |
| **Preconditions** | User has valid API keys for the selected LLM provider and Exa |
| **Main Flow** | 1. User selects LLM provider and model in the sidebar<br>2. User enters API keys<br>3. User types a research query<br>4. User clicks "Start Research"<br>5. System creates the AI agent and executes the research task<br>6. System displays real-time progress<br>7. System displays the structured report<br>8. User downloads the report |
| **Postconditions** | A structured Markdown report is saved to `output/research_report.md` and available for download |
| **Alternative Flow** | If API keys are missing, a warning is displayed and research is blocked |

### UC-02: Analyze Uploaded PDF Papers

| Attribute | Detail |
|-----------|--------|
| **Actor** | Researcher |
| **Preconditions** | User has at least one PDF file to upload |
| **Main Flow** | 1. User uploads one or more PDF files via the file uploader<br>2. User types a research query<br>3. User clicks "Start Research"<br>4. System saves PDFs to temporary files<br>5. System appends PDF file paths to the task description<br>6. AI agent reads and incorporates PDF content into the analysis<br>7. System generates a report including insights from the PDFs |
| **Postconditions** | Report includes analysis of both web sources and uploaded PDFs |

### UC-03: Use Local Ollama Model for Offline Research

| Attribute | Detail |
|-----------|--------|
| **Actor** | Researcher (with Ollama installed locally) |
| **Preconditions** | Ollama is running locally with at least one model downloaded |
| **Main Flow** | 1. User selects "Ollama" as the provider<br>2. System queries local Ollama instance for available models<br>3. User selects a model from the dropdown<br>4. User types a research query<br>5. User clicks "Start Research"<br>6. System uses the local model (web search is disabled)<br>7. Report is generated based on the model's training data |
| **Postconditions** | A research report is generated without any internet-dependent API calls |
| **Alternative Flow** | If Ollama is offline or no models are found, a warning is displayed |

### UC-04: Use a Custom Model

| Attribute | Detail |
|-----------|--------|
| **Actor** | Advanced User |
| **Preconditions** | User knows a valid model string for their provider |
| **Main Flow** | 1. User selects OpenAI or GROQ as the provider<br>2. User selects "Custom" from the model dropdown<br>3. User enters a custom model string<br>4. User proceeds with the research workflow |
| **Postconditions** | The custom model is used for LLM inference |

---

## 8. Data Requirements

### 8.1 Input Data

| Data Item | Format | Source | Constraints |
|-----------|--------|--------|-------------|
| Research Query | Free-text string | User input | No length limit enforced by the UI |
| PDF Files | `.pdf` binary files | User upload | Must be text-based (not scanned images); content truncated to 12,000 chars |
| API Keys | String (password-masked) | User input | Must be valid keys for the respective provider |
| Provider Selection | Enum: OpenAI, GROQ, Ollama | User selection | — |
| Model Selection | String | User selection or input | Must be a valid model for the selected provider |

### 8.2 Output Data

| Data Item | Format | Destination | Description |
|-----------|--------|-------------|-------------|
| Research Report | Markdown (`.md`) | `output/research_report.md` + browser display + download | Structured academic report with 7 sections |
| Real-Time Agent Output | Plain text | Scrollable container in the Streamlit UI | Cleaned, deduplicated agent progress output |

### 8.3 Data Storage

- **Temporary:** Uploaded PDFs are saved to OS temp directory (`tempfile.NamedTemporaryFile`)
- **Persistent:** Research reports saved to `output/research_report.md` (overwritten each run)
- **In-Memory:** API keys stored as environment variables for the session duration only

---

## 9. Constraints & Assumptions

### 9.1 Constraints

1. Streamlit's execution model requires full script re-execution on each user interaction
2. PDF extraction is text-only — scanned or image-based PDFs will yield empty or minimal content
3. The Exa AI API has rate limits and usage quotas tied to the user's API key
4. LLM context windows limit the amount of information that can be processed in a single request
5. Ollama models have limited function-calling capabilities, restricting tool usage
6. The system is designed for single-user operation per Streamlit instance

### 9.2 Assumptions

1. Users have stable internet connectivity for cloud-based LLM and Exa API access
2. The Exa AI, OpenAI, and GROQ APIs maintain backward compatibility
3. Users understand the quality trade-offs between different LLM providers and models
4. The CrewAI framework maintains compatibility with the agent/task/crew API pattern

---

## 10. Appendices

### Appendix A: Dependency List

| Package | Version | Purpose |
|---------|---------|---------|
| `crewai` | Latest | Agentic AI framework |
| `crewai-tools` | Latest | Base tool classes |
| `streamlit` | Latest | Web UI framework |
| `exa-py` | Latest | Exa AI Python client |
| `requests` | Latest | HTTP client |
| `pysqlite3-binary` | Latest | SQLite compatibility |
| `PyMuPDF` | Latest | PDF processing |
| `pypdf` | Latest | PDF text extraction |
| `pydantic` | Latest | Data validation |

### Appendix B: API Endpoints

| API | Endpoint | Method | Purpose |
|-----|----------|--------|---------|
| Exa Answer | `https://api.exa.ai/answer` | POST | Web research with citations |
| Ollama Tags | `http://localhost:11434/api/tags` | GET | Discover local models |
| OpenAI | Via `crewai.LLM` abstraction | — | LLM inference |
| GROQ | Via `crewai.LLM` abstraction | — | LLM inference |
