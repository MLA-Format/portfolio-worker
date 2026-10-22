# Library imports.
import asyncpg
import logging
from fastapi import HTTPException
from typing import Any

# Get global logger.
logger = logging.getLogger(__name__)


async def get_connection(hyperdrive: Any) -> asyncpg.Connection:
    try:
        connection = await asyncpg.connect(
            host=hyperdrive.host,
            port=int(hyperdrive.port),
            user=hyperdrive.user,
            password=hyperdrive.password,
            database=hyperdrive.database,
            ssl=False,
        )
    except Exception:
        logger.exception("Failed to connect to the database.")
        raise HTTPException(
            status_code=500, detail="Failed to connect to the database.")

    return connection


async def db_get_skills(env: Any) -> list[dict[str, Any]]:
    """
    Return all parent (first level) skills, each with its child (second level) skills,
    ordered by priority.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all skills in one query, then group children under their parents.
        skills = await connection.fetch(
            "SELECT skills.id as id, skills.name as name, skills.priority as priority, "
            "skills.icon as icon, skills.parent_id as parent_id FROM skills "
            "ORDER BY skills.priority, skills.id"
        )

        parents = {
            skill["id"]: {**dict(skill), "children": []}
            for skill in skills
            if skill["parent_id"] is None
        }

        for skill in skills:
            if skill["parent_id"] in parents:
                parents[skill["parent_id"]]["children"].append(dict(skill))

        return list(parents.values())
    except Exception:
        logger.exception("Failed to fetch skills.")
        raise HTTPException(status_code=500, detail="Failed to fetch skills.")
    finally:
        await connection.close()


async def db_get_contacts(env: Any) -> list[dict[str, Any]]:
    """
    Return all general contacts, ordered by priority.
    Contacts linked to a project (e.g. a project's GitHub or live URL) are excluded.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all contacts not linked to a project.
        contacts = await connection.fetch(
            "SELECT contacts.name as name, contacts.value as value, "
            "contacts.icon as icon, contacts.link as link, contacts.priority as priority, "
            "contacts.show_in_header as show_in_header FROM contacts "
            "WHERE contacts.id NOT IN (SELECT project_contacts.contact_id FROM project_contacts) "
            "ORDER BY contacts.priority, contacts.id"
        )

        return [dict(contact) for contact in contacts]
    except Exception:
        logger.exception("Failed to fetch contacts.")
        raise HTTPException(
            status_code=500, detail="Failed to fetch contacts.")
    finally:
        await connection.close()


async def db_get_education(env: Any) -> list[dict[str, Any]]:
    """
    Return all educational institutions, ordered with current and most recent first.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all schools.
        schools = await connection.fetch(
            "SELECT education.school as school, education.degree as degree, "
            "education.start_date as start_date, education.end_date as end_date, "
            "education.image as image FROM education "
            "ORDER BY education.end_date DESC, education.start_date DESC"
        )

        return [dict(school) for school in schools]
    except Exception:
        logger.exception("Failed to fetch education.")
        raise HTTPException(
            status_code=500, detail="Failed to fetch education.")
    finally:
        await connection.close()


async def db_get_projects(env: Any) -> list[dict[str, Any]]:
    """
    Return all projects with their linked skills and optional URL contacts,
    ordered by priority.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all projects, then their skills and contacts, and group them by project.
        projects = await connection.fetch(
            "SELECT projects.id as id, projects.name as name, "
            "projects.start_date as start_date, projects.end_date as end_date, "
            "projects.description as description, projects.image as image, "
            "projects.priority as priority FROM projects "
            "ORDER BY projects.priority, projects.id"
        )

        skills = await connection.fetch(
            "SELECT project_skills.project_id as project_id, skills.id as id, "
            "skills.name as name, skills.priority as priority, skills.icon as icon "
            "FROM project_skills JOIN skills "
            "ON skills.id = project_skills.skill_id "
            "ORDER BY skills.priority, skills.id"
        )

        contacts = await connection.fetch(
            "SELECT project_contacts.project_id as project_id, contacts.id as id, "
            "project_contacts.contact_type as type, contacts.name as name, "
            "contacts.value as value, contacts.icon as icon, contacts.link as link, "
            "contacts.priority as priority, contacts.show_in_header as show_in_header "
            "FROM project_contacts JOIN contacts "
            "ON contacts.id = project_contacts.contact_id "
            "ORDER BY project_contacts.contact_type"
        )

        project_values = {
            project["id"]: {**dict(project), "skills": [], "contacts": []}
            for project in projects
        }

        for skill in skills:
            project_values[skill["project_id"]]["skills"].append(dict(skill))

        for contact in contacts:
            project_values[contact["project_id"]
                           ]["contacts"].append(dict(contact))

        return list(project_values.values())
    except Exception:
        logger.exception("Failed to fetch projects.")
        raise HTTPException(
            status_code=500, detail="Failed to fetch projects.")
    finally:
        await connection.close()


async def db_get_experience(env: Any) -> list[dict[str, Any]]:
    """
    Return all work experience, ordered by priority.
    """
    connection = await get_connection(env.HYPERDRIVE)

    try:
        # Get all experience.
        experience = await connection.fetch(
            "SELECT experience.id as id, experience.name as name, "
            "experience.title as title, experience.icon as icon, "
            "experience.start_date as start_date, experience.end_date as end_date, "
            "experience.bulleted_description as bulleted_description, "
            "experience.priority as priority FROM experience "
            "ORDER BY experience.priority, experience.id"
        )

        return [dict(job) for job in experience]
    except Exception:
        logger.exception("Failed to fetch experience.")
        raise HTTPException(
            status_code=500, detail="Failed to fetch experience.")
    finally:
        await connection.close()
