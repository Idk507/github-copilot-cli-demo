
---

## 🗂️ Project: Simple FastAPI App

We'll build a **Task Manager API** with:
- `GET /tasks` — list all tasks
- `POST /tasks` — create a task
- `GET /tasks/{id}` — get a task by ID
- `DELETE /tasks/{id}` — delete a task

---

## Phase 1 — Setup & Authentication

### Step 1: Install Copilot CLI

```bash
# macOS
brew install github/gh/copilot

# Verify installation
copilot version
```

### Step 2: Authenticate

```bash
copilot login
```
> This opens a browser OAuth flow. After login, your token is stored securely. All future sessions use it automatically.

For CI or headless use later:
```bash
export COPILOT_GITHUB_TOKEN=github_pat_YOUR_TOKEN_HERE
```

---

## Phase 2 — Initialize the Project

### Step 3: Create your project folder and open it

```bash
mkdir fastapi-task-manager
cd fastapi-task-manager
git init
```

### Step 4: Initialize Copilot for this repo

```bash
copilot init
```

> This creates `.github/copilot-instructions.md` — a Markdown file where you describe your project to Copilot. It gets loaded automatically in every session inside this folder.

Edit `.github/copilot-instructions.md`:

```markdown
# Project: FastAPI Task Manager

This is a simple Python FastAPI REST API for managing tasks.
- Language: Python 3.11+
- Framework: FastAPI
- No database — use in-memory list for now
- Follow PEP8 conventions
- All routes under /tasks
- Use Pydantic models for request/response validation
- Include docstrings on all route handlers
```

> **Why this matters:** Every Copilot session in this project will read these instructions automatically, so you never have to re-explain the project context.

---

## Phase 3 — Interactive Mode (Chat + Build)

### Step 5: Launch an interactive session

```bash
copilot
```

You're now in the interactive terminal UI. You'll see the Copilot prompt. Let's name this session first:

```
/rename fastapi-task-manager-build
```

> `/rename` gives the session a meaningful name so you can `/resume` it later without hunting through a list.

---

### Step 6: Check your environment is loaded

```
/env
```

> This shows you what context Copilot has loaded — your custom instructions from `.github/copilot-instructions.md`, any MCP servers, skills, agents. Confirm your project instructions are listed.

---

### Step 7: Ask Copilot to scaffold the project structure

Type this prompt:

```
Create the folder structure and files for a simple FastAPI task manager app.
Include: main.py, models.py, routes/tasks.py, requirements.txt, and a .gitignore for Python.
Don't write any logic yet — just create the empty files with correct imports.
```

> Copilot will use the `create` and `write` tools. It will ask for permission before creating files — type `y` to allow each one, or type `allow all` to approve everything at once.

---

### Step 8: Check what was created

```
/diff
```

> `/diff` shows all file changes made so far in this session in a rich diff view. Confirm the structure looks right before moving on.

Also run this in your shell to see the tree:

```
! tree .
```

> The `!` prefix runs a shell command directly without going through the AI — it's an instant passthrough to your terminal.

---

### Step 9: Build the Pydantic models

```
Now write the Pydantic models in models.py.
Create a Task model with: id (int), title (str), description (str), done (bool, default False).
Also create a TaskCreate model without the id field for POST requests.
```

---

### Step 10: Build the routes

```
Now implement all four routes in routes/tasks.py:
- GET /tasks — return all tasks
- POST /tasks — create a task, auto-increment id
- GET /tasks/{task_id} — return task or 404
- DELETE /tasks/{task_id} — delete task or 404
Use the models from models.py. Store tasks in an in-memory list.
```

---

### Step 11: Wire up main.py

```
Now write main.py. Create the FastAPI app instance, include the tasks router, and add a root GET / endpoint that returns {"message": "Task Manager API is running"}.
```

---

### Step 12: Review context usage

```
/context
```

> Shows how full the context window is with a visual breakdown. On a small project like this it'll be light — but on bigger projects, run `/compact` when this fills up.

---

### Step 13: View the final diff before testing

```
/diff
```

Carefully review every file that was changed. If anything looks off, you can:

```
/undo
```

> `/undo` rolls back all file changes from the last AI turn — a clean, one-command rollback.

---

## Phase 4 — Switch to Autopilot Mode

Now that the structure and logic are in place, switch to autopilot to let Copilot handle the remaining tasks autonomously — testing, linting, and documentation.

### Step 14: Switch to autopilot with Shift+Tab

Press **`Shift+Tab`** to cycle through modes until you see `AUTOPILOT` in the UI indicator.

Or launch a new autopilot session directly from the terminal:

