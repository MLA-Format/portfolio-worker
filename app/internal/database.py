# Library imports.
import asyncpg
import logging

# Get global logger.
logger = logging.getLogger(__name__)

async def get_connection(hyperdrive) -> asyncpg.Connection:
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
            "SELECT education.school as school, education.degree as degree, "
            "education.start_date as start_date, education.end_date as end_date, "
            "education.image as image FROM education"
        )

        return [dict(school) for school in schools]

    except Exception as error:
        logger.exception(f"Failed to fetch skills: {error}")
        return
    finally:
        await connection.close()


async def db_get_projects(env):
    """
    Return all projects with their linked skills and optional URL contacts.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        projects = await connection.fetch(
            "SELECT projects.id as id, projects.name as name, "
            "projects.start_date as start_date, projects.end_date as end_date, "
            "projects.description as description, projects.image as image, "
            "projects.priority as priority FROM projects "
            "ORDER BY projects.priority NULLS LAST, projects.id"
        )

        skills = await connection.fetch(
            "SELECT project_skills.project_id as project_id, skills.id as id, "
            "skills.name as name, skills.priority as priority, skills.icon as icon "
            "FROM project_skills JOIN skills "
            "ON skills.id = project_skills.skill_id "
            "ORDER BY project_skills.project_id, skills.priority NULLS LAST, skills.id"
        )

        contacts = await connection.fetch(
            "SELECT project_contacts.project_id as project_id, contacts.id as id, "
            "project_contacts.contact_type as type, contacts.name as name, "
            "contacts.value as value, contacts.icon as icon, contacts.link as link, "
            "contacts.priority as priority, contacts.show_in_header as show_in_header "
            "FROM project_contacts JOIN contacts "
            "ON contacts.id = project_contacts.contact_id "
            "ORDER BY project_contacts.project_id, project_contacts.contact_type"
        )

        project_values = {
            project["id"]: {
                **dict(project),
                "skills": [],
                "contacts": [],
            }
            for project in projects
        }

        for skill in skills:
            project_values[skill["project_id"]]["skills"].append(
                {
                    "id": skill["id"],
                    "name": skill["name"],
                    "priority": skill["priority"],
                    "icon": skill["icon"],
                }
            )

        for contact in contacts:
            project_values[contact["project_id"]]["contacts"].append(
                {
                    "id": contact["id"],
                    "type": contact["type"],
                    "name": contact["name"],
                    "value": contact["value"],
                    "icon": contact["icon"],
                    "link": contact["link"],
                    "priority": contact["priority"],
                    "show_in_header": contact["show_in_header"],
                }
            )

        return list(project_values.values())
    except Exception as error:
        logger.exception(f"Failed to fetch projects: {error}")
        raise
    finally:
        await connection.close()


async def db_get_snippets(env):
    """
    Return all code snippets, ordered by priority.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        snippets = await connection.fetch(
            "SELECT snippets.id as id, snippets.name as name, "
            "snippets.snippet_path as snippet_path, snippets.language as language, "
            "snippets.priority as priority FROM snippets "
            "ORDER BY snippets.priority NULLS LAST, snippets.id"
        )

        return [dict(snippet) for snippet in snippets]
    except Exception as error:
        logger.exception(f"Failed to fetch snippets: {error}")
        raise
    finally:
        await connection.close()