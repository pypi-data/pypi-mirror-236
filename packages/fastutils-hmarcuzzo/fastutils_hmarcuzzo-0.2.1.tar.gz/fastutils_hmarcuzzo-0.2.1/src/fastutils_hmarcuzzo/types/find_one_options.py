from typing import Any, List, TypedDict, Optional


class FindOneOptions(TypedDict, total=False):
    select: List[str]
    where: Optional[Any]
    order_by: Any
    relations: Any
