from __future__ import annotations

from argparse import _MutuallyExclusiveGroup
from argparse import _SubParsersAction
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from pathlib import Path

from vortex.models import DesignType

NON_SERVER_COMMANDS = ("code", "clean", "config", "docs")


def _check_positive_limit(val: str, limit: int = 50) -> int:
    new_val = int(val)
    if new_val <= 0 or new_val > limit:
        raise ArgumentTypeError(f"%s is not between 1 and {limit}. " % val)
    return new_val


def _add_server_option(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--server",
        "-s",
        metavar="NAME",
        help="Enter the name of the server definition in the config file to use",
    )


def _add_design_type_option(
    parser: ArgumentParser | _MutuallyExclusiveGroup,
) -> None:
    parser.add_argument(
        "--type",
        "-t",
        nargs="*",
        dest="design_type",
        type=DesignType.from_name,
        metavar="DESIGN_TYPE",
        help=(f"Choices: {[t.name.lower() for t in DesignType]}"),
    )


def add_code_parser(
    command_parser: _SubParsersAction[ArgumentParser],
) -> ArgumentParser:
    code_parser = command_parser.add_parser(
        "code",
        help="Open the workspace in Visual Studio Code",
        add_help=False,
    )
    code_parser.add_argument("--help", "-h", action="store_true")
    return code_parser


def add_list_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    list_parser = command_parser.add_parser(
        "list",
        aliases=("ls",),
        help=(
            "List Puakma Applications on the server or cloned locally."
            "(ls is an alias for 'vortex list --local')"
        ),
    )
    list_parser.add_argument(
        "--group",
        "-g",
        nargs="*",
        help="Enter application 'group' to filter the results",
    )
    list_parser.add_argument(
        "--name",
        "-n",
        nargs="*",
        help="Enter application 'name' to filter the results",
    )
    list_parser.add_argument(
        "--template",
        "-t",
        nargs="*",
        help="Enter application 'template' to filter the results",
    )
    list_parser.add_argument(
        "--fuzzy",
        "-z",
        help="Set this flag to fuzzy search when using filters",
        action="store_true",
    )
    list_parser.add_argument(
        "--local",
        action="store_true",
        dest="show_local_only",
        help="Set this flag to list locally cloned applications instead",
    )
    list_parser.add_argument(
        "--show-inherited",
        help="Set this flag to also display inherited applications",
        action="store_true",
    )
    list_parser.add_argument(
        "--show-inactive",
        help="Set this flag to also display inactive applications",
        action="store_true",
    )
    list_parser.add_argument(
        "--ids-only",
        "-x",
        help=(
            "Set this flag to only display the ID's of the applications in the output"
        ),
        dest="show_ids_only",
        action="store_true",
    )
    list_parser.add_argument(
        "--open-urls",
        "-o",
        help="Set this flag to open each application URL in a web browser",
        action="store_true",
    )
    list_parser.add_argument(
        "--open-dev-urls",
        "-d",
        help="Set this flag to open each application webdesign URL in a web browser",
        action="store_true",
    )
    list_parser.add_argument(
        "--show-connections",
        help="Set this flag to list the Database Connections of locally cloned apps",
        action="store_true",
    )
    list_parser.add_argument(
        "--all",
        "-a",
        help="Set this flag to show all applications",
        action="store_true",
    )
    _add_server_option(list_parser)


def add_clone_parser(
    command_parser: _SubParsersAction[ArgumentParser],
) -> ArgumentParser:
    clone_parser = command_parser.add_parser(
        "clone",
        help="Clone Puakma Applications and their design objects into the workspace",
    )
    clone_parser.add_argument(
        "app_ids",
        nargs="*",
        metavar="APP_ID",
        help="The ID(s) of the Puakma Application(s) to clone",
        type=int,
    )
    clone_parser.add_argument(
        "--reclone",
        help="Set this flag to reclone locally cloned applictions",
        action="store_true",
    )
    clone_parser.add_argument(
        "--get-resources",
        "-r",
        help="Set this flag to also clone the application's resources",
        action="store_true",
    )
    clone_parser.add_argument(
        "--open-urls",
        "-o",
        help="Set this flag to open the application and webdesign URLs after cloning",
        action="store_true",
    )
    clone_parser.add_argument(
        "--pmx",
        nargs="?",
        metavar="PATH",
        const="",
        help=(
            "Set this flag to clone applications in .pmx format to a destination "
            "folder. Default is 'exports' in the workspace."
        ),
        type=Path,
    )
    _add_server_option(clone_parser)
    return clone_parser


