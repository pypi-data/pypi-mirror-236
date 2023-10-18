from typing import Optional, List, Dict, Union, Any

from utils.exception import DjangoWebException

DATATYPE = Optional[Union[List, Dict]]
ERRTYPE = Optional[DjangoWebException]
BODYTYPE = Dict[str, Any]
