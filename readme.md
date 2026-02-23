# Read It Later CLI: Queue & Stack Data Structure Manager

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **terminal based read it later application** that demonstrates classic data structures in python: **FIFO queue** for browsing order and **LIFO stack** for favorites. Built as a capstone demonstrating professional Python practices clear functions, error handling, and testable design.

Managing URLs to read later requires two distinct workflows:
- **Queue (`feed`)**: "Read in order I found them" (FIFO)—add to end, process from front.
- **Stack (`favorites`)**: "Quick favorites list" (LIFO)—add/remove most recent.

This CLI lets you add/skip, favorite/unfavorite, and view both structures with clear numbering.

## 🛠️ Key Data Structures

| Structure | Type | Behavior | Use Case |
|-----------|------|----------|----------|
| `feed` | `collections.deque()` | FIFO (append/popleft) | Sequential "read later" queue |
| `favorites` | `list` | LIFO (append/pop) | Quick-access favorites stack |

## ✨ Features

- **Interactive menu** with dispatch table pattern (`dict` maps key → function)
- **Input validation** (empty feed, invalid indices, edge cases)
- **Toggleable tracing** for debugging internal state (sizes, choices, flow)
- **Professional structure**: docstrings, single-responsibility functions, clear naming
- **Graceful shutdown** and error handling throughout

## 🚀 Quick Start

```bash
git clone https://github.com/Of-Arte/read-it-later.git
cd read-it-later
python main.py
```

## Future Plans
- Add local storage using SQLite.

- Integrate a local LLM via Ollama to generate short summaries of each URL in the background.
