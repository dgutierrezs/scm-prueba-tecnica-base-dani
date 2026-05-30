from sqlalchemy import Select, text
from fastapi import  HTTPException, status
from app.models import Item

def apply_filters(stmt: Select, filters: str | None) -> Select:
    """
    Aplica una cadena de filtros a un Select.

    TODO (candidato): sustituye esta implementación por una segura.
      - El input debe ser estructurado (JSON), no SQL crudo.
      - Whitelist de columnas resueltas contra el modelo ORM.
        Allowed fields: set[str] = {"id", "sku", "status", "warehouse_id", "created_at"}
      - Whitelist de operadores.
      - Valores siempre parametrizados.
      - 400 ante filtros inválidos.
    """


    if not filters:
        return stmt
    allowed_fields = {"id", "sku", "status", "warehouse_id", "created_at"}
    allowed_operators = {"=", "!=", ">", "<", "LIKE", "IN", "IS NOT"}
    for filter in filters:
        if filter.operator not in allowed_operators:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operador no permitido: {filter.operator}"
)
        if filter.field not in allowed_fields:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campo no permitido: {filter.field}"
)
        if filter.operator == "=":
            column = getattr(Item, filter.field)
            stmt = stmt.where(column == filter.value)
            
    return stmt
            