```bash
copilot --autopilot --allow-tool='shell(pip:*),shell(python:*),write,read' \
  -i "Do the following in order:
      1. Install dependencies from requirements.txt into a virtual environment
      2. Run the app with uvicorn and verify it starts without errors
      3. Write a test file tests/test_tasks.py using pytest and httpx
      4. Run the tests and fix any failures
      5. Add type hints to all functions in routes/tasks.py"
```

> **Flags explained:**
> - `--autopilot` — no confirmation prompts, Copilot runs the full chain autonomously
> - `--allow-tool='shell(pip:*),shell(python:*),write,read'` — whitelists only the tools it actually needs; pip installs, python runs, file reads/writes. Nothing else.
> - `-i` — inline prompt (alternative to `-p`; keeps stdin open for the session)

---

## Phase 5 — Programmatic Commands (Scripting & Automation)

### Step 15: Generate a README automatically (programmatic, silent)

```bash
copilot -p "Read all the Python files in this project and generate a professional README.md.
Include: project description, installation steps, how to run, all API endpoints with examples using curl." \
  --allow-tool='read,write' \
  --allow-all-paths \
  --silent \
  --no-ask-user
```

> **Flags explained:**
> - `-p` — programmatic prompt (no interactive UI, runs and exits)
> - `--silent` — outputs only the agent response, no stats or decoration
> - `--no-ask-user` — agent won't pause to ask clarifying questions
> - `--allow-all-paths` — lets it read any file in the project

---

### Step 16: Run a security check (programmatic)

```bash
copilot -p "Review all Python files for security issues: unvalidated inputs, missing error handling, injection risks. Output a numbered list of findings." \
  --allow-tool='read' \
  --model claude-sonnet-4-6 \
  --silent \
  --share=./audit/security-review.md
```

> - `--share=PATH` — exports the full session transcript to a Markdown file automatically after it finishes. Great for audit trails.
> - `--model` — pin a specific model for this task

---

### Step 17: Create a PR with an AI-generated description

Back in the interactive session (or start a new one):

```bash
git add .
git commit -m "feat: initial FastAPI task manager implementation"
git push origin main
```

Then inside Copilot:
```
/pr create
```

> Copilot analyzes your diff, writes a structured PR description (summary, changes, testing notes), and opens the PR on GitHub — all from the terminal.

---

## Phase 6 — Session Management

### Step 18: Export your session as a Markdown file

```
/share file session ./docs/copilot-session-build.md
```

> Exports the entire conversation + all tool outputs as a Markdown file. Useful for team documentation or onboarding new developers.

### Step 19: Export as a GitHub Gist (sharable link)

```
/share gist session
```

> Publishes the session as a secret Gist and gives you a URL to share with teammates.

### Step 20: Resume this session later

```bash
# List all your sessions
copilot /session list

# Resume by name
copilot
# then type:
/resume fastapi-task-manager-build
```

---

## 📋 Full Command Reference Used in This Project

| Command / Flag | Where Used | Purpose |
|---|---|---|
| `copilot login` | Setup | Authenticate |
| `copilot init` | Setup | Create project instructions file |
| `copilot` | Phase 3 | Launch interactive session |
| `/rename` | Session | Name the session |
| `/env` | Session | Verify loaded context |
| `! tree .` | Session | Run shell passthrough |
| `/diff` | Session | Review all file changes |
| `/undo` | Session | Roll back last AI turn |
| `/context` | Session | Check context window usage |
| `/compact` | Session | Summarize history to free context |
| `Shift+Tab` | Session | Cycle to autopilot mode |
| `--autopilot` | Phase 4 | Autonomous execution flag |
| `--allow-tool=` | Phases 4–5 | Whitelist specific tools |
| `--deny-tool=` | CI use | Blacklist specific tools |
| `-p` | Phase 5 | Programmatic prompt (no UI) |
| `--silent` | Phase 5 | Output response only |
| `--no-ask-user` | Phase 5 | No clarifying question pauses |
| `--share=PATH` | Phase 5 | Auto-export transcript |
| `--model=` | Phase 5 | Pin a specific AI model |
| `/pr create` | Phase 5 | AI-generated PR |
| `/share file` | Phase 6 | Export session to Markdown |
| `/share gist` | Phase 6 | Publish session to Gist |
| `/resume` | Phase 6 | Re-open a named session |

---

## 🧱 Final Project Structure

```
fastapi-task-manager/
├── .github/
│   └── copilot-instructions.md   ← Copilot reads this every session
├── routes/
│   └── tasks.py
├── tests/
│   └── test_tasks.py
├── audit/
│   └── security-review.md        ← Auto-generated by --share
├── docs/
│   └── copilot-session-build.md  ← Exported session transcript
├── main.py
├── models.py
├── requirements.txt
├── README.md                     ← Auto-generated by Copilot
└── .gitignore
```

---

