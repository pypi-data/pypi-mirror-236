"""Model of TTException"""
from pydantic import BaseModel
from typing import Optional

from trustedtwin_utils.models.tt_subcodes import SubCodes


class TTExceptionBodyResponse(BaseModel, extra='forbid'):
    """Model of body returned by API exception"""

    subcode: SubCodes
    trace: str
    description: Optional[str] = None
    help: Optional[str] = None
