import csv
import sqlite3
import json

def load_recipes():
    """Load recipes from CSV into SQLite database."""
    print("Creating database...")
    conn = sqlite3.connect('data/recipes.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        minutes INTEGER,
        contributor_id INTEGER,
        submitted TEXT,
        tags TEXT,  -- JSON array
        nutrition TEXT,  -- JSON array
        n_steps INTEGER,
        steps TEXT,  -- JSON array
        description TEXT,
        ingredients TEXT,  -- JSON array
        n_ingredients INTEGER
    )
    ''')
    
    print("Reading CSV and inserting data...")
    with open('data/recipes.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert string lists to JSON strings for storage
            row['tags'] = json.dumps(eval(row['tags']))
            row['nutrition'] = json.dumps(eval(row['nutrition']))
            row['steps'] = json.dumps(eval(row['steps']))
            row['ingredients'] = json.dumps(eval(row['ingredients']))
            
            c.execute('''
            INSERT INTO recipes VALUES (
                :id, :name, :minutes, :contributor_id, :submitted,
                :tags, :nutrition, :n_steps, :steps, :description,
                :ingredients, :n_ingredients
            )
            ''', row)
            
            if reader.line_num % 10000 == 0:
                print(f"Processed {reader.line_num} recipes...")
                conn.commit()
    
    conn.commit()
    conn.close()
    print("Done! Database created at data/recipes.db")

if __name__ == '__main__':
    load_recipes() 