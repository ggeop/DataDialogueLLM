<div align="center">

# DataDialogueLLM

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/u/datadialogue)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]()
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/ggeop/DataDialogueLLM?style=for-the-badge)](https://github.com/ggeop/DataDialogueLLM/releases/tag/v1.3.0)

[![Release Workflow](https://github.com/ggeop/DataDialogueLLM/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/ggeop/DataDialogueLLM/actions/workflows/release.yml)
[![Black Code Formatter Check](https://github.com/ggeop/DataDialogueLLM/actions/workflows/black.yml/badge.svg)](https://github.com/ggeop/DataDialogueLLM/actions/workflows/black.yml)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h3>🤖 Intelligent Data Interaction Powered by AI 🔍</h3>

</div>

## 🎉 Welcome to Data Dialogue!

> Transform the way you interact with data using AI-powered conversations

DataDialogue is an innovative application that bridges the gap between your data and natural language understanding. By leveraging advanced AI capabilities, it enables intuitive data exploration and analysis through conversational interfaces.

### ✨ Key Features

- 🤖 **AI-Powered Prompts**: Intelligent prompt generation for natural data interactions
- 🔄 **Multiple Data Sources**: Seamless integration with various data repositories
- 🚀 **LLM Backend**: Advanced language model processing for accurate responses
- 🎨 **Modern UI**: Clean, intuitive interface for enhanced user experience
- 🐳 **Docker Ready**: Easy deployment with containerized services

## 🚀 Quick Preview

Try our demo by clicking the "Try Demo" button. The demo mode loads an open-source DVD database (PostgreSQL) for testing and experimentation. We provide several example prompts to get you started, but you're welcome to create your own custom prompts.
The system supports both open-source language models from HuggingFace and commercial LLMs (such as Google Gemini).


   Google Gemini provides a FREE API [get key](https://aistudio.google.com/app/apikey).
   If your machine doesn't have enough processing power to run local HuggingFace models effectively, commercial LLMs are a great alternative.


[![Data Dialogue Demo!](https://img.youtube.com/vi/breOr5o7r3Y/0.jpg)](https://www.youtube.com/watch?v=breOr5o7r3Y)

### 🏗️ Architecture

DataDialogue consists of two main components:
- **LLM Backend**: Powers the AI processing and data analysis
- **User Interface**: Provides an intuitive way to interact with the system

## 🌟 Preview Phase

We're currently in an exciting preview phase! Here's what that means for you:

- 💡 **Early Access**: Get a first look at cutting-edge AI-data interaction
- 🔄 **Regular Updates**: Frequent improvements and new features
- 👥 **Community Driven**: Your feedback shapes the future of DataDialogue
- 🐞 **Bug Reports Welcome**: Help us polish the experience


Please don't hesitate to open an issue or submit a pull request.

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

### Production Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/ggeop/data-dialogue.git
   cd data-dialogue
   ```

2. Run Data Dialogue services:

   **Linux**
   ```sh
   docker-compose --profile production pull && docker-compose --profile production up
   ```

   **Windows**
   ```powershell
   docker-compose --profile production pull; if ($?) { docker-compose --profile production up}
   ```

3. Access the frontend at `http://localhost:5000` in your web browser.

## Development

For local development and setup instructions, please refer to our [Local Development Setup Guide](LOCAL_SETUP.md).

The guide includes:
- Local environment setup for Windows and Linux
- Code style configuration with Black
- Development workflows
- Common issues and troubleshooting
- Contributing guidelines

## Project Structure

```
data-dialogue/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   ├── js/
│   │   └── templates/
│   ├── app.py
│   └── Dockerfile
├── scripts/
│   └── black/
│       ├── setup_linux.sh
│       └── setup_windows.bat
├── docker-compose.yml
├── .gitignore
├── LOCAL_SETUP.md
└── README.md
```

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

## 🤝 Contributing

Your feedback and contributions make DataDialogue better! If you have:
- 💭 Feature suggestions
- 🐞 Bug reports
- 💡 General feedback

Please read our [Contributing Guidelines](./CONTRIBUTING.md) before submitting any pull requests.

## Support and Community

- Report issues via [GitHub Issues](https://github.com/ggeop/DataDialogueLLM/issues)
- Join our community discussions [here](https://github.com/ggeop/DataDialogueLLM/discussions)
