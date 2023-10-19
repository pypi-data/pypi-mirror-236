#!/usr/bin/env python
#
# Copyright (c) 2023 Katonic Pty Ltd. All rights reserved.
#
from typing import Optional

import psycopg2
from katonic.fs.repo_config import KfsConfigBaseModel
from pydantic.types import StrictStr


class PostgreSQLConfig(KfsConfigBaseModel):
    host: StrictStr
    port: int = 5432
    db_name: StrictStr
    db_schema: Optional[StrictStr] = None
    user: StrictStr
    password: StrictStr


def get_postgres_conn(config: PostgreSQLConfig):
    return psycopg2.connect(
        dbname=config.db_name,
        host=config.host,
        port=int(config.port),
        user=config.user,
        password=config.password,
        options=f"-c search_path={config.db_schema or config.user}",
    )
