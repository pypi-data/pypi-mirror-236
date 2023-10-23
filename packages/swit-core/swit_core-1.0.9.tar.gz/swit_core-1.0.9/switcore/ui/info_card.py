from pydantic import BaseModel

from switcore.ui.item import Item


class InfoCard(BaseModel):
    type: str = 'info_card'
    items: list[Item]
    action_id: str | None = None
    draggable: bool = False
