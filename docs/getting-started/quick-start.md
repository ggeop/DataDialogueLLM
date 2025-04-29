# Quick Start Guide

This guide will help you get up and running with DataDialogue in minutes.

## Prerequisites

- Docker
- Docker Compose

## Quick Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ggeop/data-dialogue.git
   cd data-dialogue
   ```

2. Start the services:
   ```sh
   docker-compose --env-file .env.prod up
   ```

3. Access the application at `http://localhost:5000`

## First Steps

1. **Choose Your Model**
   - Select a model provider (Google, OpenAI, Anthropic, or HuggingFace)
   - For cloud models, you'll need to provide your API key
   - For local models (HuggingFace), ensure you have sufficient computing power

2. **Connect Your Data Source**
   - Select from supported data sources:
     - PostgreSQL
     - MySQL
     - Databricks
     - MongoDB
     - CSV files
   - Provide your connection details

3. **Start Querying**
   - Write natural language queries instead of SQL
   - Get instant results and visualizations
   - Copy validated queries for reuse

## Example Workflow

1. **Select Model**: Choose Google Gemini (recommended for beginners)
2. **Connect Data**: Link your PostgreSQL database
3. **Write Query**: "Show me the top 10 customers by total purchases"
4. **View Results**: See the data in a table or chart format
5. **Copy Query**: Save the generated SQL for future use

## Tips for Success

- Start with simple queries to test the system
- Use the "Copy Query" feature to learn how your questions are translated to SQL
- Try different visualization options for your results
- Check the [Common Issues](../development/COMMON_ISSUES.md) guide if you encounter problems

## Next Steps

- Explore [advanced features](../user-guide/features.md)
- Learn about [local development](../development/DEV_SETUP.md)
- Join our [community discussions](https://github.com/ggeop/DataDialogueLLM/discussions) 