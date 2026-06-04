# GitHub Copilot CLI: The Complete Guide — Commands, Plugins, Programmatic Use, and Real-World Use Cases

> **A deep-dive reference for developers who want to go beyond code completion and put an AI agent directly in their terminal.**

---

## Table of Contents

1. [What Is GitHub Copilot CLI?](#1-what-is-github-copilot-cli)
2. [Installation and Authentication](#2-installation-and-authentication)
3. [The Three Layers of Copilot CLI](#3-the-three-layers-of-copilot-cli)
4. [Part I — CLI Commands: Every Command Explained](#4-part-i--cli-commands-every-command-explained)
   - 4.1 Core Binary Commands
   - 4.2 Interactive Slash Commands (the Full List)
   - 4.3 Keyboard Shortcuts Cheat Sheet
   - 4.4 Tool Availability and Permission Patterns
   - 4.5 Environment Variables
5. [Part II — CLI Plugins: Extending Copilot with Packages](#5-part-ii--cli-plugins-extending-copilot-with-packages)
   - 5.1 Plugin Commands
   - 5.2 plugin.json Reference
   - 5.3 marketplace.json Reference
   - 5.4 Loading Order and Precedence
6. [Part III — Programmatic Use: Scripting and CI/CD Automation](#6-part-iii--programmatic-use-scripting-and-cicd-automation)
   - 6.1 Core Programmatic Flags
   - 6.2 Tool Filters and Fine-Grained Permissions
   - 6.3 Model Selection and Precedence
   - 6.4 Custom Agents in Headless Mode
7. [Real-World Use Case Examples](#7-real-world-use-case-examples)
8. [Best Practices and Pro Tips](#8-best-practices-and-pro-tips)
9. [Summary](#9-summary)

---

## 1. What Is GitHub Copilot CLI?

GitHub Copilot CLI is a full-featured **agentic coding assistant that runs directly in your terminal**. Unlike IDE extensions that suggest code snippets inline, Copilot CLI takes on complete tasks — reading your codebase, running shell commands, editing files, creating pull requests, conducting deep research, and more — all from a conversational prompt.

Think of it as having a senior engineer sitting beside you in your terminal. You describe a task in plain English; Copilot CLI plans a course of action, asks for permission before making consequential changes, executes multi-step workflows, and reports results — all without leaving the command line.

**Key capabilities at a glance:**

- **Interactive chat** — conversational back-and-forth in a rich terminal UI
- **Autopilot mode** — fully autonomous execution without stopping to confirm every step
- **Plan mode** — generate an implementation plan before any code is written
- **Fleet mode** — run subtasks in parallel across multiple subagents
- **Remote control** — steer a CLI session from GitHub.com or GitHub Mobile
- **Programmatic mode** — pipe a prompt in, get a result back (no interactive UI)
- **Plugins** — install or create packages that add agents, skills, MCP servers, and more
- **MCP server support** — connect the agent to any Model Context Protocol server
- **Custom agents** — define specialized sub-agents in Markdown files
- **Hooks** — run your own scripts before/after tool calls
- **Session persistence** — resume previous sessions; export transcripts to Markdown or Gists

---

## 2. Installation and Authentication

### Install

```bash
# macOS (Homebrew)
brew install github/gh/copilot

# Or download from GitHub releases and put the binary on your PATH
```

### Authenticate

```bash
# Log in via browser OAuth (default)
copilot login

# Log in to GitHub Enterprise Cloud (data residency)
copilot login --host https://your-org.ghe.com

# Use a fine-grained PAT via environment variable (for CI/headless use)
COPILOT_GITHUB_TOKEN=github_pat_... copilot
```

**Supported token types:**
- Fine-grained personal access tokens (v2 PATs) with the "Copilot Requests" permission
- OAuth tokens from the Copilot CLI app
- OAuth tokens from the GitHub CLI (`gh`) app

> **Note:** Classic `ghp_` personal access tokens are NOT supported.

Token priority order (highest to lowest): `COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN`

---

## 3. The Three Layers of Copilot CLI

Before diving into commands, it helps to understand how the three reference areas relate to each other:

| Layer | What it covers | When you use it |
|---|---|---|
| **CLI Commands** | All interactive commands, slash commands, keyboard shortcuts, tool names, environment variables | Every day use — launching sessions, chatting, using the UI |
| **CLI Plugins** | Installing, creating, and distributing packages that add new capabilities to the CLI | Sharing skills/agents with a team; building internal tooling; distributing to a marketplace |
| **Programmatic Reference** | Running the CLI without an interactive UI, piping prompts from scripts or CI pipelines | Automation, GitHub Actions, CI/CD, batch processing |

---

## 4. Part I — CLI Commands: Every Command Explained

### 4.1 Core Binary Commands

These are the commands you run directly in your shell, outside of any interactive session.

| Command | What it does | Detailed Notes |
|---|---|---|
| `copilot` | Launch the interactive terminal UI | No flags needed for a basic session. Opens a rich chat interface with timeline, tool output rendering, and keyboard shortcuts. |
| `copilot login` | Authenticate via OAuth browser flow | Stores a token in your OS credential store (or `~/.copilot/` if no credential store found). Use `--host` for GHE data residency instances. |
| `copilot logout` | Sign out | Removes stored credentials. |
| `copilot completion SHELL` | Generate shell completion script | Supports `bash`, `zsh`, `fish`. Pipe into your shell's completion directory to get tab-completion for all Copilot CLI subcommands and options. |
| `copilot help [TOPIC]` | Display help | Topics: `config`, `commands`, `environment`, `logging`, `monitoring`, `permissions`, `providers`. |
| `copilot init` | Initialize Copilot for a repository | Creates `AGENTS.md` / `.github/copilot-instructions.md` scaffolding with project-specific instructions for the agent. |
| `copilot mcp` | Manage MCP server configurations | Add, edit, and remove Model Context Protocol server connections from the command line. |
| `copilot plugin` | Manage plugins and marketplaces | See Part II for the full sub-command breakdown. |
| `copilot update` | Download and install the latest version | Also available as `/update` inside an interactive session. |
| `copilot version` | Show version and check for updates | Use `-v` or `--version` as shorthand. |

#### Shell Completion Examples

```bash
# Bash — current session only
source <(copilot completion bash)

# Bash — persistent (Linux)
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh — persistent (restart shell after running)
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

---

### 4.2 Interactive Slash Commands (The Full List)

Once inside an interactive session, you communicate via natural-language prompts **and** these slash commands. Slash commands are prefixed with `/` and can be run at any time, even mid-task.

#### Session and Navigation

| Command | Purpose |
|---|---|
| `/clear`, `/new`, `/reset [PROMPT]` | Start a fresh conversation. Optionally provide an opening prompt for the new session. |
| `/resume [SESSION-ID]`, `/continue` | Switch to a different session. Opens a session picker if no ID is provided. |
| `/rename [NAME]` | Name the current session for easier later retrieval. |
| `/session [SUBCOMMAND]` | Manage sessions in detail. Subcommands: `info`, `checkpoints`, `files`, `plan`, `rename`, `cleanup`, `prune`, `delete`, `delete-all`. |
| `/exit`, `/quit` | Exit the CLI. |
| `/restart` | Restart the CLI binary, preserving the current session. |

#### Context and Workspace

| Command | Purpose |
|---|---|
| `/cwd`, `/cd [PATH]` | Show the current working directory or change to a new one. |
| `/add-dir PATH` | Add an additional directory to the allowed file-access list for this session. |
| `/list-dirs` | Show all directories the agent currently has permission to access. |
| `/env` | Show loaded context: custom instructions, MCP servers, skills, agents, plugins, LSP servers, extensions. |
| `/instructions` | View and toggle which custom instruction files are loaded. |
| `/context` | Display context window token usage with a visual breakdown. |
| `/compact` | Summarize the conversation history to reclaim context window space without losing meaning. |

#### Agentic Modes

| Command | Purpose |
|---|---|
| `/plan [PROMPT]` | Enter plan mode — Copilot drafts an implementation plan and waits for your approval before executing. |
| `/delegate [PROMPT]` | Delegate changes to a remote repository; Copilot opens a pull request automatically. |
| `/fleet [PROMPT]` | Spin up parallel subagents to tackle different parts of a task simultaneously. |
| `/review [PROMPT]` | Trigger the code review agent on the current diff or a specified set of changes. |
| `/research TOPIC` | Run a deep research investigation using GitHub search and web sources. |

#### Pull Requests and Version Control

| Command | Purpose |
|---|---|
| `/pr [view\|create\|fix\|auto]` | Manage pull requests for the current branch. `create` opens a PR with an AI-generated description; `fix` addresses review comments; `auto` picks the best action. |
| `/diff` | Show the changes made so far in the current directory in rich diff format. |
| `/undo`, `/rewind` | Revert the last AI turn, rolling back any file changes made during that turn. |

#### Models and Customization

| Command | Purpose |
|---|---|
| `/model [MODEL]`, `/models` | Select or switch the active AI model. Choice is persisted to your config file. |
| `/agent` | Browse available custom agents and switch the active agent. |
| `/skills [list\|info\|add\|remove\|reload]` | Manage agent skills. |
| `/mcp [show\|add\|edit\|delete\|disable\|enable\|auth\|reload]` | Manage MCP server connections in the running session. |
| `/lsp [show\|test\|reload\|help]` | Manage Language Server Protocol server configurations. |
| `/plugin [marketplace\|install\|uninstall\|update\|list]` | Manage plugins from within an interactive session. |

#### Productivity Utilities

| Command | Purpose |
|---|---|
| `/allow-all [on\|off\|show]`, `/yolo` | Enable or disable the "allow everything" permission mode. |
| `/reset-allowed-tools` | Clear all previously granted tool permissions; the agent will ask again on next use. |
| `/share [file\|html\|gist] [session\|research] [PATH]` | Export the session to a Markdown file, interactive HTML file, or GitHub Gist. |
| `/chronicle <standup\|tips\|improve\|reindex>` | Session history tools — generate standups from your work history, get productivity tips, etc. (experimental) |
| `/usage` | Show token and request usage statistics for the current session. |
| `/changelog [summarize] [VERSION\|last N\|since VERSION]` | View the CLI changelog; add `summarize` for an AI-generated summary. |
| `/keep-alive [on\|off\|busy\|DURATION]` | Prevent the machine from sleeping during long-running agent tasks. |
| `/copy` | Copy the most recent agent response to the clipboard. |
| `/theme [default\|dim\|high-contrast\|colorblind]` | Change the UI color theme. |
| `/terminal-setup` | Configure the terminal for multiline input (Shift+Enter, Ctrl+Enter). |
| `/experimental [on\|off\|show]` | Toggle experimental features. |
| `/version` | Show CLI version from within a session. |
| `/help` | Show the help for all interactive commands. |

#### Remote Control

| Command | Purpose |
|---|---|
| `/remote [on\|off]` | Enable or disable remote steering, which lets you send messages to this session from GitHub.com or GitHub Mobile. |
| `/ide` | Connect to or disconnect from a VS Code workspace. |

---

### 4.3 Keyboard Shortcuts Cheat Sheet

#### Global Shortcuts

| Shortcut | Purpose |
|---|---|
| `@ FILENAME` | Include a file's contents in the current prompt context |
| `# NUMBER` | Include a GitHub issue or pull request by number in context |
| `! COMMAND` | Run a shell command directly, bypassing the AI agent |
| `?` | Open quick help (on an empty prompt) |
| `Ctrl+C` | Cancel operation or clear input; press twice to exit |
| `Ctrl+D` | Shut down the session |
| `Ctrl+G` | Open the prompt in your `$EDITOR` |
| `Ctrl+L` | Clear the screen |
| `Ctrl+Enter` / `Ctrl+Q` | Queue a message to send while the agent is busy |
| `Ctrl+R` | Reverse-search through command history |
| `Ctrl+V` | Paste from clipboard as an attachment |
| `Ctrl+X then /` | Run a slash command while in the middle of typing a prompt |
| `Ctrl+X then b` | Push the running shell command to the background |
| `Ctrl+X then o` | Open the most recent link from the timeline |
| `Ctrl+Z` | Suspend to background (Unix) |
| `Shift+Enter` / `Alt+Enter` | Insert a newline in the input without submitting |
| `Shift+Tab` | Cycle between standard, plan, and autopilot modes |

#### Timeline Shortcuts

| Shortcut | Purpose |
|---|---|
| `Ctrl+F` | Open timeline search |
| `Ctrl+O` | Expand recent timeline items to show more detail |
| `Ctrl+E` | Expand all timeline items |
| `Ctrl+T` | Toggle reasoning display in responses |
| `Page Up` / `Page Down` | Scroll the timeline |

#### Session Picker Shortcuts (when `/resume` is open)

| Shortcut | Purpose |
|---|---|
| `↑`/`↓` | Move selection |
| `Enter` | Open selected session |
| `s` | Cycle sort: relevance → created → name → last used |
| `Tab` | Switch between local and remote session tabs |
| `d` | Delete the selected session |
| `Esc` | Close the picker |

---

### 4.4 Tool Availability and Permission Patterns

When you run Copilot CLI interactively or programmatically, you can precisely control which tools the agent is allowed to use. Tools come in categories:

#### Shell Tools

| Tool Name | Description |
|---|---|
| `bash` / `powershell` | Execute shell commands |
| `list_bash` / `list_powershell` | List active shell sessions |
| `read_bash` / `read_powershell` | Read output from a running shell session |
| `stop_bash` / `stop_powershell` | Terminate a shell session |
| `write_bash` / `write_powershell` | Send input to a running shell session |

#### File Operation Tools

| Tool Name | Description |
|---|---|
| `apply_patch` | Apply patches (used by some models) |
| `create` | Create new files |
| `edit` | Edit files via string replacement |
| `view` | Read files or directories |

#### Agent and Task Delegation Tools

| Tool Name | Description |
|---|---|
| `list_agents` | List available agents |
| `read_agent` | Check background agent status |
| `task` | Run subagents |

#### Other Tools

| Tool Name | Description |
|---|---|
| `ask_user` | Ask the user a clarifying question |
| `glob` | Find files matching patterns |
| `grep` / `rg` | Search for text in files |
| `skill` | Invoke a custom skill |
| `web_fetch` | Fetch and parse web content |

#### Permission Patterns

The `--allow-tool` and `--deny-tool` flags accept patterns in the format `Kind(argument)`:

| Kind | Example Pattern | What it matches |
|---|---|---|
| `shell` | `shell(git:*)` | All git subcommands (git push, git pull, etc.) |
| `shell` | `shell(npm test)` | Only the exact command `npm test` |
| `write` | `write(src/*.ts)` | Any TypeScript file under `src/` |
| `read` | `read(.env)` | The specific `.env` file |
| `url` | `url(github.com)` | All HTTPS URLs on github.com |
| `url` | `url(https://*.api.com)` | Any subdomain of api.com |
| `memory` | `memory` | Storing facts to agent memory |
| `MyMCP` | `MyMCP(create_issue)` | Only the `create_issue` tool from MyMCP server |

> **Important:** Deny rules always take precedence over allow rules, even when `--allow-all` is set.

```bash
# Allow all git commands except git push
copilot --allow-tool='shell(git:*)' --deny-tool='shell(git push)'

# Allow specific MCP tool
copilot --allow-tool='github(create_issue)'

# Allow everything from a named MCP server
copilot --allow-tool='MyMCP'
```

---

### 4.5 Environment Variables

| Variable | Description |
|---|---|
| `COPILOT_GITHUB_TOKEN` | Authentication token (highest precedence) |
| `GH_TOKEN` | Authentication token (second precedence) |
| `GITHUB_TOKEN` | Authentication token (third precedence) |
| `COPILOT_ALLOW_ALL` | Set to `true` to allow all permissions automatically |
| `COPILOT_AUTO_UPDATE` | Set to `false` to disable automatic updates |
| `COPILOT_MODEL` | Set the AI model (e.g. `claude-sonnet-4.6`, `gpt-5.3-codex`) |
| `COPILOT_HOME` | Override the config and state directory (default: `~/.copilot`) |
| `COPILOT_CACHE_HOME` | Override the cache directory for marketplace caches and packages |
| `COPILOT_EDITOR` | Editor for interactive prompt editing (fallback after `$VISUAL`, `$EDITOR`) |
| `COPILOT_SKILLS_DIRS` | Comma-separated list of additional skill directories |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Comma-separated list of additional custom instruction directories |
| `COPILOT_SUBAGENT_MAX_CONCURRENT` | Maximum concurrent subagents (default: `32`, range: `1–256`) |
| `COPILOT_SUBAGENT_MAX_DEPTH` | Maximum subagent nesting depth (default: `6`, range: `1–256`) |
| `COPILOT_GH_HOST` | GitHub hostname for Copilot CLI only (overrides `GH_HOST`) |
| `GH_HOST` | GitHub hostname for both GH CLI and Copilot CLI |
| `COPILOT_PROMPT_FRAME` | Set `1` to enable / `0` to disable the decorative UI frame |
| `PLAIN_DIFF` | Set `true` to disable rich diff rendering |
| `GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS` | Set `true` to load project extensions in prompt (`-p`) mode |
| `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS` | Set `true` to load repository hooks in prompt mode |
| `GITHUB_COPILOT_PROMPT_MODE_WORKSPACE_MCP` | Set `true` to load workspace MCP sources in prompt mode |

---

## 5. Part II — CLI Plugins: Extending Copilot with Packages

Plugins allow you to bundle custom agents, skills, MCP server configurations, hooks, and even CLI commands into a single installable package. They are the distribution mechanism for Copilot CLI extensions — for your own team or for the wider community.

### 5.1 Plugin Commands

#### Terminal Commands (outside interactive session)

| Command | Description |
|---|---|
| `copilot plugin install SPECIFICATION` | Install a plugin (see specification formats below) |
| `copilot plugin uninstall NAME` | Remove a plugin |
| `copilot plugin list` | List all installed plugins |
| `copilot plugin update NAME` | Update a specific plugin (use `--all` to update everything) |
| `copilot plugin enable NAME` | Re-enable a previously disabled plugin |
| `copilot plugin disable NAME` | Disable a plugin without uninstalling it |
| `copilot plugin marketplace add SPECIFICATION` | Register a plugin marketplace |
| `copilot plugin marketplace list` | List registered marketplaces |
| `copilot plugin marketplace browse NAME` | Browse plugins in a marketplace |
| `copilot plugin marketplace remove NAME` | Unregister a marketplace |

#### Plugin Install Specification Formats

| Format | Example | Description |
|---|---|---|
| Marketplace | `plugin@marketplace` | Install from a registered marketplace |
| GitHub repo | `OWNER/REPO` | Install from the root of a GitHub repository |
| GitHub subdir | `OWNER/REPO:PATH/TO/PLUGIN` | Install from a subdirectory in a repo |
| Git URL | `https://github.com/o/r.git` | Install from any Git URL |
| Local path | `./my-plugin` or `/abs/path` | Install from a local directory |

---

### 5.2 plugin.json Reference

Every plugin must have a `plugin.json` file at its root. This manifest tells Copilot CLI what the plugin contains and where to find its components.

#### Required Field

| Field | Type | Description |
|---|---|---|
| `name` | string | Kebab-case plugin name. Letters, numbers, hyphens only. Max 64 chars. |

#### Optional Metadata Fields

| Field | Type | Description |
|---|---|---|
| `description` | string | Brief description. Max 1024 chars. |
| `version` | string | Semantic version (e.g., `1.0.0`) |
| `author` | object | `{ name (required), email?, url? }` |
| `homepage` | string | Plugin homepage URL |
| `repository` | string | Source repository URL |
| `license` | string | License identifier (e.g., `MIT`) |
| `keywords` | string[] | Search keywords for marketplace discovery |
| `category` | string | Plugin category |
| `tags` | string[] | Additional tags |

#### Component Path Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `agents` | string \| string[] | `agents/` | Paths to agent directories (`.agent.md` files) |
| `skills` | string \| string[] | `skills/` | Paths to skill directories (`SKILL.md` files) |
| `commands` | string \| string[] | — | Paths to command directories |
| `hooks` | string \| object | — | Path to a hooks config file, or inline hooks object |
| `mcpServers` | string \| object | — | Path to MCP config file (`.mcp.json`), or inline server definitions |
| `lspServers` | string \| object | — | Path to LSP config file, or inline server definitions |

#### Example plugin.json

```json
{
  "name": "my-dev-tools",
  "description": "React development utilities for our team",
  "version": "1.2.0",
  "author": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "license": "MIT",
  "keywords": ["react", "frontend", "typescript"],
  "agents": "agents/",
  "skills": ["skills/", "extra-skills/"],
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

---

### 5.3 marketplace.json Reference

A marketplace is a curated list of plugins hosted in a GitHub repository (or local directory). Store `marketplace.json` in `.github/plugin/` or `.claude-plugin/` in your repository.

#### Top-Level Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Kebab-case marketplace name. Max 64 chars. |
| `owner` | object | Yes | `{ name, email? }` — marketplace owner info |
| `plugins` | array | Yes | List of plugin entries |
| `metadata` | object | No | `{ description?, version?, pluginRoot? }` |

#### Plugin Entry Fields (within `plugins` array)

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Kebab-case plugin name |
| `source` | string \| object | Yes | Relative path, GitHub owner/repo, or URL |
| `description` | string | No | Plugin description |
| `version` | string | No | Plugin version |
| `strict` | boolean | No | When `true` (default), full schema validation is enforced |

#### Example marketplace.json

```json
{
  "name": "acme-internal-plugins",
  "owner": {
    "name": "Acme Engineering",
    "email": "eng-tools@acme.com"
  },
  "metadata": {
    "description": "Internal Copilot CLI plugins for Acme developers",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "frontend-design",
      "description": "UI design utilities and component generators",
      "version": "2.1.0",
      "source": "plugins/frontend-design"
    },
    {
      "name": "security-checks",
      "description": "OWASP and internal security audit skills",
      "version": "1.3.0",
      "source": "plugins/security-checks"
    }
  ]
}
```

---

### 5.4 Loading Order and Precedence

When multiple plugins or configuration sources define the same agent, skill, or MCP server, Copilot CLI follows a deterministic precedence model:

**Agents and Skills — first-found-wins:**

1. `~/.copilot/agents/` (user-level)
2. `<project>/.github/agents/` (project-level)
3. `<parents>/.github/agents/` (inherited from parent directories)
4. `<project>/.claude/agents/` (project-level)
5. Plugin-provided agents (in install order)
6. Remote org/enterprise agents

**MCP Servers — last-wins:**

1. `~/.copilot/mcp-config.json` (lowest priority)
2. Plugin-provided MCP configs
3. `--additional-mcp-config` flag (highest priority)

**Key rule:** Built-in tools and agents are always present and cannot be overridden by any user-defined configuration.

---

## 6. Part III — Programmatic Use: Scripting and CI/CD Automation

The programmatic mode turns Copilot CLI into a scriptable AI subprocess. You pass a prompt with `-p`, get a response to stdout, and the process exits cleanly — no interactive UI involved.

### 6.1 Core Programmatic Flags

| Option | Description |
|---|---|
| `-p PROMPT`, `--prompt=PROMPT` | Execute a prompt non-interactively. The CLI runs, outputs the response, and exits. |
| `-s`, `--silent` | Output only the agent response — no usage stats, no decorations. Essential for piping output. |
| `--allow-all`, `--yolo` | Grant all permissions (tools + paths + URLs). Equivalent to `--allow-all-tools --allow-all-paths --allow-all-urls`. |
| `--allow-all-tools` | Allow all tools without per-tool confirmation. Required for most non-interactive use. |
| `--allow-all-paths` | Disable file path verification. |
| `--allow-all-urls` | Allow fetching any URL. |
| `--allow-tool=TOOL ...` | Selectively allow specific tools (comma-separated list). |
| `--deny-tool=TOOL ...` | Deny specific tools (takes precedence over `--allow-all`). |
| `--no-ask-user` | Prevent the agent from pausing to ask clarifying questions. |
| `--model=MODEL` | Pin a specific AI model. |
| `--agent=AGENT` | Use a specific custom agent. |
| `--add-dir=PATH` | Add an additional directory to the allowed paths list. |
| `--secret-env-vars=VAR ...` | Redact named env variable values from all output/logs. |
| `--share=PATH` | Export the session transcript to a Markdown file after completion. |
| `--share-gist` | Publish the session transcript to a secret GitHub Gist. |
| `--output-format=FORMAT` | `text` (default) or `json` (outputs JSONL — one JSON object per line). |
| `--autopilot` | Enable autonomous continuation in prompt mode. |
| `--max-autopilot-continues=COUNT` | Cap the number of continuation messages in autopilot mode. |

### 6.2 Tool Filters and Fine-Grained Permissions

| Kind | Example | What it controls |
|---|---|---|
| `shell` | `shell(git:*)` | All git subcommands |
| `shell` | `shell(npm test)` | Only the exact `npm test` command |
| `write` | `write(.github/copilot-instructions.md)` | Write to this specific path |
| `write` | `write(README.md)` | Write to any file ending in `/README.md` |
| `url` | `url(github.com)` | HTTPS access to github.com |
| `url` | `url(http://localhost:3000)` | Access to local dev server |
| `url` | `url(https://*.github.com)` | Any GitHub subdomain |
| `url` | `url(https://docs.github.com/copilot/*)` | A specific path subtree |
| MCP server | `github(create_issue)` | Only `create_issue` tool from `github` MCP server |

### 6.3 Model Selection and Precedence

You can specify which model handles a task — useful for balancing cost and capability across different CI jobs.

```bash
# Fast, cheap model for simple summary tasks
copilot -p "What does this project do?" -s --model claude-haiku-4.5

# Powerful model for deep reasoning tasks
copilot -p "Fix the race condition in the worker pool" \
  --model gpt-5.3-codex \
  --allow-tool='write,shell'
```

**Model precedence order (highest to lowest):**
1. Model specified in the custom agent definition (if using `--agent`)
2. `--model` command-line option
3. `COPILOT_MODEL` environment variable
4. `model` key in `~/.copilot/config.json`
5. CLI default model

You can set a persistent model and reasoning effort in `~/.copilot/config.json`:

```json
{
  "model": "gpt-5.3-codex",
  "reasoning_effort": "low"
}
```

### 6.4 Custom Agents in Headless Mode

```bash
# Use a custom code-review agent in programmatic mode
copilot -p "Review the latest commit" \
  --allow-tool='shell' \
  --agent code-review
```

---

## 7. Real-World Use Case Examples

### Use Case 1: Daily Interactive Coding Session

```bash
# Launch a session from your project root
cd ~/projects/my-api
copilot

# Inside the session:
# > "Explain the auth middleware in src/middleware/auth.ts"
# > "Refactor it to use async/await instead of callbacks"
# > "/diff"
# > "/pr create"
```

### Use Case 2: Autopilot Mode for Large Refactors

```bash
# Launch directly into autopilot mode — no confirmation prompts
copilot --autopilot --allow-all-tools --allow-all-paths \
  -i "Migrate all console.log statements to use the Winston logger"
```

### Use Case 3: CI/CD — Automated Code Quality Check

```yaml
# .github/workflows/copilot-review.yml
- name: Copilot code review
  env:
    COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_TOKEN }}
  run: |
    copilot -p "Review the changed files in this PR for security issues and coding standards violations" \
      --allow-tool='shell(git:*)' \
      --allow-tool='read' \
      --model claude-sonnet-4.6 \
      --silent \
      --share=review-output.md
```

### Use Case 4: Scripted Batch Processing

```bash
#!/bin/bash
# Generate tests for all service files that lack test coverage

for service in src/services/*.ts; do
  echo "Generating tests for $service..."
  copilot -p "Write unit tests for $service. Place them in tests/ following the existing naming convention." \
    -s \
    --allow-tool='write,read' \
    --allow-all-paths \
    --no-ask-user
done
```

### Use Case 5: Fleet Mode for Parallel Feature Work

```
# Inside interactive session:
/fleet "Implement the user authentication feature:
- Subagent 1: Create the JWT token service in src/auth/
- Subagent 2: Write the login and register API endpoints
- Subagent 3: Write unit tests for both"
```

### Use Case 6: Deep Research on a Technical Topic

```
# Inside interactive session:
/research "What are the current best practices for rate limiting in Node.js APIs in 2025? Focus on Redis-based solutions."
```

### Use Case 7: Remote Control from Mobile

```bash
# Start a session with remote access enabled
copilot --remote

# The CLI displays a session URL you can open in GitHub Mobile
# You can then send messages and monitor progress from your phone
```

### Use Case 8: Installing and Using a Team Plugin

```bash
# An enterprise team registers their internal marketplace
copilot plugin marketplace add https://github.com/acme/copilot-plugins

# Browse available plugins
copilot plugin marketplace browse acme-copilot-plugins

# Install a specific plugin
copilot plugin install security-checks@acme-copilot-plugins

# Now the security audit agent is available in every session
copilot
# > "Run the security audit agent on the payment module"
```

### Use Case 9: Session Export and Audit Trail

```bash
# Run a task and automatically export the full transcript
copilot -p "Analyze the database schema and suggest normalization improvements" \
  --allow-all \
  --share=./audit/copilot-db-analysis-$(date +%Y%m%d).md \
  --silent
```

### Use Case 10: Agentic Pull Request Management

```
# Inside interactive session on a feature branch:
/pr create

# Copilot will:
# 1. Analyze the diff
# 2. Generate a structured PR description
# 3. Link related issues
# 4. Open the PR on GitHub
```

---

## 8. Best Practices and Pro Tips

**Start with Plan Mode for complex tasks.** Use `Shift+Tab` or `--mode=plan` to have Copilot draft a plan before touching any files. This is the single best way to avoid unwanted changes.

**Use `/undo` freely.** Copilot CLI tracks checkpoints, so you can always roll back the last turn's file changes with `/undo`. Don't be afraid to let it try things.

**Lock down tools in CI.** Never use `--allow-all` in CI pipelines. Instead, explicitly list the exact tools the agent needs: `--allow-tool='shell(git:*),write(src/*),read'`. This creates a minimal-permission surface and makes your CI pipelines auditable.

**Name your sessions.** Use `/rename` or `-n NAME` to give sessions meaningful names. You'll thank yourself later when you want to `/resume` a specific session from three days ago.

**Use `/compact` for long sessions.** When the context window fills up on a long task, `/compact` summarizes the history into a tighter representation, reclaiming tokens without losing the thread of work.

**Use `@file` and `#issue` for precision context.** Rather than describing a file, just type `@src/auth/middleware.ts` in your prompt to inject the file's contents directly. Same for `#123` to include a GitHub issue.

**Redact secrets in programmatic mode.** Always use `--secret-env-vars` to redact any tokens or passwords that might appear in logs: `--secret-env-vars='DB_PASSWORD,AWS_SECRET_KEY'`.

**Store model preferences in config.** Instead of always passing `--model`, set your preferred model once in `~/.copilot/config.json` using the `/model` slash command. It persists across sessions.

**Use plugins for team consistency.** Package your team's custom agents, shared skills, and MCP server configurations into a plugin and distribute via an internal marketplace. This ensures every developer gets the same capabilities without manual setup.

**Monitor context usage.** Use `/context` to see how full the context window is. On long exploratory tasks, periodically `/compact` to keep performance high and avoid context cutoff.

---

## 9. Summary

GitHub Copilot CLI is not just a terminal chat interface — it's a composable, scriptable, extensible AI agent platform built for software developers. Here's what you now know:

**CLI Commands** give you a full-featured terminal UI with rich slash commands for managing sessions, agentic modes, pull requests, model selection, MCP servers, and more. The keyboard shortcuts alone — from queueing messages to expanding timeline items to remote steering — make daily use significantly faster.

**Plugins** let you package and distribute custom agents, skills, and MCP configurations as installable packages. The `plugin.json` manifest and `marketplace.json` catalog enable team-level distribution without requiring every developer to manually configure their environment.

**Programmatic mode** transforms Copilot CLI into a CI/CD-native tool. With `-p` for prompts, `-s` for silent output, precise tool permission patterns, and model pinning, you can build AI-powered automation into GitHub Actions, shell scripts, and batch workflows with full auditability.

Together these three layers make GitHub Copilot CLI one of the most powerful developer productivity tools available — a genuine AI agent for the command line that you can customize, extend, and automate to fit exactly how you work.

---

*Last updated: May 2026. For the latest commands and options, run `copilot help` in your terminal or visit [docs.github.com/copilot](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).*
