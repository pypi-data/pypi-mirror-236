from pydantic import BaseModel, Field

from switcore.ui.interactive_image import InteractiveImage


class ImageGrid(BaseModel):
    type: str = "image_grid"
    images: list[InteractiveImage]
    column_count: int = Field(..., ge=2, le=3)
