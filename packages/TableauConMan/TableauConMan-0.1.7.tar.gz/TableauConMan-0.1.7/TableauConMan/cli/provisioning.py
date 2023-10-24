from TableauConMan.plan import Plan
from TableauConMan.workbooks_manager import WorkbooksManager
from TableauConMan.data_sources_manager import DataSourcesManager
from TableauConMan.projects_manager import ProjectsManager
from TableauConMan.groups_manager import GroupsManager
from TableauConMan.yaml_connector import YamlConnector
from loguru import logger
from dotenv import load_dotenv
from . import cli
import click

load_dotenv()

# "./public_sync_plan.yaml"
@cli.command()  # type: ignore
@click.option(
    "--yaml_path",
    help="String path of where the yaml plan is located",
)
def migrate_content(yaml_path: str):
    """

    :param yaml_path:
    :return:
    """
    raw_plan = YamlConnector(yaml_path)

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    migrate_datasources(plan)

    migrate_workbooks(plan)


@cli.command()  # type: ignore
@click.option(
    "--yaml_path",
    help="String path of where the yaml plan is located",
)
def provision_settings(yaml_path: str):
    """

    :param yaml_path:
    :return:
    """
    raw_plan = YamlConnector(yaml_path)

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    provision_groups(plan)


def migrate_datasources(migrate_plan: Plan):
    logger.info("Processing Datasources")
    datasources = DataSourcesManager(migrate_plan)
    datasources.populate_datasources()
    logger.info("Populated datasources")
    # logger.debug(datasources.reference_datasources)

    datasource_options = datasources.get_datasource_options()

    to_update, to_add, to_remove = datasources.get_datasource_changes()
    logger.debug(f"Update:{to_update}, Add:{to_add}, Remove:{to_remove}")

    datasources.remove(to_remove)

    datasources.add(
        to_add,
        to_update,
        datasource_options,
    )

    logger.info("Processed Datasources")


def migrate_workbooks(migration_plan: Plan):
    logger.info("Processing Workbooks")
    workbooks = WorkbooksManager(migration_plan)
    workbooks.populate_workbooks()
    logger.info("Populated workbooks")
    logger.debug(workbooks.reference_workbooks)

    workbook_options = workbooks.get_workbook_options()
    to_update, to_add, to_remove = workbooks.get_workbook_changes()
    logger.debug(f"Update:{to_update}, Add:{to_add}, Remove:{to_remove}")

    workbooks.remove(to_remove)

    workbooks.add(to_add, to_update, workbook_options)

    logger.info("Processed Workbooks")


def provision_projects(provision_plan: Plan):
    logger.info("Processing Projects")
    projects = ProjectsManager(provision_plan)
    projects.populate_projects()
    logger.info("Populated projects")
    logger.debug(f"Reference Projects: {projects.reference_projects}")
    logger.debug(f"Reference Project List: {projects.reference_projects_list}")
    logger.debug(f"Target Projects: {projects.target_projects}")
    logger.debug(f"Target Project List: {projects.target_projects_list}")
    logger.debug(f"Target Project Path List: {projects.target_project_paths_list}")
    logger.debug(
        f"Reference Project Path List: {projects.reference_project_paths_list}"
    )

    to_update, to_remove, to_add = projects.get_project_changes()
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    projects.add(to_add)

    projects.remove(to_remove)

    projects.update(to_update)

    logger.info("Processed Projects")

    project_options = projects.get_project_options()

    if project_options.get("update_permissions"):
        logger.info("Processing Permissions")
        projects.populate_projects()
        logger.info("Populated projects")
        projects.populate_users_and_groups()
        projects.populate_project_permissions()
        projects.populate_permission_capabilities()

        """logger.debug(
            f"Target Capabilities: {projects.target_project_capabilities_list}"
        )"""
        """logger.debug(
            f"Reference Capabilities: {projects.reference_project_capabilities_list}"
        )"""

        to_update, to_remove, to_add = projects.get_permission_changes()
        # logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")
        logger.debug(f"Add:{to_add}")
        logger.debug(f"Remove:{to_remove}")
        # logger.debug(f"Update: {to_update}")

        projects.add_capabilities(to_add)

        projects.remove_capabilities(to_remove)

    logger.info("Processed Permissions")


def provision_groups(provision_plan: Plan):
    logger.info("Processing Groups")
    groups = GroupsManager(provision_plan)
    groups.populate_groups()
    logger.info("Populated groups")
    logger.debug(f"Target Groups: {groups.target_groups_list}")
    logger.debug(f"Reference Groups: {groups.reference_groups_list}")
    logger.debug(f"Target Group Memberships: {groups.target_group_memberships_list}")
    logger.debug(
        f"Reference Group Memberships: {groups.reference_group_memberships_list}"
    )
    groups.populate_users()

    to_add, to_remove, to_update = groups.get_group_changes()
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    groups.remove(to_remove)

    groups.add(to_add)

    groups.update(to_update)

    logger.info("Processed Groups")
