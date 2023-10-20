import os
import pendulum
import pandas as pd
from sqlalchemy import create_engine


class SQLServer:
    """
    Pass in a conn string to generate the engine for querying
    Example: pd.read_sql(query, SQLServer(SERVER="EXAMPLE_SERVER_CONN_STRING").engine)
    
    SQLAlchemy EXAMPLE_SERVER_CONN_STRING Format:
    mssql+pyodbc://user:password@server-ip/database?driver=ODBC+Driver
    """
    def __init__(self, SQLSERVER_CONN_STR):
        self.engine = create_engine(os.getenv(SQLSERVER_CONN_STR))
        self.database = self.engine.url.database
        self.dialect = str(self.engine.url).split('+')[0]
        self.timestamp = pendulum.now(tz='Asia/Singapore').strftime('%Y-%m-%d %H:%M:%S %p')

    def read_with_timestamp(self, sql):
        df = pd.read_sql(sql, self.engine)
        df["updated_at"] = pd.to_datetime('now', utc=True).tz_convert('Asia/Singapore').strftime('%Y-%m-%d %H:%M:%S %p')
        return df