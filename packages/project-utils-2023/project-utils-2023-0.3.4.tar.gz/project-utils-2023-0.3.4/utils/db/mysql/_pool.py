from typing import Any, Optional

from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from dbutils.steady_db import SteadyDBConnection

from ._collection import MysqlCollection
from ._result import MysqlResult


class MysqlPool(MysqlCollection):
    pool: Optional[PooledDB] = None

    def __init__(self, creator: Any, *args, **kwargs):
        super().__init__(max_connections=10, min_cached=5, max_cached=10, max_shared=10)
        if self.pool is None:
            self.pool = PooledDB(
                creator,
                self.min_cached,
                self.max_cached,
                self.max_shared,
                self.max_connections,
                self.blocking,
                setsession=self.set_session,
                ping=self.ping,
                *args, **kwargs
            )

    def running(self, sql: str, data: Any = None, many: bool = False) -> MysqlResult:
        conn: SteadyDBConnection = self.pool.connection()
        cursor: DictCursor = conn.cursor(DictCursor)
        result: MysqlResult = self.execute(conn, cursor, sql, data, many)
        return result
