from typing import Any, List, TypedDict, Optional, Dict


class FindOneOptions(TypedDict, total=False):
    select: List[str]
    where: Optional[List[Dict[str, Any] | bool]]
    order_by: Any
    relations: Any
