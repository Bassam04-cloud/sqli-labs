```python
"""
Centralized MySQL connection for SQLi-Labs.
Supports local Docker and Aiven MySQL connections.
"""

import os
import mysql.connector
from mysql.connector import pooling

_pool = None


def get_pool():
    global _pool

    if _pool is None:
        config = {
            "pool_name": "sqlilabs_pool",
            "pool_size": 5,
            "host": os.getenv("DB_HOST", "db"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "sqlilabs"),
            "autocommit": True,
        }

        if os.getenv("DB_SSL", "false").lower() == "true":
            config["ssl_disabled"] = False
            config["ssl_verify_cert"] = True
            config["ssl_verify_identity"] = True
            config["ssl_ca"] = os.getenv("DB_SSL_CA")

        _pool = pooling.MySQLConnectionPool(**config)

    return _pool


def get_conn():
    return get_pool().get_connection()
```
