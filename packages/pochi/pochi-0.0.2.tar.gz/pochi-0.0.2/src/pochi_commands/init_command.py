import os
import shutil
import logging
import pochi_commands.constants as constants

class InitCommand(object):
    
    def __init__(self, parser):
        # print('init command')
        init_parser = parser.add_parser("init", usage="pochi init [--name=<folder_name>] [--version=<version_name>] [--connection=<connection_name] [--force]", description="Create a blank native app project with default folder structure and prebuilt templates in the current folder or in the folder specified with the --name option.",
            help=f"Creates a blank native app project with default folder structure and prebuilt templates in the current folder.\nIf the --name option is specified, create the folder and generate the project in it.")
        init_parser.add_argument("--name",nargs="?", help="Specify a folder name to create the project inside that folder.")
        init_parser.add_argument("--version",nargs="?", default="MyFirstVersion", help="Specify a version name; default is MyFirstVersion.")
        init_parser.add_argument("--connection",nargs="?", default="UnknownConnection", help="Specify a Snowflake connection; default is UnknownConnection")
        init_parser.add_argument("--force", action="store_true", help="Full init and overwrite any existing files")

    def get_help_text(self):
        help_text = """pochi init [--name=<folder_name>] [--version=<version_name>] [--connection=<connection_name] [--force]
    Creates a blank native app project with default directory structure and prebuilt templates in the current directory.
        
    Options:
        --name=<folder_name>            Create the blank native app project in a directory named <folder_name>
        --version=<version_name>        Override the default version name in config/project.toml
        --connection=<conn_name>        Override the default connection name in config/project.toml
        --force                         Overwrite an existing project directory with default templates
"""
        return help_text
    
    def execute(self, options):
        # print(f"Initializing with name: {options.init.name}")
        if options.init.name:
            # the user specified a name for the project; create a new folder with that name
            # and use the folder as the working directory
            os.makedirs(options.init.name, exist_ok=True)
            os.chdir(options.init.name)
        else:
            options.init.name = os.path.split(os.getcwd())[1]

        logging.info("============================================================================================")
        logging.info("--- Creating / Refreshing a Native App ---")

        if options.init.force == True:
            # delete all the files in the current directory
            try:
                # Remove all files and directories within the directory
                for root, dirs, files in os.walk(os.getcwd(), topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        shutil.rmtree(dir_path)
            except Exception as e:
                print(f"An error occurred: {e}")
        elif os.path.exists(os.path.join("config", "project.toml")):
            print("Project " + options.init.name +" already exists; use --force option to overwrite the project files")
            # return


        # Set up config folder
        if os.path.isdir('config')==False:
            os.makedirs("config", exist_ok=True)
            with open(os.path.join("config", "project.toml"), "w") as sql_output:
                sql_output.write(
                    constants.config_project_toml.format(
                            application_package_name=options.init.name,
                            application_version_name=options.init.version,
                            default_connection=options.init.connection)
                        )
            logging.info("Config files created in " + os.path.join(os.getcwd(), "config"))
        else:
            logging.info(os.path.join(os.getcwd(), "config") + " already exists, skipping...")

        # Set up server-side code folder (for App Package)
        if os.path.isdir(os.path.join("src", "provider"))==False:
            # os.makedirs(os.path.join("src", "provider", "java"), exist_ok=True)
            os.makedirs(os.path.join("src", "provider", "python"), exist_ok=True)
            os.makedirs(os.path.join("src", "provider", "sql"), exist_ok=True)
            os.makedirs(os.path.join("src", "provider", "sql", "preinstall"), exist_ok=True)
            os.makedirs(os.path.join("src", "provider", "sql", "postinstall"), exist_ok=True)

            with open(os.path.join("src", "provider", "sql", "app_pkg_definition_01.sql"), "w") as sql_output:
                sql_output.write(
                    # constants.provider_app_pkg_definition_sql.format(
                    #         application_package_name=options.init.name)
                    constants.provider_app_pkg_definition_sql
                        )

            with open(os.path.join("src", "provider", "sql", "preinstall", "preinstall_definition_01.sql"), "w") as sql_output:
                sql_output.write(
                    # constants.provider_preinstall_definition_sql.format(
                    #         application_package_name=options.init.name)
                    constants.provider_preinstall_definition_sql
                        )
            with open(os.path.join("src", "provider", "sql", "postinstall", "postinstall_definition_01.sql"), "w") as sql_output:
                sql_output.write(
                    # constants.provider_postinstall_definition_sql.format(
                    #         application_package_name=options.init.name)
                    constants.provider_postinstall_definition_sql
                        )

            logging.info(f"Source files for provider code created in " + os.path.join(os.getcwd(),"src", "provider"))
        else:
            logging.info(os.path.join(os.getcwd(),"src", "provider") + " already exists, skipping...")

        # Set up client-side code folder (for App Version / App Instance)
        if os.path.isdir(os.path.join("src", "consumer"))==False:
            # os.makedirs(os.path.join("src", "consumer", "java"), exist_ok=True)
            os.makedirs(os.path.join("src", "consumer", "python"), exist_ok=True)
            os.makedirs(os.path.join("src", "consumer", "resources"), exist_ok=True)
            os.makedirs(os.path.join("src", "consumer", "sql"), exist_ok=True)

            with open(os.path.join("src", "consumer", "sql", "app_setup_definition_01.sql"), "w") as sql_output:
                sql_output.write(
                    constants.consumer_app_definition_sql.format(
                            application_package_name=options.init.name)
                        )

            with open(os.path.join("src", "consumer", "resources", "manifest.yml"), "w") as sql_output:
                sql_output.write(
                    constants.consumer_manifest_yml.format(
                            application_package_name=options.init.name)
                        )

            with open(os.path.join("src", "consumer", "resources", "README.md"), "w") as sql_output:
                sql_output.write(
                    constants.consumer_readme.format(
                            application_package_name=options.init.name)
                        )

            # shutil.copytree(MOCHI_HOME + '/client_template', f'src/consumer')
            logging.info(f"Source files for consumer code created in " + os.path.join(os.getcwd(), "src", "consumer"))
        else:
            logging.info(os.path.join(os.getcwd(), "src", "consumer") + " already exists, skipping...")

        if os.path.isdir('test')==False:
            os.makedirs(os.path.join("test", "testsuite1"), exist_ok=True)
            with open(os.path.join("test", "testsuite1", "setup.sql"), "w") as sql_output:
                sql_output.write(constants.test_setup_sql)

            with open(os.path.join("test", "testsuite1", "teardown.sql"), "w") as sql_output:
                sql_output.write(constants.test_teardown_sql)

            with open(os.path.join("test", "testsuite1", "test01.sql"), "w") as sql_output:
                sql_output.write(constants.test_code_sql)

            logging.info("Test SQL files for application package created in " + os.path.join(os.getcwd(), "test"))
        else:
            logging.info(os.path.join(os.getcwd(), "test") + " already exists, skipping...")

        if os.path.isfile('README.md')==False:
            with open("README.md", "w") as sql_output:
                sql_output.write(constants.project_readme.format(application_package_name = options.init.name))
            logging.info("Default README.md generated at " + os.path.join(os.getcwd(), "README.md"))
        else:
            logging.info(os.path.join(os.getcwd(), "README.md") + " already exists, skipping...")

        logging.info("--------------------------------------------------------------------------------------------")
        logging.info("INIT SUCCESS")
        logging.info("--------------------------------------------------------------------------------------------")
