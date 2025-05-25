# Recipes

## Data

The recipe dataset is stored in the `data/recipes.csv` file (not tracked in git due to size). The data comes from [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv) on Kaggle.

To convert the CSV data into a SQLite database:
```bash
python scripts/load_recipes.py
```

This will create `data/recipes.db` with all recipes stored in the `recipes` table.