def add_watch_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    watch_parser = command_parser.add_parser(
        "watch",
        help=(
            "Watch the workspace for changes to Design Objects "
            "and upload them to the server"
        ),
    )
    _add_server_option(watch_parser)


def add_clean_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    command_parser.add_parser(
        "clean",
        help="Delete the cloned Puakma Application directories in the workspace",
    )


def add_config_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    config_parser = command_parser.add_parser(
        "config", help="View and manage configuration"
    )

    _add_server_option(config_parser)

    config_mutex = config_parser.add_mutually_exclusive_group(required=True)
    config_mutex.add_argument(
        "--sample",
        dest="print_sample",
        action="store_true",
        help="Print a sample 'vortex-server-config.ini' file to the console",
    )
    config_mutex.add_argument(
        "--update-vscode-settings",
        action="store_true",
        help="Updates the vortex.code-workspace file. Creating it if doesn't exist",
    )
    config_mutex.add_argument(
        "--reset-vscode-settings",
        action="store_true",
        help="Recreates the vortex.code-workspace file",
    )
    config_mutex.add_argument(
        "--output-config-path",
        action="store_true",
        help="Outputs the file path to the config file",
    )
    config_mutex.add_argument(
        "--output-workspace-path",
        action="store_true",
        help="Outputs the file path to the workspace",
    )
    config_mutex.add_argument(
        "--output-server-config",
        action="store_true",
        help="Outputs the current server definition in the config file.",
    )


def add_log_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    log_parser = command_parser.add_parser(
        "log",
        help="View the last items in the server log",
    )
    log_parser.add_argument(
        "-n",
        type=_check_positive_limit,
        help="The number of logs to return between 1 and 50. Default is %(default)s",
        default=10,
        dest="limit",
    )
    log_parser.add_argument("--source", help="Filter the logs returned by their source")
    log_parser.add_argument(
        "--message", "-m", help="Filter the logs returned by their message"
    )
    log_type_mutex = log_parser.add_mutually_exclusive_group()
    log_type_mutex.add_argument("--errors-only", action="store_true")
    log_type_mutex.add_argument("--debug-only", action="store_true")
    log_type_mutex.add_argument("--info-only", action="store_true")
    log_parser.add_argument("--keep-alive", action="store_true")
    _add_server_option(log_parser)


def add_find_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    find_parser = command_parser.add_parser(
        "find",
        help="Find Design Objects of cloned applications by name",
        usage="%(prog)s [options] name",
    )
    find_parser.add_argument("name", help="The name of Design Objects to find")
    find_parser.add_argument("--app-id", type=int, nargs="*", dest="app_ids")
    find_parser.add_argument("--fuzzy", "-z", action="store_true")
    find_parser.add_argument(
        "--ids-only",
        "-x",
        help="Set this flag to only display the ID's of the objects in the output",
        dest="show_ids_only",
        action="store_true",
    )
    find_parser.add_argument(
        "--show-params",
        help="Set this flag to also display the Design Object parameters",
        action="store_true",
    )
    find_design_type_mutex = find_parser.add_mutually_exclusive_group()
    find_design_type_mutex.add_argument("--exclude-resources", action="store_true")
    _add_design_type_option(find_design_type_mutex)
    _add_server_option(find_parser)


