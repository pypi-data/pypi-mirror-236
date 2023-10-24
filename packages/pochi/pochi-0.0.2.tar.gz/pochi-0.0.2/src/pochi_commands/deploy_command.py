import os
from pochi_commands.pochi_util import pochi_util

class DeployCommand(object):
    def __init__(self, parser):
        # print('deploy command')
        deploy_parser = parser.add_parser("deploy", help="Deploy as provider or consumer")
        deploy_parser.add_argument("--provider", action="store_true", help="Deploy as a provider")
        deploy_parser.add_argument("--consumer", action="store_true", help="Deploy as a consumer")

    def get_help_text(self):
        help_text = """pochi deploy [--consumer|--provider]
    Create an application package and generate a new version/patch in the target Snowflake account specified in config/project.toml.
    This command automatically runs the build command, and then executes the deployment SQL scripts to create an Application Package,
    set up shared content, push application code into a stage, and add a version/patch.
        
    Options:
        --consumer                      Updates only the native app application code files and creates a new patch.
        --provider                      Updates only the native app package or other objects in the provider account.
"""
        return help_text

    def execute(self, options):
        pochi_util.get_connection(options)
        
        if options.deploy.consumer:
            print("Deploying as a consumer")
            pochi_util.execute_sql_from_file("Deploying Application Code",
                os.path.join("generated", "deployment", "deploy_versioned_code.sql")
                )
            
            pochi_util.execute_sql_from_file("Deploying Postinstall Commands",
                os.path.join("generated", "deployment", "deploy_postinstall_objects.sql"))
        elif options.deploy.provider:
            print("Deploying as a provider")
            pochi_util.execute_sql_from_file("Deploying Preinstall Commands",
            os.path.join("generated", "deployment", "deploy_preinstall_objects.sql"))
            
            pochi_util.execute_sql_from_file("Deploying Application Package",
                os.path.join("generated", "deployment", "deploy_application_package.sql"))
        else:
            print("Deploying")
            pochi_util.execute_sql_from_file("Deploying Preinstall Commands",
            os.path.join("generated", "deployment", "deploy_preinstall_objects.sql"))
            
            pochi_util.execute_sql_from_file("Deploying Application Package",
                os.path.join("generated", "deployment", "deploy_application_package.sql"))
            
            pochi_util.execute_sql_from_file("Deploying Application Code",
                os.path.join("generated", "deployment", "deploy_versioned_code.sql")
                )
            
            pochi_util.execute_sql_from_file("Deploying Postinstall Commands",
                os.path.join("generated", "deployment", "deploy_postinstall_objects.sql"))
        
