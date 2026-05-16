# IntelliTutor AI

An advanced **Multi-Agent AI Educational Assistant** built using **FastAPI**, **LangChain**, and **LangGraph** that intelligently generates quizzes, evaluates student answers, and orchestrates AI workflows using a centralized routing architecture with Human-in-the-Loop (HITL) support.

The platform is designed using an Agentic AI architecture where a central Route Agent manages the complete workflow and dynamically decides how requests should be processed.

---

# Table of Contents

- Introduction
- Features
- System Architecture
- Technologies Used
- Workflow Architecture
- Agents Used
- Request Flow
- Folder Structure
- Installation Guide
- UV Package Manager Setup
- Environment Variables
- Database Setup
- Running the Application
- API Documentation
- Request & Response Examples
- Human-in-the-Loop (HITL)
- LangGraph Workflow
- Future Enhancements
- License

---

# Introduction

IntelliTutor AI is an intelligent educational backend platform capable of:

- generating quizzes dynamically
- evaluating student answers
- calculating assessment scores
- providing AI-generated feedback
- managing AI workflows using multiple agents

The project demonstrates modern Agentic AI concepts using:
- LangChain
- LangGraph
- FastAPI
- PostgreSQL
- Multi-Agent Systems

The entire workflow is controlled by a centralized Route Agent that identifies user intent and routes requests to the correct AI workflow.

---

# Core Features

## AI Features

- Multi-Agent AI Architecture
- Intelligent Quiz Generation
- Multiple Choice Questions (MCQs)
- AI-Based Answer Evaluation
- Assessment Score Calculation
- Percentage-Based Result Analysis
- Question-Wise Feedback Generation
- Context-Aware Intent Detection
- Out-of-Context Query Handling
- Human-in-the-Loop Workflow
- Stateful Memory System

---

## Backend Features

- FastAPI REST APIs
- Async Backend Architecture
- PostgreSQL Integration
- Modular API Design
- Scalable Service Structure
- LangGraph Workflow Orchestration
- Structured Error Handling

---

# System Architecture

```text
                           ┌───────────────────┐
                           │       User        │
                           └─────────┬─────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │      FastAPI API       │
                        └──────────┬─────────────┘
                                   │
                                   ▼
                        ┌────────────────────────┐
                        │      Route Agent       │
                        │  (Intent Detection)    │
                        └───────┬───────┬────────┘
                                │       │
                   Quiz Intent  │       │ Out-of-Context
                                │       │
                                ▼       ▼
                    ┌────────────────┐  ┌──────────────────┐
                    │   Quiz Agent   │  │ Direct AI Reply  │
                    └───────┬────────┘  └──────────────────┘
                            │
                            ▼
                 ┌────────────────────────┐
                 │   Review Evaluation    │
                 │   Workflow Processing  │
                 └──────────┬─────────────┘
                            ▼
                 ┌────────────────────────┐
                 │ LangGraph Orchestration│
                 └──────────┬─────────────┘
                            ▼
                 ┌────────────────────────┐
                 │ PostgreSQL Memory DB   │
                 └────────────────────────┘
```

---

# Workflow Architecture

The system follows a centralized routing workflow.

## Important Workflow Logic

### Route Agent is the Main Controller

Every request first goes to the Route Agent.

The Route Agent:
- analyzes user intent
- validates request context
- decides workflow direction
- routes requests to the proper AI system

---

# Request Flow

## Quiz Generation Flow

```text
User Request
      ↓
FastAPI API
      ↓
Route Agent
      ↓
Quiz Agent
      ↓
MCQ Generation
      ↓
User Attempts Quiz
      ↓
Answer Evaluation
      ↓
Assessment Score
      ↓
Percentage + Feedback
```

---

# Out-of-Context Handling

If the user asks unrelated questions:

Example:
```text
"Who is the president?"
```

The Route Agent:
- identifies it as out-of-context
- does NOT send request to Quiz Agent
- directly responds to user

This prevents unnecessary AI workflow execution.

---

# Agents Used

# 1. Route Agent

## Purpose

Acts as the central intelligence controller of the system.

## Responsibilities

- Intent Detection
- Context Validation
- Workflow Routing
- Out-of-Context Detection
- AI Response Coordination

## Workflow

```text
User Input
     ↓
Intent Analysis
     ↓
Decision Making
     ↓
Route to Correct Workflow
```

## Example

### Input
```json
{
"topics":"What is Python?"
"difficulty_level":"medium"
}
```

### Output
```text
Routed to Quiz Agent
```

---

# 2. Quiz Agent

## Purpose

Generates intelligent multiple-choice quizzes dynamically.

## Responsibilities

