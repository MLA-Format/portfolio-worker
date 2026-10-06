# Library imports.
import asyncpg
import logging

# Get global logger.
logger = logging.getLogger(__name__)

async def get_connection(hyperdrive) -> asyngpg.Connection:
    connection = await asyncpg.connect(
        host=hyperdrive.host,
        port=int(hyperdrive.port),
        user=hyperdrive.user,
        password=hyperdrive.password,
        database=hyperdrive.database,
        ssl=False,
    )

    return connection

async def db_get_skills(env):
    """

    """
    connection = await get_connection(env.HYPERDRIVE)
    
    try:
        query = await connection.fetch(
            "SELECT skills.name as skills, skills.priority as priority FROM skills WHERE skills.parent_id IS NULL"
        )

        return query

    except Exception as error:
        logger.exception(f"Failed to fetch skills: {error}")
        return
    finally:
        await connection.close()