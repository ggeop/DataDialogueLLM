# Data Dialogue
## Elevate Your Data Insights

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/u/datadialogue)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]()
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/ggeop/DataDialogueLLM?style=for-the-badge)](https://github.com/ggeop/DataDialogueLLM/releases/latest)

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![Release Workflow](https://github.com/ggeop/DataDialogueLLM/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/ggeop/DataDialogueLLM/actions/workflows/release.yml)
[![Black Code Formatter Check](https://github.com/ggeop/DataDialogueLLM/actions/workflows/black.yml/badge.svg)](https://github.com/ggeop/DataDialogueLLM/actions/workflows/black.yml)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎉 Welcome to Data Dialogue

> Transform the way you interact with data using AI-powered conversations

DataDialogue is an innovative application that bridges the gap between your data and natural language understanding. By leveraging advanced AI capabilities, it enables intuitive data exploration and analysis through conversational interfaces.

A user can select a LLM model and connect it with a data source and do his analysis by writing simple prompts instead of writing SQL queries or code.

![Data Dialogue Steps](media/imgs/data_dialogue_steps.png)
![Data Dialogue Agent Responses](media/imgs/data_dialogue_agent_responses.png)

## ✨ Key Features

- **Natural Language Querying**: Interact with your data using simple prompts instead of SQL
- **Multiple LLM Integration**:
  - HuggingFace models
  - Commercial models (Google LLMs)
- **Flexible Architecture**: Extend to different data sources easily
- **RESTful API**: Easy integration with other systems
- **Secure Query Execution**: Protection against harmful SQL commands
- **Query Validation**: Create and validate queries with copy option
- **Results Visualization**: Interactive data visualization
- **Multiple Data Source Support**: Connect to various data sources

<table>
<tr>
<td valign="top">
<h3>Supported Providers</h3>
<table>
<tr><th></th><th>Provider</th><th align="center">Status</th></tr>
<tr><td><img src="frontend/static/images/logos/google-logo.png" width="20"></td><td>Google</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/hf-logo.png" width="20"></td><td>HF</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/openai-logo.png" width="20"></td><td>OpenAI</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/anthropic-ai-logo.png" width="20"></td><td>Anthropic</td><td align="center">✔️</td></tr>
</table>
</td>
<td width="40"></td>
<td valign="top">
<h3>Supported Data Sources</h3>
<table>
<tr><th></th><th>Source</th><th align="center">Status</th></tr>
<tr><td><img src="frontend/static/images/logos/postgresql-logo.png" width="20"></td><td>PostgreSQL</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/mysql-log.png" width="20"></td><td>MySQL</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/databricks-logo.png" width="20"></td><td>Databricks</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/mongo-db-logo.png" width="20"></td><td>Mongo DB</td><td align="center">✔️</td></tr>
<tr><td><img src="frontend/static/images/logos/csv-logo.png" width="20"></td><td>CSV</td><td align="center">✔️</td></tr>
</table>
</td>
</tr>
</table>

## 🎯 Getting Started

### Prerequisites

- Docker
- Docker Compose

### Quick Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ggeop/data-dialogue.git
   cd data-dialogue
   ```

2. Run Data Dialogue services:
   ```sh
   docker-compose --env-file .env.prod up
   ```

3. Access the frontend at `http://localhost:5000` in your web browser.

> **Pro Tip**: Get your [FREE Google Gemini API key](https://aistudio.google.com/app/apikey) for the best cloud-based experience!

## 📚 Documentation

- [Installation Guide](getting-started/installation.md) - Detailed setup instructions
- [Quick Start Guide](getting-started/quick-start.md) - Get up and running quickly
- [Contributing](community/CONTRIBUTING.md) - How to contribute

## 🤝 Contributing

Your feedback and contributions make DataDialogue better! If you have:
- 💭 Feature suggestions
- 🐞 Bug reports
- 💡 General feedback

Please read our [Contributing Guidelines](community/CONTRIBUTING.md) before submitting any pull requests.

## ♥️ Support and Community

- Report issues via [GitHub Issues](https://github.com/ggeop/DataDialogueLLM/issues)
- Join our community discussions [here](https://github.com/ggeop/DataDialogueLLM/discussions)

## 📎 License

Distributed under the MIT License. See [License](license.md) for more information. 