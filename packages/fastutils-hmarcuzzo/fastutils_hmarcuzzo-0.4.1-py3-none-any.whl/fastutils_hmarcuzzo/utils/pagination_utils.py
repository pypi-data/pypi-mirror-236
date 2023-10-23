from typing import TypeVar

from starlette.requests import Request

from fastutils_hmarcuzzo.types.find_many_options import FindManyOptions
from fastutils_hmarcuzzo.types.pagination import Pagination


E = TypeVar("E")


class PaginationUtils:
    @staticmethod
    def generate_paging_parameters(request: Request) -> Pagination:
        request_params = request.query_params
        page = request_params.get("page")
        size = request_params.get("size")

        if page is None or size is None:
            raise ValueError("Pagination params not found")

        return Pagination(skip=int(page), take=int(size))

    @staticmethod
    def get_paging_data(
        paging_params: Pagination,
    ) -> FindManyOptions:
        paging_data = FindManyOptions(
            skip=(paging_params["skip"] - 1) * paging_params["take"],
            take=paging_params["take"],
        )

        return paging_data
