import os
import shutil
import logging
import glob
from pathlib import Path

class BuildCommand(object):
    def __init__(self, parser):
        # print('build command')
        parser.add_parser("build", help="Build")

    def get_help_text(self):
        help_text = """pochi build
    Build and generate Snowflake artifacts that can be deployed to a Snowflake account. Files are staged in generated/ folder.
"""
        return help_text
    def __refresh_output_folder(self):
        if os.path.exists("generated"):
            shutil.rmtree("generated")

        logging.info("--- Creating Output Directory ---")
    
        # Create necessary directories
        os.makedirs(os.path.join("generated", "app", "sql"), exist_ok=True)
        os.makedirs(os.path.join("generated", "deployment"), exist_ok=True)

        logging.info("Output directory created " + os.path.abspath("generated"))
        logging.info("")
    
    def __read_sql_files(self, src_dir):
        sql_files = glob.glob(os.path.join(src_dir, "*.sql"))
        consolidated_output = ""
        if sql_files:
            for sql_file in sql_files:
                with open(sql_file, "r") as sql_input:
                    consolidated_output = consolidated_output + sql_input.read() + "\n"
        return consolidated_output

    def __write_sql_file(self, sql_content, dest_sql_file):
        with open(dest_sql_file, "w") as sql_output:
            sql_output.write(sql_content)

    def execute(self, options):
        print("Building")
        self.__refresh_output_folder()

        # for preinstall files, consolidate all of the SQL files (ordered by file name) in the
        # src/provider/sql/preinstall directory into generated/deployment/deploy_preinstall_objects.sql
        preinstall_sql_commands = self.__read_sql_files(src_dir=os.path.join("src", "provider", "sql", "preinstall"))
        self.__write_sql_file(
            preinstall_sql_commands.format(application_package_name=options.project_config.application_package_name),
            dest_sql_file = os.path.join("generated", "deployment", "deploy_preinstall_objects.sql"))

        # for postinstall files, consolidate all of the SQL files (ordered by file name) in the
        # src/provider/sql/postinstall directory into generated/deployment/deploy_postinstall_objects.sql
        postinstall_sql_commands = self.__read_sql_files(src_dir=os.path.join("src", "provider", "sql", "postinstall"))
        self.__write_sql_file(
            postinstall_sql_commands.format(application_package_name=options.project_config.application_package_name),
            dest_sql_file = os.path.join("generated", "deployment", "deploy_postinstall_objects.sql"))

        # for app package definition files, consolidate all of the SQL files (ordered by file name) in the
        # src/provider/sql directory into generated/deployment/deploy_application_package.sql
        # PLUS: Add the CREATE APPLICATION PACKAGE line
        app_pkg_sql_commands = f"""
create application package if not exists {options.project_config.application_package_name};
use application package {options.project_config.application_package_name};
""" 
        app_pkg_sql_commands += self.__read_sql_files(src_dir=os.path.join("src", "provider", "sql"))
        self.__write_sql_file(
            app_pkg_sql_commands.format(application_package_name=options.project_config.application_package_name),
            dest_sql_file = os.path.join("generated", "deployment", "deploy_application_package.sql"))




        # Compose the application code directory inside "generated/app" folder.
        # 1. Copy all the resource files (recursively) into generated/app directory
        # This should include the README.md, the manifest.yml, or any other additional resources
        # such as ML models, test data, zip files, images, etc.
        shutil.copytree(os.path.join("src", "consumer", "resources"),
                        os.path.join("generated", "app"), dirs_exist_ok=True)


        # 2. Copy all the files in the src/consumer/python directory (recursively) into generated/app/python directory
        if len(os.listdir(os.path.join("src", "consumer", "python")))>0:
            shutil.copytree(os.path.join("src", "consumer", "python"),
                        os.path.join("generated", "app", "python"), dirs_exist_ok=True)


        # 3. Copy all the subdirectories in the src/consumer/sql directory (recursively) into generated/app directory
        # The purpose is to support the scenario where the project has subfolders inside the src/consumer/sql directory,
        # eg to include streamlit folders, additional SQL files that should be loaded dynamically, etc.
        src_directory = os.path.join("src", "consumer", "sql")
        target_directory = os.path.join("generated", "app")
        for root, _, files in os.walk(src_directory):
            if files:
                # Extract the relative path of the current directory
                relative_path = os.path.relpath(root, src_directory)
                           
                # Create the destination directory path
                dest_path = os.path.join(target_directory, relative_path)
            
                # Copy the entire directory to the destination
                shutil.copytree(root, dest_path, dirs_exist_ok=True)


        # 4. for app code definition (i.e. setup script), consolidate all of the SQL files (ordered by file name) in the
        # src/consumer/sql directory into generated/app/sql/setup.sql
        app_setup_sql_commands = self.__read_sql_files(src_dir=os.path.join("src", "consumer", "sql"))
        self.__write_sql_file(
            app_setup_sql_commands,
            dest_sql_file = os.path.join("generated", "app", "sql", "setup.sql"))

        # 5. Generate a deployment SQL to perform the following:
        # (a) CREATE STAGE to store the application version files
        # (b) PUT statements to upload all of the files in generated/app directory into the stage
        # (c) ALTER APPLICATION PACKAGE statement to create a new version or add a patch to an existing version using
        #     the stage in (a)

        deploy_app_code_commands = f"""

create schema if not exists {options.project_config.application_package_name}.sourcecode;
create stage if not exists {options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name};

"""

        upload_sql = ""
        for root, _, files in os.walk(os.path.join("generated", "app")):
            for file in files:
                file_path = os.path.join(root, file)
                full_path = os.path.abspath(file_path)
                relative_path = os.path.relpath(file_path, os.path.join("generated", "app"))

                # To support windows clients, we need to convert relative path to posix version for stage/path
                relative_path = Path(relative_path).as_posix()
                # Since relative_path contains the file name, which we don't need for the PUT command, remove the file name
                relative_path = relative_path.rstrip(file)
                #print(relative_path)
                upload_sql += f"PUT 'file://{full_path}' @{options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name}/{relative_path} auto_compress=false overwrite=true;\n"

        deploy_app_code_commands += upload_sql
        deploy_app_code_commands += f"""
----------------------------------------------------------------------------------------------------------------
-- Create a new version or a new patch for an existing version using the files uploaded in the named stage.
-- To change the application package name or the version name, edit config/project.config, and your changes will
-- automatically propagate throughout the generated SQL files.
--
-- See Docs:
-- https://docs.snowflake.com/en/developer-guide/native-apps/versioning
-- https://docs.snowflake.com/en/sql-reference/sql/alter-application-package-version
----------------------------------------------------------------------------------------------------------------
execute immediate $$
declare
  QUERY_RESULT_NUMBER integer;
begin
    show versions in application package {options.project_config.application_package_name};
    select count(*) into :QUERY_RESULT_NUMBER from table(result_scan(last_query_id())) where "version"=UPPER('{options.project_config.application_version_name}');
    
    if (QUERY_RESULT_NUMBER = 0) then
        alter application package {options.project_config.application_package_name}
            add version {options.project_config.application_version_name} using '@{options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name}';
        return '{options.project_config.application_package_name} added';
    else
        alter application package {options.project_config.application_package_name}
            add patch for version {options.project_config.application_version_name} using '@{options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name}';
        
        select "patch" into :QUERY_RESULT_NUMBER from table(result_scan(last_query_id()));
        return 'Version {options.project_config.application_version_name} Patch ' || QUERY_RESULT_NUMBER || ' added';
    end if;
end;
$$;
"""

        self.__write_sql_file(
            deploy_app_code_commands,
            dest_sql_file = os.path.join("generated", "deployment", "deploy_versioned_code.sql"))
        
        self.__write_sql_file(
            preinstall_sql_commands + app_pkg_sql_commands + deploy_app_code_commands + postinstall_sql_commands,
            dest_sql_file = os.path.join("generated", "deployment", "deploy_full.sql"))