- Generate MCQs
- Generate Options
- Create Correct Answers
- Difficulty-Based Questions
- Educational Content Generation

---

## Example Quiz Format

```json
{
  "question": "What is Python?",
  "options": [
    "A)Programming Language",
    "B)Database",
    "C)Operating System",
    "D)Browser"
  ]
}
```

---

# 3. Review & Assessment Workflow

## Purpose

Evaluates user-selected options and generates assessment results.

## Responsibilities

- Compare user answers
- Calculate score
- Generate percentage
- Provide question-wise feedback
- Generate final assessment report

---

# Assessment Features

The system generates:

- Total Score
- Percentage
- Correct Answers Count
- Wrong Answers Count
- Individual Feedback
- Performance Summary

---

# Example Assessment Response

```json
{
  "score": 8,
  "total_questions": 10,
  "percentage": 80,
  "feedback": [
    {
      "question": "What is Python?",
      "status": "Correct",
      "feedback": "Good understanding of basics."
    },
    {
      "question": "What is OOP?",
      "status": "Wrong",
      "feedback": "Review OOP concepts again."
    }
  ]
}
```

---

# Technologies Used

## Programming Language

- Python

---

## Backend Framework

- FastAPI

---

## AI Frameworks

- LangChain
- LangGraph

---

## Database

- PostgreSQL

---

## AI Concepts

- Agentic AI
- Multi-Agent Systems
- Human-in-the-Loop (HITL)
- Intent Detection
- Workflow Orchestration
- AI Routing Systems
- Stateful AI Workflows

---

# Folder Structure

```text
IntelliTutor-AI/
│
├── app/
│   │
│   ├── agents/
│   │   ├── route_agent.py
│   │   ├── quiz_agent.py
│   │   └── review_agent.py
│   │
│   ├── routes/
│   │   └── outes.py
│   │
│   ├── services/
│   │   └── chat_service.py
│   │
│   ├── database/
│   │   └── db.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── config/
│   │   └── settings.py
|   |
|   |── tools/
|   |    └── tools.py
│   │
│   ├── utils/
│   │   └── helper.py
|   |   └── logger.py
|   |   └── api_response.py
│   │
│   └── main.py
│
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .env
├── README.md
└── Dockerfile
```

---

# Installation Guide

# Method 1 — Using UV (Recommended)

UV is a modern ultra-fast Python package manager.

---

# Step 1 — Install UV

## Windows

```bash
pip install uv
```

---

## Mac/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

# Step 2 — Clone Repository

```bash
git clone https://github.com/your-username/intellitutor-ai.git
```

---

# Step 3 — Navigate to Project

```bash
cd intellitutor-ai
```

---

# Step 4 — Create Virtual Environment

```bash
uv venv
```

---

# Step 5 — Activate Virtual Environment

## Windows

```bash
.venv\Scripts\activate
```

---

## Linux/Mac

```bash
source .venv/bin/activate
```

---

# Step 6 — Install Dependencies

```bash
uv sync
```

---

# Alternative Installation Using pip

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@localhost/intellitutor
```

---

# Database Setup

## Create PostgreSQL Database

```sql
CREATE DATABASE intellitutor;
```

---

# Running the Application

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# API Request Examples

# Generate Quiz

## Endpoint

```http
POST /api/v1/chat
```

---

## Request Body

```json
{
  "topic": "Python",
  "difficulty": "medium",
  "number_of_questions": 5
}
```

---

## Response

```json
{
  "quiz": [
    {
      "question": "What is Python?",
      "options": [
        "Programming Language",
        "Browser",
        "Database",
        "Operating System"
      ]
    }
  ]
}
```

---

# Submit Quiz Answers

## Terminal Level

```text
User Enters a list of answers
```
---

## Response

```json
{
  "score": 4,
  "total_questions": 5,
  "percentage": 80,
  "feedback": [
    {
      "question": "What is Python?",
      "status": "Correct",
      "feedback": "Excellent answer."
    }
  ]
}
```

---

# LangGraph Workflow

LangGraph is used for:

- Agent orchestration
- Conditional routing
- Stateful execution
- Workflow persistence
- Human approval checkpoints
- Multi-agent coordination

---

# Human-in-the-Loop (HITL)

The system integrates Human-in-the-Loop middleware to improve:
- reliability
- safety
- controlled execution
- workflow validation

---

# Key Concepts Implemented

- Agentic AI
- Multi-Agent Collaboration
- AI Intent Routing
- Educational AI Systems
- LangGraph Workflow Management
- AI-Based Assessment Systems
- MCQ Evaluation Engine
- Backend API Development
- PostgreSQL Memory Persistence

---


# Author

## Lokesh Sankar

Backend Developer | Agentic AI Developer | FastAPI Developer

---
