from src.core import logger
from src.db.mysql_connector import MySQLDatabase
import asyncio

# Example usage:

async def main():
    db = MySQLDatabase(
        host='localhost', 
        port=3306, 
        user='runicorer', 
        password='123123'
    )
    
    try:
        # # Running any SQL command (creating a table)
        # await db.execute('CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))')

        # # Switching to another database and creating a table there
        # await db.execute('USE other_db')
        # await db.execute('CREATE TABLE IF NOT EXISTS test_table_other (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))', db='other_db')
        
        # # Inserting data into the default database
        # await db.execute('INSERT INTO test_table (name) VALUES (%s)', params=('John Doe',), db='default_db')

        await db.execute("USE runicore;")
        results = await db.execute("SELECT * FROM users;")
        if results:
            print(results)
        
    
    except Exception as e:
        logger.error(f"An error occurred during database operations: {e}")
    finally:
        await db.close()

# Running the async function
asyncio.run(main())
