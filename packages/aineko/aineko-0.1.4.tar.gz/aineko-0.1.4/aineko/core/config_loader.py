# Copyright 2023 Aineko Authors
# SPDX-License-Identifier: Apache-2.0
"""Module to load config files."""
from typing import Union, overload

from schema import Optional as optional  # type: ignore
from schema import Schema, SchemaError  # type: ignore

from aineko.config import AINEKO_CONFIG
from aineko.utils.io import load_yamls


class ConfigLoader:
    """Class to read yaml config files.

    Args:
        pipeline_config_file: path of pipeline config file. Defaults
        to DEFAULT_CONF_SOURCE.

    Attributes:
        pipeline_config_file (str): path to pipeline configuration file
        config_schema (Schema): schema to validate config against

    Methods:
        load_config: load config for project(s) from yaml files
        validate_config: validate config against config_schema
    """

    def __init__(
        self,
        pipeline_config_file: str,
    ):
        """Initialize ConfigLoader."""
        self.pipeline_config_file = pipeline_config_file or AINEKO_CONFIG.get(
            "DEFAULT_PIPELINE_CONFIG"
        )

        # Setup config schema
        self.config_schema = Schema(
            {
                # Pipeline config
                "pipeline": {
                    "name": str,
                    optional("default_node_settings"): dict,
                    # Node config
                    "nodes": {
                        str: {
                            "class": str,
                            optional("node_params"): dict,
                            optional("node_settings"): dict,
                            optional("inputs"): list,
                            optional("outputs"): list,
                        },
                    },
                    # Datasets config
                    "datasets": {
                        str: {
                            "type": str,
                            optional("params"): dict,
                        },
                    },
                },
            },
        )

    def load_config(self) -> dict:
        """Load config for project(s) from yaml files.

        Load the config from the specified pipeline config.
        Example:
                {
                    "pipeline": {
                        "name": ...,
                        "nodes": {...},
                        "datasets": {...}
                    },
                }

        Raises:
            ValueError: If project is not a string or list of strings

        Returns:
            Config for each project (dict keys are project names)
        """
        config = load_yamls(self.pipeline_config_file)

        try:
            self._validate_config_schema(pipeline_config=config)
        except SchemaError as e:
            raise SchemaError(
                f"Schema validation failed for pipeline "
                f"`{config['pipeline']['name']}`."
                f"Config files loaded from {self.pipeline_config_file} "
                f"returned {config}."
            ) from e

        return config

    def _validate_config_schema(self, pipeline_config: dict) -> bool:
        """Validate config.

        Note:
        e.g. schema -
        {
            "pipeline": {
                "name": str,
                "nodes": dict,
                "datasets": dict,
            }
        }

        For more information on schema validation,
        see: https://github.com/keleshev/schema

        Args:
            pipeline_config: config to validate

        Raises:
            SchemaError: if config is invalid

        Returns:
            True if config is valid
        """
        self.config_schema.validate(pipeline_config)
        return True

    @overload
    def _update_params(self, value: dict, params: dict) -> dict:
        ...

    @overload
    def _update_params(self, value: list, params: dict) -> list:
        ...

    @overload
    def _update_params(self, value: str, params: dict) -> str:
        ...

    @overload
    def _update_params(self, value: int, params: dict) -> int:
        ...

    def _update_params(
        self, value: Union[dict, list, str, int], params: dict
    ) -> Union[dict, list, str, int]:
        """Update value with params.

        Recursively calls the method if value is a list or dictionary until it
        reaches a string or int. If string then formats the str with variable
        mapping in params dict.

        Args:
            value: value to update
            params: params to update value with

        Returns:
            object with updated values (dict, list, str, or int)
        """
        if isinstance(value, dict):
            new_dict_val = {}
            for key, val in value.items():
                new_dict_val[key] = self._update_params(val, params)
            return new_dict_val
        if isinstance(value, list):
            new_list_val: list = []
            for val in value:
                new_list_val.append(self._update_params(val, params))
            return new_list_val
        if isinstance(value, str):
            for key, val in params.items():
                value = value.replace(f"${key}", val)
            return value
        if isinstance(value, (int, float)):
            return value
        raise ValueError(
            f"Invalid value type {type(value)}. "
            "Expected dict, list, str, or int."
        )
