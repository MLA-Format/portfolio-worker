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
        parent_level_skills = await connection.fetch(
            "SELECT skills.name as skill, skills.priority as priority, skills.id as id FROM skills WHERE skills.parent_id IS NULL"
        )

        ret_val: list = []

        for parent in parent_level_skills:
            children_skills = await connection.fetch(
                "SELECT skills.name as skill, skills.priority as priority FROM skills where skills.parent_id=$1",
                parent.get("id")
            )

            curr_parent: dict = dict(parent)
            curr_parent.update(
                {
                    "children": children_skills
                }
            )
            ret_val.append(curr_parent)
        
        return ret_val


    except Exception as error:
        logger.exception(f"Failed to fetch skills: {error}")
        return
    finally:
        await connection.close()