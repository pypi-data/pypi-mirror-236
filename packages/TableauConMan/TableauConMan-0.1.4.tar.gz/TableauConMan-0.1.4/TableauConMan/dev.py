import os
from plan import Plan
from projects_manager import ProjectsManager
from specification import Specification
from yaml_connector import YamlConnector
from jinja2 import Environment, BaseLoader, Template, FileSystemLoader
import yaml
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def custom_function(string):
    return string


def envvar(variable_name):
    return os.environ.get(variable_name)


def load_yaml_jinja():
    content = """{% set name = "pyexcel-ezodf" %}
    {% set version = "0.3.3" %}

    package:
      name: {{ name|lower }}
      other: this stuff
      version: {{ envvar('TABLEAU_API_SANDBOX_SITE_NAME') }}"""

    file_text = open("provision_plan.yaml", "r", encoding="UTF-8")

    templateLoader = FileSystemLoader(searchpath=".")

    jinja_environment = Environment(loader=templateLoader)
    jinja_environment.globals.update(envvar=envvar)

    yaml_content = yaml.safe_load(
        jinja_environment.get_template("provision_plan.yaml").render()
    )
    print(yaml_content["target"]["site_name"])


def generate_specification():
    raw_plan = YamlConnector("./provision_plan.yaml")

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    generate_project_specification(plan)


def generate_project_specification(generation_plan: Plan):
    projects = ProjectsManager(generation_plan)

    (
        projects_schema,
        permission_templates_schema,
    ) = projects.generate_server_project_schema()

    # logger.info(f"Projects Schema: {projects_schema}")
    # logger.info(f"Permission Templates Schema: {permission_templates_schema}")

    server_as_spec = {**projects_schema, **permission_templates_schema}

    spec_string = f"""{server_as_spec}"""

    logger.info(f"Server as Spec: {spec_string}")

    raw_spec = YamlConnector(yaml_string=spec_string)

    spec = Specification()
    spec.load_spec(raw_spec.get_yaml())

    spec.write_spec(spec.raw_spec, "test_spec")


def provision_settings():
    raw_plan = YamlConnector("./provision_plan.yaml")

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    provision_projects(plan)


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


if __name__ == "__main__":
    # provision_settings()
    # load_yaml_jinja()
    generate_specification()
