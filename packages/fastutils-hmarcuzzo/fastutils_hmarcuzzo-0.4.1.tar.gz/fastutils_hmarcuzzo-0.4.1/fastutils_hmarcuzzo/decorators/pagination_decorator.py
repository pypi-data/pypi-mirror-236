from typing import TypeVar

from starlette.requests import Request

from fastutils_hmarcuzzo.types.find_many_options import FindManyOptions
from fastutils_hmarcuzzo.utils.pagination_utils import PaginationUtils

E = TypeVar("E")


class GetPagination(object):
    def __call__(self, request: Request) -> FindManyOptions:
        paging_params = PaginationUtils.generate_paging_parameters(request)

        return PaginationUtils.get_paging_data(paging_params)
