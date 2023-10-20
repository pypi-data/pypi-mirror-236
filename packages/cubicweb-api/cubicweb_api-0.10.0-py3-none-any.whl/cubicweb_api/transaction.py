# copyright 2023-2023 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import Union, Dict, List

from cubicweb.rset import ResultSet
from typing_extensions import TypedDict, TypeGuard

from cubicweb.server.session import Connection


class QueryReference(TypedDict):
    queryIndex: int
    row: int
    column: int


QueryParams = Dict[str, Union[str, int, float, QueryReference]]


class Query(TypedDict):
    query: str
    params: Union[QueryParams, None]


class InvalidTransaction(Exception):
    pass


def is_query_reference(value: object) -> TypeGuard[QueryReference]:
    return isinstance(value, dict) and "queryIndex" in value


class Transaction:
    def __init__(self, queries: List[Query]):
        self.queries = queries

    def execute(self, cnx: Connection):
        rset_list: List[ResultSet] = []
        for query in self.queries:
            try:
                resolved_params = self.resolve_parameter_references(
                    query["params"], rset_list
                )
                rset = cnx.execute(query["query"], resolved_params)
            except Exception:
                cnx.rollback()
                raise
            rset_list.append(rset)
        cnx.commit()
        return rset_list

    @staticmethod
    def resolve_parameter_references(
        params: Union[QueryParams, None], rset_list: List[ResultSet]
    ) -> Union[Dict, None]:
        if not params:
            return None
        modified_params = params.copy()
        for key, value in params.items():
            if not is_query_reference(value):
                continue
            query_idx = value["queryIndex"]
            if query_idx >= len(rset_list):
                raise InvalidTransaction(
                    "A query reference index refers to a request which has not yet been executed"
                )
            if query_idx < 0:
                raise InvalidTransaction(
                    "A query reference index must be a natural integer."
                )
            row = value["row"]
            current_rset = rset_list[query_idx]
            if row < 0 or row >= len(current_rset):
                raise InvalidTransaction(
                    "A query reference row refers to an incorrect row number."
                )
            column = value["column"]
            if column < 0 or column >= len(current_rset[row]):
                raise InvalidTransaction(
                    "A query reference column refers to an incorrect column number."
                )
            modified_params[key] = rset_list[query_idx][row][column]
        return modified_params
