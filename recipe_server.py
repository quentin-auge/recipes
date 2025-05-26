import sqlite3
import json
from typing import List
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Recipe Search")

def search_recipes_by_ingredient(ingredient: str) -> List[str]:
    """Search recipes containing a specific ingredient."""
    conn = sqlite3.connect('data/recipes.db')
    cursor = conn.cursor()
    
    # Search in the ingredients JSON array using json_each to unnest the array
    cursor.execute("""
        SELECT DISTINCT name 
        FROM recipes, json_each(recipes.ingredients) 
        WHERE json_each.value LIKE ?
        LIMIT 10
    """, (f"%{ingredient.lower()}%",))
    
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

@mcp.tool()
def find_recipes_with_ingredient(ingredient: str) -> str:
    """
    Find recipes that contain a specific ingredient.
    
    Args:
        ingredient: The ingredient to search for (e.g. "chicken", "tomatoes")
        
    Returns:
        JSON string containing an array of recipe titles
    """
    recipes = search_recipes_by_ingredient(ingredient)
    return json.dumps({"recipes": recipes})

if __name__ == "__main__":
    mcp.run() 