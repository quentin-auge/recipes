from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import ollama
import json
from typing import List, Dict, Any
import asyncio

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",
    args=["recipe_server.py"],
    env=None,
)

async def get_recipe_suggestions(session: ClientSession, ingredient: str) -> List[str]:
    """Use MCP client to get recipe suggestions based on an ingredient."""
    print(f'Calling MCP for {ingredient}')
    response = await session.call_tool("find_recipes_with_ingredient", arguments={"ingredient": ingredient})
    recipes = json.loads(response.content[0].text)["recipes"]
    return recipes

def extract_ingredients(query: str) -> List[str]:
    """Use Ollama to extract ingredients from a natural language query."""
    system_prompt = """You are a helpful cooking assistant. Extract ingredients from the user's query.
Return ONLY a JSON array of ingredient names, nothing else. Example: ["chicken", "garlic"]"""
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': query}
    ]
    print(f'Sent to LLM: {messages}')
    response = ollama.chat(model='mistral', messages=messages)
    
    try:
        # The model should return a JSON array string
        ingredients = json.loads(response['message']['content'])
        return ingredients
    except (json.JSONDecodeError, KeyError):
        # Fallback if model doesn't return valid JSON
        return [query.lower()]

async def suggest_recipes(session: ClientSession, query: str) -> Dict[str, List[str]]:
    """Get recipe suggestions based on ingredients in the query."""
    ingredients = extract_ingredients(query)
    results = {}
    
    for ingredient in ingredients:
        recipes = await get_recipe_suggestions(session, ingredient)
        results[ingredient] = recipes
    
    return results

def format_suggestions(suggestions: Dict[str, List[str]]) -> str:
    """Format recipe suggestions into a readable string."""
    system_prompt = """You are a helpful cooking assistant. Given these recipe suggestions, 
write a friendly response recommending some recipes to try. Keep it concise but engaging. Answer in French. Include the recipe original name."""
    
    # Convert suggestions to a readable format
    suggestions_text = "Here are the recipes I found:\n\n"
    for ingredient, recipes in suggestions.items():
        suggestions_text += f"For {ingredient}:\n"
        for i, recipe in enumerate(recipes, 1):
            suggestions_text += f"{i}. {recipe}\n"
        suggestions_text += "\n"
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': suggestions_text}
    ]
    print(f'Sent to LLM: {messages}')
    response = ollama.chat(model='mistral', messages=messages)
    
    return response['message']['content']

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            print("👩‍🍳 Recipe Assistant")
            print("Ask me about recipes with specific ingredients!")
            print("(Type 'quit' to exit)")
            print("-" * 50)
            
            while True:
                query = input("\nWhat would you like to cook? ").strip()
                
                if query.lower() in ('quit', 'exit'):
                    break
                
                if not query:
                    continue
                    
                print("\n🔍 Searching for recipes...")
                suggestions = await suggest_recipes(session, query)
                
                if not any(suggestions.values()):
                    print("❌ Sorry, I couldn't find any recipes matching those ingredients.")
                    continue
                
                response = format_suggestions(suggestions)
                print("\n" + response)
                print("-" * 50)

if __name__ == "__main__":
    asyncio.run(run()) 