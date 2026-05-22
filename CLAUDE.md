# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment setup

Requires a `.env` file with `ANTHROPIC_API_KEY=<your-key>`. The venv is at `.venv/`.

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the scripts

```bash
python main.py      # multi-turn demo: asks Claude two questions and prints the second answer
python chatbot.py   # interactive: prompts for user input, sends it to Claude, prints response
```

## Architecture

Both scripts share the same pattern:

- `Anthropic()` client auto-reads `ANTHROPIC_API_KEY` from the environment (loaded via `python-dotenv`)
- Conversation state is a plain `list` of `{"role": ..., "content": ...}` dicts passed directly to `client.messages.create()`
- `add_user_message` / `add_assistant_message` append to that list; `chat()` calls the API and returns prefixed text

`main.py` is a scripted two-turn exchange (no stdin). `chatbot.py` replaces the hardcoded question with `input()` for an interactive single-turn loop.

Model used: `claude-sonnet-4-6`.
