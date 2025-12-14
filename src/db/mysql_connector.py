from typing import List, Tuple, Any, Optional
import aiomysql
import asyncio
from ..core import logger

class MySQLDatabase:
    def __init__(self, host: str, port: int, user: str, password: str, db: Optional[str] = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db  # Default database to connect to
        self.pool = None
        logger.info(f"Initialized MySQLDatabase with host: {host}, port: {port}")

    async def _create_pool(self):
        """Create a connection pool."""
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,  # Default database
            minsize=1,
            maxsize=10
        )
        logger.info("MySQL connection pool created.")

    async def _get_connection(self) -> aiomysql.Connection:
        """Get a connection from the pool."""
        if not self.pool:
            await self._create_pool()
        return await self.pool.acquire()

    async def execute(self, sql: str, params: Optional[Tuple[Any, ...]] = None, db: Optional[str] = None) -> Optional[List[Tuple[Any, ...]]]:
        """
        Execute any SQL query. If a database is specified, it will use 'USE db_name' 
        to switch to that database before executing the query.

        :param sql: The SQL query to execute
        :param params: Parameters to bind to the query (if any)
        :param db: Database to switch to (if any)
        :return: List of tuples with query results if SELECT query, otherwise None
        """
        conn = await self._get_connection()
        try:
            async with conn.cursor() as cursor:
                # If a specific database is provided, switch to that database
                if db:
                    await cursor.execute(f"USE {db}")
                    logger.info(f"Switched to database: {db}")
                
                # Execute the SQL query
                await cursor.execute(sql, params)
                
                # Check if the query is a SELECT query and fetch results if needed
                if sql.strip().lower().startswith("select"):
                    result = await cursor.fetchall()
                    return result
                else:
                    await conn.commit()
                    logger.info(f"Executed query: {sql} with params: {params}. No results returned.")
                    return None
        except Exception as e:
            logger.error(f"Error executing query: {sql}. Error: {e}")
            raise
        finally:
            self.pool.release(conn)
            logger.info("Connection released back to the pool.")

    async def close(self) -> None:
        """Close the connection pool."""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed.")
