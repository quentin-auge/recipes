# Recipes

## Development Setup

1. Create and activate a virtual environment using `uv`:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Ollama Setup

1. Install Ollama:
```bash
brew install ollama
```

2. Start Ollama service:
```bash
brew services start ollama
```

3. Pull the Mistral model:
```bash
ollama pull mistral
```

## Data

The recipe dataset is stored in the `data/recipes.csv` file (not tracked in git due to size). The data comes from [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv) on Kaggle.

To convert the CSV data into a SQLite database:
```bash
python scripts/load_recipes.py
```

This will create `data/recipes.db` with all recipes stored in the `recipes` table.

## LLM Recipe Assistant

The LLM-powered recipe assistant combines Ollama's Mistral model with our recipe database to provide intelligent recipe suggestions.

To run the assistant:
```bash
python llm_recipe_client.py
```

Features:
- Natural language ingredient extraction
- Multi-ingredient search
- AI-powered recipe suggestions
- French language responses with original recipe names

Example queries:
- "I want to cook something with chicken and garlic"
- "What can I make with tomatoes and basil?"
- "Show me recipes with mushrooms"

## MCP Server

The MCP server provides tools to search and interact with the recipe database.

### Running the Server

You can run the server with the MCP Inspector for testing:
```bash
mcp dev recipe_server.py
```

### Available Tools

- `find_recipes_with_ingredient(ingredient: str)`: Search for recipes containing a specific ingredient. Returns a JSON response with recipe titles.