def add_grep_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    grep_parser = command_parser.add_parser(
        "grep",
        help=(
            "Search the contents of cloned Design Objects using a Regular Expression."
        ),
        usage="%(prog)s [options] pattern",
    )
    grep_parser.add_argument("pattern", help="The Regular Expression pattern to match")
    grep_parser.add_argument("--app-id", type=int, nargs="*", dest="app_ids")

    grep_output_mutex = grep_parser.add_mutually_exclusive_group()
    grep_output_mutex.add_argument("--output-paths", action="store_true")
    grep_output_mutex.add_argument("--output-apps", action="store_true")

    grep_design_type_mutex = grep_parser.add_mutually_exclusive_group()
    grep_design_type_mutex.add_argument("--exclude-resources", action="store_true")

    _add_design_type_option(grep_design_type_mutex)
    _add_server_option(grep_parser)


def add_new_parser(
    command_parser: _SubParsersAction[ArgumentParser],
) -> ArgumentParser:
    new_parser = command_parser.add_parser("new", help="Create new Design Object(s)")
    new_parser.add_argument("names", nargs="+")
    new_parser.add_argument("--app-id", type=int, required=True)
    new_parser.add_argument("--comment", "-c")
    new_parser.add_argument("--inherit-from")
    new_parser.add_argument("--open-action")
    new_parser.add_argument("--save-action")
    new_parser.add_argument("--parent-page")
    new_parser.add_argument(
        "--type",
        "-t",
        dest="design_type",
        type=DesignType.from_name,
        metavar=f"[{', '.join([t.name.lower() for t in DesignType])}]",
        required=True,
    )
    new_parser.add_argument(
        "--content-type", help="The MIME Type. Only used when creating a 'resource'."
    )
    _add_server_option(new_parser)
    return new_parser


def add_copy_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    copy_parser = command_parser.add_parser(
        "copy", help="Copy a Design Object from one application to another"
    )
    copy_parser.add_argument("ids", nargs="+", metavar="DESIGN_ID", type=int)
    copy_parser.add_argument(
        "--app-id", nargs="+", type=int, required=True, metavar="APP_ID"
    )
    copy_parser.add_argument("--copy-params", action="store_true")
    _add_server_option(copy_parser)


def add_delete_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    delete_parser = command_parser.add_parser(
        "delete", help="Delete Design Object(s) by ID"
    )
    delete_parser.add_argument("obj_ids", nargs="+", type=int, metavar="DESIGN_ID")
    _add_server_option(delete_parser)


def add_db_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    db_parser = command_parser.add_parser(
        "db", help="Interact with Database Connections"
    )
    db_parser.add_argument(
        "connection_id",
        metavar="CONNECTION_ID",
        type=int,
        help="The Database Connection ID",
    )
    db_mutex = db_parser.add_mutually_exclusive_group(required=True)
    db_mutex.add_argument("--sql", help="Execute a given SQL query")
    db_mutex.add_argument(
        "--schema",
        metavar="TABLE_NAME",
        help="View the schema of a table",
    )
    db_mutex.add_argument(
        "--list-tables",
        "-l",
        action="store_true",
        help="List the tables within the Database Connection",
    )
    db_parser.add_argument(
        "--update",
        "-u",
        action="store_true",
        help="Set this flag when running modifying querys to update the database",
    )
    db_parser.add_argument(
        "--limit",
        "-n",
        metavar="N",
        type=_check_positive_limit,
        help=(
            "The number of results to be returned when using --sql between 1 and 50. "
            "This flag adds the 'LIMIT' clause of the given SQL query. "
            "Default is %(default)s."
        ),
        default=5,
    )


def add_docs_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    command_parser.add_parser("docs", help="Open the Torndao Server Blackbook")


def add_upload_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    upload_parser = command_parser.add_parser(
        "upload", help="Upload a .pmx file to create a new application."
    )
    upload_parser.add_argument(
        "pmx_file", type=Path, help="The path to the .pmx file to upload"
    )
    upload_parser.add_argument(
        "--name", "-n", help="The name of the application to create", required=True
    )
    upload_parser.add_argument(
        "--group", "-g", help="The group of the application to create", required=True
    )


def add_execute_parser(command_parser: _SubParsersAction[ArgumentParser]) -> None:
    execute_parser = command_parser.add_parser(
        "execute",
        aliases=("exec",),
        help="Execute a command on the server",
    )
    execute_parser.add_argument("cmd", help="The command to execute", metavar="CMD")
