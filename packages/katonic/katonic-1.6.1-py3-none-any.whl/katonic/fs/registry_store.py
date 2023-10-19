#!/usr/bin/env python
#
# Copyright (c) 2023 Katonic Pty Ltd. All rights reserved.
#
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Tuple

from katonic.fs.registry import Registry


class RegistryStore(ABC):
    """
    A registry store is a storage backend for the feature store registry.
    """

    @abstractmethod
    def create_registry(self, table_query: str, index_query: str) -> Registry:
        """
        Creates the registry in PostgreSQL database depending on the backend.

        Args:
            table_query: table query string to create a new table in the database.
            index_query: index query string to create index for the new table in the database.
        """
        pass

    @abstractmethod
    def get_registry(self, get_query: str) -> Registry:
        """
        Retrieves the registry from the registry path. If there is no file at that path,
        raises a FileNotFoundError.

        Args:
            get_query: table query string to create a new table in the database.
        Returns:
            Returns either the registry table stored at the registry path, or an empty registry table.
        """
        pass

    @abstractmethod
    def update_registry(
        self, update_query: Tuple[str, Any], insert_query: Tuple[str, Any]
    ):
        """
        Overwrites the current registry with the table passed in. This method
        writes to the registry path.

        Args:
            registry: the new Registry
        """
        pass

    @abstractmethod
    def teardown(self):
        """
        Tear down the registry.
        """
        pass
