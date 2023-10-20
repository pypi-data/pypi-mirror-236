from attrs import define, field
from collections import defaultdict
from sqlalchemy import create_engine, text, TextClause
from itertools import product
import numpy as np
from typing import Optional, Iterable, Tuple, List
import os
from volstreet import timeit
import pandas as pd


@define
class DBManager:
    # Database attributes
    _DB_NAME: str = field(default=None)
    _DB_USER: str = field(default=None)
    _DB_PASS: str = field(default=None)
    _DB_HOST: str = field(default=None)
    _DB_PORT: str = field(default=None)
    _database_connection_url: str = field(default=None)
    _alchemy_engine_url: str = field(default=None)

    # SQLAlchemy engine
    alchemy_engine = field(default=None, init=False)

    # Storing queries to see if caching is possible
    _queries: defaultdict = field(factory=lambda: defaultdict(list), init=False)

    def __attrs_post_init__(self):
        self._set_db_credentials()
        self._set_database_connection_urls()

    @staticmethod
    def _get_env_var(var_name: str):
        """Fetch environment variables safely."""
        var_value = os.getenv(var_name)
        if var_value is None:
            raise EnvironmentError(f"Environment variable '{var_name}' is not set.")
        return var_value

    def _set_db_credentials(self):
        self._DB_NAME = self._get_env_var("TSDB_DBNAME")
        self._DB_USER = self._get_env_var("TSDB_USER")
        self._DB_PASS = self._get_env_var("TSDB_PASS")
        self._DB_HOST = self._get_env_var("TSDB_HOST")
        self._DB_PORT = self._get_env_var("TSDB_PORT")

    def _set_database_connection_urls(self):
        self._database_connection_url = (
            f"postgres://{self._DB_USER}:{self._DB_PASS}@{self._DB_HOST}:"
            f"{self._DB_PORT}/{self._DB_NAME}?sslmode=require"
        )
        self._alchemy_engine_url = self._database_connection_url.replace(
            "postgres", "postgresql"
        )

    def set_alchemy_engine(self):
        self.alchemy_engine = create_engine(self._alchemy_engine_url)

    def get_executed_queries(self):
        return self._queries

    @staticmethod
    def generate_sql_query_for_option_prices(
        cols_to_return: Optional[Iterable[str]] = None,
        specific_timestamps: Optional[Iterable[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        indices: Optional[str | Iterable[str]] = None,
        strike: Optional[int | str | float | Iterable[int | float]] = None,
        time_range: Optional[Tuple[str, str]] = None,
    ) -> str:
        """
        Generate an SQL query based on the provided arguments.

        Parameters:
        - cols_to_return: Columns to return from the SQL query
        - start_time: Start time for the timestamp filter (Optional)
        - end_time: End time for the timestamp filter (Optional)
        - indices: Indices to filter (either a single index as a string or a list of indices) (Optional)
        - strike: Strike prices to filter (either a single strike price or a list of strike prices) (Optional)
        - time_range: Time range within each day to filter for (Optional). Format: ('HH:MM', 'HH:MM')

        Returns:
        - SQL query as a string
        """

        if cols_to_return is None:
            cols_to_return = ["timestamp", "expiry", "strike", "option_type", "close"]

        # Convert columns to a comma-separated string
        columns_str = ", ".join(cols_to_return)

        # Initialize WHERE clauses
        where_clauses = []

        # Timestamp filtering
        if start_time and end_time:
            where_clauses.append(f"timestamp BETWEEN '{start_time}' AND '{end_time}'")

        # Time range filtering within each day
        if time_range:
            start_time_of_day, end_time_of_day = time_range
            where_clauses.append(
                f"(EXTRACT(HOUR FROM timestamp) * 60 + EXTRACT(MINUTE FROM timestamp)) BETWEEN \
                                 (EXTRACT(HOUR FROM TIME '{start_time_of_day}') * 60 + EXTRACT(MINUTE FROM TIME '{start_time_of_day}')) AND \
                                 (EXTRACT(HOUR FROM TIME '{end_time_of_day}') * 60 + EXTRACT(MINUTE FROM TIME '{end_time_of_day}'))"
            )

        # Specific Timestamps filtering
        if specific_timestamps:
            specific_timestamps_placeholder = ", ".join(
                [f"'{x}'" for x in specific_timestamps]
            )
            where_clauses.append(f"timestamp IN ({specific_timestamps_placeholder})")

        # Indices filtering
        if indices:
            indices_placeholder = (
                f"'{indices}'"
                if isinstance(indices, str)
                else ", ".join([f"'{x}'" for x in indices])
            )
            where_clauses.append(f"underlying IN ({indices_placeholder})")

        # Strike price filtering
        if strike:
            strike_placeholder = (
                f"{strike}"
                if isinstance(strike, (int, float, str))
                else ", ".join(map(str, strike))
            )
            where_clauses.append(f"strike IN ({strike_placeholder})")

        # Combine WHERE clauses
        where_clause_str = " AND ".join(where_clauses) if where_clauses else "1=1"

        # Generate the SQL query
        # noinspection SqlNoDataSourceInspection
        sql_query = f"""
        SELECT {columns_str}
        FROM index_options,
        WHERE {where_clause_str};
        """

        return sql_query

    @staticmethod
    def generate_query_for_option_prices(
        index: str,
        timestamps: List[str],
        expirys: List[str],
        strikes: List[Tuple[float, float]] | List[float],
        option_type: Optional[str] = None,
        cols_to_return: Optional[Iterable[str]] = None,
    ) -> TextClause:
        if cols_to_return is None:
            cols_to_return = ["timestamp", "expiry", "strike", "option_type", "close"]

        columns_str = ", ".join([f"index_options.{x}" for x in cols_to_return])

        # Create a Common Table Expression (CTE) to hold the specific timestamp, strike, and option_type combinations
        if not isinstance(strikes[0], (tuple, list)):
            assert (
                option_type is not None
            ), "Option type must be provided if single strikes are provided."

            cte_entries = ", ".join(
                [
                    f"('{timestamp}'::timestamp, {strike}::integer, '{expiry}'::text, '{option_type}'::text)"
                    for timestamp, expiry, strike in zip(timestamps, expirys, strikes)
                ]
            )
        else:
            cte_entries = ", ".join(
                [
                    f"('{timestamp}'::timestamp, {call_strike}::integer, '{expiry}'::text, 'CE'::text), "
                    f"('{timestamp}'::timestamp, {put_strike}::integer, '{expiry}'::text, 'PE'::text)"
                    for timestamp, expiry, (call_strike, put_strike) in zip(
                        timestamps, expirys, strikes
                    )
                ]
            )
        cte = f"WITH conditions AS (SELECT * FROM (VALUES {cte_entries}) AS t(timestamp, strike, expiry, option_type))"

        # Base query string
        sql_query = text(
            f"""
            {cte}
            SELECT {columns_str}
            FROM index_options
            INNER JOIN conditions
            ON index_options.timestamp = conditions.timestamp 
               AND index_options.expiry = conditions.expiry
               AND index_options.strike = conditions.strike
               AND index_options.option_type = conditions.option_type
            WHERE index_options.underlying = '{index}';
        """
        )

        return sql_query

    @staticmethod
    def generate_query_for_option_prices_product(
        index: str,
        timestamps: List[str],
        expirys: List[str],
        strikes: List[float | int],
        option_type: Optional[str] = None,
        cols_to_return: Optional[Iterable[str]] = None,
    ) -> TextClause:  # Changed return type to str as SQLAlchemy is not available
        if cols_to_return is None:
            cols_to_return = [
                "timestamp",
                "expiry",
                "strike",
                "option_type",
                "close",
            ]

        # Sanity run np.unique on timestamps, expirys, strikes, option_type
        timestamps = list(np.unique(timestamps))
        expirys = list(np.unique(expirys))
        strikes = list(np.unique(strikes))

        columns_str = ", ".join([f"index_options.{x}" for x in cols_to_return])

        # Convert strikes to int if its a float
        strikes = [
            int(strike) if isinstance(strike, float) else strike for strike in strikes
        ]

        # Generate all possible combinations of timestamp, expiry, and strike
        all_combinations = list(product(timestamps, strikes, expirys))

        cte_entries_list = []
        for timestamp, strike, expiry in all_combinations:
            if option_type:
                cte_entries_list.append(
                    (
                        timestamp,
                        strike,
                        expiry,
                        f"'{option_type}'::text",
                    )
                )
            else:
                cte_entries_list.extend(
                    [
                        (timestamp, strike, expiry, "'CE'::text"),
                        (timestamp, strike, expiry, "'PE'::text"),
                    ]
                )

        # Sort the conditions by timestamp and strike
        cte_entries_list.sort(key=lambda x: (x[0], x[1]))
        cte_entries = ", ".join(
            [
                f"('{timestamp}'::timestamp, {strike}::integer, '{expiry}'::text, {option_type})"
                for timestamp, strike, expiry, option_type in cte_entries_list
            ]
        )
        cte = f"WITH conditions AS (SELECT * FROM (VALUES {cte_entries}) AS t(timestamp, strike, expiry, option_type))"

        # Base query string
        sql_query = text(
            f"""
            {cte}
            SELECT {columns_str}
            FROM index_options
            INNER JOIN conditions
            ON index_options.timestamp = conditions.timestamp 
               AND index_options.expiry = conditions.expiry
               AND index_options.strike = conditions.strike
               AND index_options.option_type = conditions.option_type
            WHERE index_options.underlying = '{index}';
        """
        )

        return sql_query

    @timeit
    def fetch_option_prices_from_tsdb(self, query: str | TextClause) -> pd.DataFrame:
        """Fetch option prices from TimescaleDB using the provided query."""
        engine = create_engine(self._alchemy_engine_url)
        with engine.connect() as connection:
            option_prices = pd.read_sql(query, connection)

        # Store the query
        self._queries["index_options"].append(query)
        return option_prices
