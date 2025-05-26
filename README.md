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

## Data

The recipe dataset is stored in the `data/recipes.csv` file (not tracked in git due to size). The data comes from [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv) on Kaggle.

To convert the CSV data into a SQLite database:
```bash
python scripts/load_recipes.py
```

This will create `data/recipes.db` with all recipes stored in the `recipes` table.

## MCP Server

The MCP server provides tools to search and interact with the recipe database.

### Running the Server

You can run the server with the MCP Inspector for testing:
```bash
mcp dev recipe_server.py
```

This will open the MCP Inspector in your browser, where you can:
- View available tools
- Test the recipe search functionality
- See the JSON responses

### Available Tools

- `find_recipes_with_ingredient(ingredient: str)`: Search for recipes containing a specific ingredient. Returns a JSON response with recipe titles.