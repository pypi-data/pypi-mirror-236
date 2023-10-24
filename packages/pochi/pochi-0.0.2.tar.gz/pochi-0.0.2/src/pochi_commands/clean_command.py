from pochi_commands.pochi_util import pochi_util
import shutil
import os

class CleanCommand(object):
    def __init__(self, parser):
        # print('clean command')
        parser.add_parser("clean", help="Clean")

    def get_help_text(self):
        help_text = """pochi clean
    Drop deployed Application Package and remove generated files.
"""
        return help_text

    def execute(self, options):
        print("Cleaning")
        # (1) run DROP APPLICATION PACKAGE options.project_config.application_package_name
        pochi_util.get_connection(options)
        pochi_util.execute_sql("DROP APPLICATION PACKAGE IF EXISTS {application_package_name}".format(application_package_name = options.project_config.application_package_name))

        # (2) delete generated directory
        if os.path.exists("generated"):
            shutil.rmtree("generated")
        