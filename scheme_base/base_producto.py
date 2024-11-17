from pydantic import BaseModel

class UploadProducto(BaseModel):
    nombreProducto: str | None = None
    descripcion: str | None = None
    precioUnitario: float | None = None
    imagen: str | None = None