import snowflake.connector
import os

class PochiUtil(object):
    def __init__(self):
        self.__connection = None

    def get_connection(self, options):
        try:
            if self.__connection is None:
                print("********************************* MAKING SNOWFLAKE CONNECTION **********************************")
                self.__connection = snowflake.connector.connect(
                    user=options.project_config.default_connection.username,
                    password=options.project_config.default_connection.password,
                    account=options.project_config.default_connection.accountname
                    )
        except snowflake.connector.Error as e:
            raise Exception(f"Snowflake connection error: {e}")
        # return self.__connection

    def execute_sql(self, sql_statement):
        print(sql_statement)
        cur = self.__connection.cursor().execute(sql_statement)
        print("[Status: " + self.__connection.get_query_status(cur.sfqid).name +"]\n")
        
    
    def execute_sql_from_file(self, heading, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as sql_file:
                print("******************* "+ heading.upper() + " *******************")
                for cur in self.__connection.execute_stream(sql_file, remove_comments=True):
                    print(cur.query)
                    print("[Status: " + self.__connection.get_query_status(cur.sfqid).name +"]\n")

pochi_util = PochiUtil()