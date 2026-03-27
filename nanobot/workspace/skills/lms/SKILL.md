# LMS Skills

You have access to the LMS (Learning Management System) backend through MCP tools. This skill guide teaches you how to use these tools effectively.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `lms_health` | Check if the LMS backend is healthy and report item count | None |
| `lms_labs` | List all labs available in the LMS | None |
| `lms_learners` | List all learners registered in the LMS | None |
| `lms_pass_rates` | Get pass rates (avg score and attempt count per task) for a lab | `lab` (required): Lab identifier |
| `lms_timeline` | Get submission timeline (date + submission count) for a lab | `lab` (required): Lab identifier |
| `lms_groups` | Get group performance (avg score + student count per group) for a lab | `lab` (required): Lab identifier |
| `lms_top_learners` | Get top learners by average score for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | `lab` (required): Lab identifier |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline. May take a moment. | None |

## How to Use These Tools

### When the user asks about available labs
Call `lms_labs` first to get the list of labs. This gives you the lab IDs and titles.

### When the user asks about a specific lab's performance
1. If the user specifies a lab (e.g., "Show me Lab 02 scores"), use that lab ID directly
2. If the user does NOT specify a lab (e.g., "Show me the scores"), respond by:
   - First calling `lms_labs` to get available labs
   - Then asking the user which lab they want to see, OR listing the available labs and offering to show data for any of them

### When comparing labs
Call `lms_labs` first, then call the relevant tool (e.g., `lms_pass_rates`, `lms_completion_rate`) for each lab to gather comparison data.

### Formatting responses
- **Percentages**: Format as "X%" (e.g., "67.3%" not "0.673")
- **Scores**: Round to one decimal place (e.g., "56.2" not "56.234567")
- **Counts**: Use plain numbers (e.g., "127 students" not "127.0 students")
- **Tables**: Use markdown tables for comparing multiple labs or items

### Response style
- Keep responses **concise** but informative
- Lead with the answer, then provide supporting details
- Offer follow-up actions (e.g., "Would you like to see the timeline for this lab?")

## Example Interactions

### User: "What can you do?"
Respond with:
> I can help you explore data from the LMS backend. Here's what I can do:
> - List available labs and learners
> - Show pass rates, completion rates, and submission timelines for any lab
> - Identify top performers and group performance
> - Check system health
> 
> Just ask me about a specific lab or say "what labs are available?" to get started.

### User: "Show me the scores" (no lab specified)
Respond with:
> Which lab would you like to see scores for? Here are the available labs:
> - Lab 01 – Products, Architecture & Roles
> - Lab 02 — Run, Fix, and Deploy a Backend Service
> - ...
> 
> Or I can show you pass rates, completion rates, or group performance.

### User: "Which lab has the lowest pass rate?"
1. Call `lms_labs` to get all labs
2. Call `lms_pass_rates` for each lab
3. Compare and identify the lowest
4. Present the answer with supporting data

### User: "Who are the top 3 students in Lab 04?"
Call `lms_top_learners` with `lab="lab-04"` (or the appropriate ID) and `limit=3`.

## Important Notes

- Always use the actual lab ID from `lms_labs` when calling tools that require a `lab` parameter
- If a tool returns an error, explain what went wrong and suggest an alternative
- The LMS backend is the source of truth — don't hallucinate data
