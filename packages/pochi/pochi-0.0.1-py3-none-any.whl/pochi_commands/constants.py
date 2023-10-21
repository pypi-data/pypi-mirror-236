
test_setup_sql = """
-- SETUP SQL FILE
-- Use this file to include commands to configure your environment.
-- This file is run once in the test cycle. All other test<name>.sql files are run after.
-- For individiaul test setup/teardown, include them in the test<name>.sql file.
select 'TEST:SETUP';

drop application if exists {application_package_name}_Client;

create application {application_package_name}_Client from application package {application_package_name}
using version {application_version_name};
"""

test_teardown_sql = """
-- TEARDOWN SQL FILE
-- Use this file to include commands to clean your environment.
-- This file is run once in the test cycle, after all other test<name>.sql files are run.
-- For individiaul test setup/teardown, include them in the test<name>.sql file.
select 'TEST:TEARDOWN';

drop application if exists {application_package_name}_Client;

"""

test_code_sql = """
-- TEST SQL FILE
-- Use this file to include commands to test your code.
-- For individiaul test setup/teardown SQL commands, include them in this file.
-- Only Same-Account testing supported at this time.
select 'TEST:TEST';

"""

config_project_toml = """
application_package_name="{application_package_name}"
application_version_name="{application_version_name}"
default_connection="{default_connection}"

"""

provider_app_pkg_definition_sql = """
----------------------------------------------------------------------------------------------------------------
-- HOW TO USE THIS FILE
-- Define schema level objects that need to be defined in the application package (eg schemas, views, tables, etc)
-- These objects will be created in the Application Package object.
--
-- More details at https://docs.snowflake.com/en/sql-reference/sql/create-application-package
----------------------------------------------------------------------------------------------------------------
-- Default SQL file to create server-side objects in the Application Package

select 'DEFINING OBJECTS IN APPLICATION PACKAGE {application_package_name}';

-- By default, the Client App does not have access to any objects in the APPLICATION PACKAGE.
-- To make data objects in the APPLICATION PACKAGE available to the client app, you need to
-- grant them to a special object: "SHARE IN APPLICATION PACKAGE {application_package_name}".

-- SAMPLE SQL
-- GRANT USAGE ON SCHEMA <schema> TO SHARE IN APPLICATION PACKAGE {application_package_name};
-- GRANT SELECT ON TABLE <schema>.<table> TO SHARE IN APPLICATION PACKAGE {application_package_name};
-- GRANT SELECT ON VIEW <schema>.<view> TO SHARE IN APPLICATION PACKAGE {application_package_name};
"""

provider_preinstall_definition_sql = """
-- The files in the preinstall directory are run BEFORE the application package is created
-- Use this to create account-level objects like roles, databases, users, etc.
select 'Preinstall-Scripts';
"""

provider_postinstall_definition_sql = """
-- The files in the postinstall directory are run AFTER a new version or patch is created.
-- Use this to perform downstream configuration, such as setting release directive, creating a listing
-- etc.
select 'Postinstall-Scripts';
"""

project_readme = """
# Sample Project Readme

## what is it?
Add your module description here.

## Link to documentation
Link to your documentation.

## Code Samples.
Add code examples for the Library Module.

"""

consumer_app_definition_sql = """
-- Define your application code here.
-- 
-- You can create multiple SQL files, and when you run the build command,
-- all of the SQL files will be consolidated (by alphanumeric order of the file names)
-- into the application setup SQL script in the generated/app/sql directory.

select 'DEFINING CLIENT-SIDE OBJECTS IN APPLICATION';

-- To allow a customer access to objects defined in this file, each object (schema, UDF, Procedure, Views, Tables, etc)
-- must be explicitly granted to an APPLICATION ROLE
create application role if not exists APPOWNER;

-- Sample SQL for the GRANT statements
-- grant usage on schema <schema> to application role appowner;
-- grant usage on function <schema>.<function> to application role appowner;
-- grant usage on procedure <schema>.<procedure> to application role appowner;
"""

consumer_manifest_yml = """
manifest_version: 1
artifacts: # required
  readme: README.md
  setup_script: sql/setup.sql
  extension_code: true
configuration: # optional
  log_level: debug # optional (default: off)
  trace_level: always # optional (default: off)
"""

consumer_readme = """
# Welcome to Your Native App

## what is it?

Add your application description here.

## what's included?

Add details about the application assets
"""