import argparse
import sys
from pochi_commands.test_command import TestCommand
from pochi_commands.init_command import InitCommand
from pochi_commands.build_command import BuildCommand
from pochi_commands.deploy_command import DeployCommand
from pochi_commands.clean_command import CleanCommand
from pochi_commands.config_command import ConfigCommand
import toml
import os
import configparser
from pathlib import Path
import logging


class PochiCommandManager(object):
    def __init__(self):
        self.__parser = argparse.ArgumentParser(add_help=False)
        self.__subparsers = self.__parser.add_subparsers(title="Available Targets")
        self.__subparsers.add_parser("help", help="Display Help")

        self.__init_command = InitCommand(self.__subparsers)
        self.__config_command = ConfigCommand(self.__subparsers)
        self.__build_command = BuildCommand(self.__subparsers)
        self.__clean_command = CleanCommand(self.__subparsers)
        self.__deploy_command = DeployCommand(self.__subparsers)
        self.__test_command = TestCommand(self.__subparsers)

    def __get_help_text(self):
        help_text = """usage:
    pochi init [--name=<folder_name>] [--version=<version_name>] [--connection=<connection_name] [--force]
    pochi config --name=<parameter_name> --value=<parameter_value>
    pochi [ clean ] [ build ] [ deploy [--consumer|--provider] ] [ test ]

Pochi is a CLI tool for building, deploying and testing Snowflake native applications. You can include multiple targets,
and pochi always runs the targets in the following order: init -> clean -> build -> deploy -> test

eg:
pochi init --name=PochiProject --connection=MySnowflakeAccount deploy test

The above command creates a project folder named PochiProject, builds the project, creates the application package PochiProject
in the MySnowflakeAccount, and executes the basic test.

Targets:
"""
        return help_text

    def __print_help_text(self):
        print(self.__get_help_text())
        print(self.__init_command.get_help_text())
        print(self.__config_command.get_help_text())
        print(self.__clean_command.get_help_text())
        print(self.__build_command.get_help_text())
        print(self.__deploy_command.get_help_text())
        print(self.__test_command.get_help_text())
        
    def __parse_user_command_arguments(self, arguments):
        # Divide argv by commands
        split_argv = [[]]
        for c in arguments:
            if c in self.__subparsers.choices:
                split_argv.append([c])
            else:
                split_argv[-1].append(c)
        # Initialize namespace
        args = argparse.Namespace()
        for c in self.__subparsers.choices:
            setattr(args, c, None)
        # Parse each command
        self.__parser.parse_args(split_argv[0], namespace=args)  # Without command
        for argv in split_argv[1:]:  # Commands
            n = argparse.Namespace()
            setattr(args, argv[0], n)
            self.__parser.parse_args(argv, namespace=n)

        setattr(args, "project_config", self.__load_config_files())
        return args
    
    def __load_config_files(self):
        # Step 1: Process the config/project.toml file
        # If the file does not exist, then this folder is not initialized. Return None
        project_config_file_path = os.path.join("config", "project.toml")

        if os.path.exists(project_config_file_path):
            project_config_data = toml.load(os.path.join("config", "project.toml"))
        else:
            # config/project.toml not found; so there's no app pkg name, no version, no connectio name
            return None

        project_config = argparse.Namespace()
        setattr(project_config, "application_package_name", project_config_data.get("application_package_name"))
        setattr(project_config, "application_version_name", project_config_data.get("application_version_name"))
        setattr(project_config, "default_connection", project_config_data.get("default_connection"))

        # Step 2: Load the Snowflake connections files to look up the project's connection target
        # Snowflake has multiple configs that can be loaded:
        # (1) $SNOWFLAKE_HOME/connections.toml (if $SNOWFLAKE_HOME exists)
        # (2) ~/.snowflake/connections.toml (if it exists)
        # (3) ~/.snowsql/config (regular config file, not TOML)
        # There may be other locations but Pochi only supports the above 3 locations at this point.

        snowflake_home_directory = os.getenv("SNOWFLAKE_HOME", Path.home())
        connections_toml = os.path.join(snowflake_home_directory, "connections.toml")
        snowsql_config = os.path.join(Path.home(), ".snowsql", "config")

        connection_config = None
        connection_config_namespace = None
        if os.path.exists(connections_toml):
            # Found the SnowCLI connection toml file; load it!
            connection_config_namespace = argparse.Namespace()
            connection_config = toml.load(connections_toml)
        elif os.path.exists(snowsql_config):
            # Found the SnowSQL config file!
            connection_config_namespace = argparse.Namespace()
            connection_config = configparser.ConfigParser()
            connection_config.read(snowsql_config)

        try:
            default_connection_config = connection_config[project_config_data["default_connection"]]
            for parameter in default_connection_config:
                setattr(connection_config_namespace, parameter, default_connection_config[parameter])
        except Exception as e:
            logging.warn("Invalid config parameter: default_connection " + project_config_data["default_connection"] + " is not a valid connection name.")

        # set default_connection to the connection details, or None if no connection config file found
        setattr(project_config, "default_connection", connection_config_namespace)

        return project_config


    def execute_commands(self, arguments):
        args = self.__parse_user_command_arguments(arguments)

        if args.help != None:
            self.__print_help_text()
            # self.__help_command.execute(args)
            sys.exit(0)

        if args.init != None:
            self.__init_command.execute(args)
            sys.exit(0)
       
        if args.config!=None:
            self.__config_command.execute(args)
            sys.exit(0)

        if args.clean != None:
            self.__clean_command.execute(args)

        if args.build != None:
            self.__build_command.execute(args)

        if args.deploy != None:
            if args.build==None:
                self.__build_command.execute(args)
            self.__deploy_command.execute(args)

        if args.test != None:
            self.__test_command.execute(args)