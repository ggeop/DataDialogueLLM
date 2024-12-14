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

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://www.youtube.com/watch?v=breOr5o7r3Y">
          <picture>
            <img src="media/imgs/data_dialogue_agent_responses.png" alt="Data Dialogue Demo" width="600" style="max-width: 100%; border-radius: 10px; margin-bottom: -40px;"/>
          </picture>
          <br/>
        </a>
      </td>
    </tr>
    <tr>
      <td align="center">
        <a href="https://www.youtube.com/watch?v=breOr5o7r3Y" style="text-decoration: none;">
          <picture>
            <img src="media/youtube_button.png" alt="Play Button" width="20" style="margin-right: 5px; vertical-align: middle;"/>
          </picture>
          <sup>Click to watch the demo video</sup>
        </a>
      </td>
    </tr>
  </table>
</div>

> Transform the way you interact with data using AI-powered conversations

DataDialogue is an innovative application that bridges the gap between your data and natural language understanding. By leveraging advanced AI capabilities, it enables intuitive data exploration and analysis through conversational interfaces.

A user can select a LLM model and connect it with a data source and do his analysis by writing simple prompts instead of writing SQL queries or code.


We're currently in an exciting preview phase! Here's what that means for you:

- 💡 **Early Access**: Get a first look at cutting-edge AI-data interaction
- 🔄 **Regular Updates**: Frequent improvements and new features
- 👥 **Community Driven**: Your feedback shapes the future of DataDialogue
- 🐞 **Bug Reports Welcome**: Help us polish the experience


Please don't hesitate to open an issue or submit a pull request.


## ✨ Key Features

- Natural language querying of databases
- Integration with multiple language models
   - Integration with HuggingFace models
   - Integration with Commercial models (currently with Google LLMs)
- Flexible architecture for extending to different data sources
- RESTful API for easy integration
- Secure query execution with protection against harmful SQL commands
- Create validated Queries (+ Copy option)
- Results Visualization
- **Supported Models**: Choose between HuggingFace & public providers
- **Data Sources**: Suppoorts connection with multiple data sources
 
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

![UI Screenshot](media/imgs/data_dialogue_steps.png)
![UI Screenshot](media/imgs/data_dialogue_agent_responses.png)

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

4. **Try the Demo**: Click the video above to see it in action
5. **Choose Your Model**:
   - Local: HuggingFace models (requires sufficient computing power)
   - Cloud: Commercial LLMs (recommended for lighter setups)

> **Pro Tip**: Get your [FREE Google Gemini API key](https://aistudio.google.com/app/apikey) for the best cloud-based experience!


## 📑 Development

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

## ✋ Need Help?

Feel free to:
- Open an issue on GitHub
- Ask questions in pull requests
- Contact project maintainers

## 📎 License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.
