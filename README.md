<div align="center">

<span style="font-size: 2em; font-weight: bold;">Data Dialogue</span>
<br>
<span style="font-size: 1.2em; font-style: italic;">Elevate Your Data Insights</span>
<hr>

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/u/datadialogue)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]()
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/ggeop/DataDialogueLLM?style=for-the-badge)](https://github.com/ggeop/DataDialogueLLM/releases/latest)

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![Release Workflow](https://github.com/ggeop/DataDialogueLLM/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/ggeop/DataDialogueLLM/actions/workflows/release.yml)
[![Black Code Formatter Check](https://github.com/ggeop/DataDialogueLLM/actions/workflows/black.yml/badge.svg)](https://github.com/ggeop/DataDialogueLLM/actions/workflows/black.yml)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 🎉 Welcome to Data Dialogue

> Transform the way you interact with data using AI-powered conversations

DataDialogue is an innovative application that bridges the gap between your data and natural language understanding. By leveraging advanced AI capabilities, it enables intuitive data exploration and analysis through conversational interfaces.

A user can select a LLM model and connect it with a data source and do his analysis by writing simple prompts instead of writing SQL queries or code.


<div style="display: flex; gap: 20px;">

<div>

**Supported Providers**

|      | Provider | Status |
|------|----------|:------:|
| <img src="frontend/static/images/logos/google-logo.png" width="20"> | Google | ✔️ |
| <img src="frontend/static/images/logos/hf-logo.png" width="20">     | HF     | ✔️ |
| <img src="frontend/static/images/logos/openai-logo.png" width="20"> | OpenAI | ✔️ |
| <img src="frontend\static/images/logos/anthropic-ai-logo.png" width="20"> | Athropic | ✔️ |

</div>

<div>

**Supported Data Sources**
|      | Source | Status |
|------|----------|:------:|
| <img src="frontend/static/images/logos/postgresql-logo.png" width="20"> | PostgreSQL | ✔️ |
| <img src="frontend/static/images/logos/mysql-log.png" width="20"> | MySQL | ✔️ |
| <img src="frontend/static/images/logos/databricks-logo.png" width="20"> | Databricks | ✔️ |
| <img src="frontend/static/images/logos/mongo-db-logo.png" width="20"> | Mongo DB | ✔️ |
| <img src="frontend/static/images/logos/csv-logo.png" width="20"> | CSV | ✔️ |

</div>

</div>

## 🌟 Preview Phase

We're currently in an exciting preview phase! Here's what that means for you:

- 💡 **Early Access**: Get a first look at cutting-edge AI-data interaction
- 🔄 **Regular Updates**: Frequent improvements and new features
- 👥 **Community Driven**: Your feedback shapes the future of DataDialogue
- 🐞 **Bug Reports Welcome**: Help us polish the experience


Please don't hesitate to open an issue or submit a pull request.

Experience our powerful demo with just one click! We've prepared everything you need to get started instantly:

<div align="center">
<div style="position: relative; display: inline-block; width: fit-content;">
  <a href="https://www.youtube.com/watch?v=breOr5o7r3Y" style="text-decoration: none;">
    <img src="media/imgs/data_dialogue_agent_responses.png" alt="Data Dialogue Demo" width="600" style="display: block; border-radius: 8px; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);"/>
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">
      <img src="media/youtube_button.png" alt="Play Button" style="width: 64px; transition: transform 0.2s ease-in-out;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'"/>
    </div>
  </a>
</div>
</div>

### ✨ Key Features

- **Demo Database**: Pre-loaded open-source DVD database (PostgreSQL)
- **Example Prompts**: Curated selection of prompts to showcase capabilities
- **Flexible Model Support**: Choose between:
  - 🤗 HuggingFace open-source models
  - 🤖 Commercial LLMs (like Google Gemini)

### 🎯 Getting Started

1. **Try the Demo**: Click the video above to see it in action
2. **Choose Your Model**:
   - Local: HuggingFace models (requires sufficient computing power)
   - Cloud: Commercial LLMs (recommended for lighter setups)

> **Pro Tip**: Get your [FREE Google Gemini API key](https://aistudio.google.com/app/apikey) for the best cloud-based experience!

---

<div align="center">
</div>

## Features
- Natural language querying of databases
- Integration with multiple language models
   - Integration with HuggingFace models
   - Integration with Commercial models (currently with Google LLMs)
- Flexible architecture for extending to different data sources
- RESTful API for easy integration
- Secure query execution with protection against harmful SQL commands
- Create validated Queries (+ Copy option)
- Results Visualization

![UI Screenshot](media/imgs/data_dialogue_steps.png)
![UI Screenshot](media/imgs/data_dialogue_agent_responses.png)

## Quick Start Guide

### Prerequisites

- Docker
- Docker Compose

### Run

1. Clone the repository:
   ```sh
   git clone https://github.com/ggeop/data-dialogue.git
   cd data-dialogue
   ```

2. Run Data Dialogue services:
   ```
   docker-compose --env-file .env.prod up
   ```


3. Access the frontend at `http://localhost:5000` in your web browser.

## Development

For local development and setup instructions, please refer to our [Local Development Setup Guide](./docs/DEV_SETUP.md).

The guide includes:
- Local environment setup for Windows and Linux
- Code style configuration with Black
- Development workflows
- Common issues and troubleshooting
- Contributing guidelines


## 🤝 Contributing

Your feedback and contributions make DataDialogue better! If you have:
- 💭 Feature suggestions
- 🐞 Bug reports
- 💡 General feedback

Please read our [Contributing Guidelines](./docs/CONTRIBUTING.md) before submitting any pull requests.

## ♥️ Support and Community

- Report issues via [GitHub Issues](https://github.com/ggeop/DataDialogueLLM/issues)
- Join our community discussions [here](https://github.com/ggeop/DataDialogueLLM/discussions)

## Need Help?

Feel free to:
- Open an issue on GitHub
- Ask questions in pull requests
- Contact project maintainers

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.