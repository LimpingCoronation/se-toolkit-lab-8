# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**

The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks:

```
Perceive → Reason → Act → Observe → (repeat)
```

**The 4 Steps:**
1. **Perceive** — Gather information (user input, tool outputs, file contents, system state)
2. **Reason** — Analyze the situation, plan next steps, select appropriate tools
3. **Act** — Execute decisions (call tools, modify files, send messages)
4. **Observe** — Receive feedback (results, errors, new state)

Then the loop repeats until the goal is achieved.

**Why It Matters:**
- Autonomy — Agents work without constant human guidance
- Adaptability — Agents adjust based on outcomes
- Multi-step reasoning — Complex tasks broken into iterative steps
- Error recovery — Agents detect and respond to failures

**Question: "What labs are available in our LMS?"** (before MCP tools)

The bare agent read the task files from its workspace and listed the labs from the markdown files, not from the LMS backend. This shows the agent has no tools yet — it can only use its training data and read workspace files.

## Task 1B — Agent with LMS tools

**Question: "What labs are available?"** (with MCP tools)

The agent now calls the LMS backend via MCP and returns real data:

```
Based on the LMS backend, here are the available labs:

 ID  Lab Title                                               
 ─────────────────────────────────────────────────────────── 
 1   Lab 01 – Products, Architecture & Roles                 
 2   Lab 02 — Run, Fix, and Deploy a Backend Service         
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy 
 4   Lab 04 — Testing, Front-end, and AI Agents              
 5   Lab 05 — Data Pipeline and Analytics Dashboard          
 6   Lab 06 — Build Your Own Agent                           
 7   Lab 07 — Build a Client with an AI Coding Agent         
 8   lab-08 (Current)                                        
```

**Question: "Which lab has the lowest pass rate?"**

The agent chained multiple MCP tool calls (`lms_labs` + `lms_pass_rates` for each lab) and identified:

> Lab 02 has the lowest pass rate with an average score of ~48.3 across all tasks.
> The biggest struggle point is "Optional 2: Make your VM a proxy" with a 0.0% average score (3 attempts, all failed).

## Task 1C — Skill prompt

**Question: "Show me the scores"** (without specifying a lab)

With the skill prompt, the agent now asks for clarification instead of hallucinating:

```
I can show you scores for a specific lab. Which lab would you like to see?

Available options:

 • lab-01 — Products, Architecture & Roles                             
 • lab-02 — Run, Fix, and Deploy a Backend Service                     
 • lab-03 — Backend API: Explore, Debug, Implement, Deploy             
 • lab-04 — Testing, Front-end, and AI Agents                          
 • lab-05 — Data Pipeline and Analytics Dashboard                      
 • lab-06 — Build Your Own Agent                                       
 • lab-07 — Build a Client with an AI Coding Agent                     
 • lab-08 — Current lab                                                

Score types I can show:

 • Pass rates — Average score and attempts per task                    
 • Group performance — Average score by student group                  
 • Top learners — Highest scoring students                             
 • Completion rate — % of students who passed                          

Just tell me which lab (e.g., "lab-04" or "lab 4") and I'll pull up the scores!
```

The skill prompt teaches the agent to:
- Ask which lab when the user doesn't specify one
- List available labs and score types
- Format responses concisely with clear options

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
