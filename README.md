# Claude Code Sandbox
Author: Xavier VAN AUSLOOS 
La Donnée Intelligente

Creation: 22 May 26

A sandbox project for learning Claude Code, created as part of the [Claude Code training](https://verify.skilljar.com/c/dhg628knonny).

It contains two small Python scripts that interact with the Anthropic API to demonstrate multi-turn conversations.

## Prerequisites

- Python 3.11+
- An Anthropic API key

Create a `.env` file at the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the scripts

**Scripted two-turn demo** — asks Claude to define quantum computing, then requests a follow-up sentence:

```bash
python main.py
```

**Interactive chatbot** — prompts for your input, sends it to Claude, and prints the response:

```bash
python chatbot.py
```
