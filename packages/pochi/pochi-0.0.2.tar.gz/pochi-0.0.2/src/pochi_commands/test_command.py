import os
from pochi_commands.pochi_util import pochi_util

class TestCommand(object):
    def __init__(self, parser):
        # print('test command')
        parser.add_parser("test", help="Run tests")

    def get_help_text(self):
        help_text = """pochi test
    Run the all of the test suites defined in the test directory.
"""
        return help_text

    def execute(self, options):
        print("Running tests")
        pochi_util.get_connection(options)

        os.makedirs(os.path.join("generated", "test"), exist_ok=True)
        for testsuite in os.listdir("test"):
            # print(testsuite)
            if os.path.isdir(os.path.join("test", testsuite)):
                # this is the test suite.
                test_setup_sql = ""
                test_teardown_sql = ""
                test_code_sql = ""

                for file in os.listdir(os.path.join("test", testsuite)):
                    # print(file)
                    with open(os.path.join("test", testsuite, file), "r") as sql_input:
                        if (file =="setup.sql"):
                            test_setup_sql = sql_input.read() + "\n"
                            test_setup_sql = test_setup_sql.format(application_package_name = options.project_config.application_package_name, application_version_name = options.project_config.application_version_name)
                        elif (file == "teardown.sql"):
                            test_teardown_sql = sql_input.read() + "\n"
                            test_teardown_sql = test_teardown_sql.format(application_package_name = options.project_config.application_package_name, application_version_name = options.project_config.application_version_name)
                        elif (file.startswith("test")):
                            test_code_sql += test_code_sql + sql_input.read() + "\n"
                            test_code_sql = test_code_sql.format(application_package_name = options.project_config.application_package_name, application_version_name = options.project_config.application_version_name)
                
                test_suite_file = os.path.join("generated", "test", testsuite + ".sql")    
                with open(test_suite_file, "w") as sql_output:
                    sql_output.write(test_setup_sql + test_code_sql + test_teardown_sql)

                pochi_util.execute_sql_from_file("Running Test " + testsuite, test_suite_file)
