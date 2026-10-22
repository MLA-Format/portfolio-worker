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
    This function will get a list of all tier one and tier two skills in the database.
    It will return them as a list of skills.
    """
    connection = await get_connection(env.HYPERDRIVE)
    
    try:
        # Get all parent (first level) skills.
        parent_level_skills = await connection.fetch(
            "SELECT skills.name as name, skills.priority as priority, skills.id as id FROM skills WHERE skills.parent_id IS NULL"
        )

        ret_val: list = []

        for parent in parent_level_skills:

            # Get all of a parent's children (second level) skills
            children_skills = await connection.fetch(
                "SELECT skills.name as name, skills.priority as priority, skills.id as id FROM skills where skills.parent_id=$1",
                parent.get("id")
            )

            curr_parent: dict = dict(parent)
            curr_parent.update(
                {
                    "children": [dict(child) for child in children_skills]
                }
            )
            ret_val.append(curr_parent)
        
        return ret_val

    except Exception as error:
        logger.exception(f"Failed to fetch skills: {error}")
        return
    finally:
        await connection.close()

async def db_get_contacts(env):
    """
    This function will return a list of all contacts in the database.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all contacts.
        contacts = await connection.fetch(
            "SELECT contacts.name as name, contacts.value as value, " \
            "contacts.icon as icon, contacts.link as link, contacts.priority as priority, "
            "contacts.show_in_header as show_in_header FROM contacts"
        )

        return [dict(contact) for contact in contacts]

    except Exception as error:
        logger.exception(f"Failed to fetch skills: {error}")
        return
    finally:
        await connection.close()

async def db_get_education(env):
    """
    This function will return a list of all related educational institutions.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all contacts.
        schools = await connection.fetch(
            "SELECT education.school as school, education.degree as degree, " \
            "education.start_date as start_date, education.end_date as end_date, " \
            "education.image as image FROM education"
        )

        return [dict(school) for school in schools]

    except Exception as error:
        logger.exception(f"Failed to fetch skills: {error}")
        return
    finally:
        await connection.close()