from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Optional
from services.analytics_service import AnalyticsService
from core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analíticas Dashboard"])

@router.get("/summary")
async def get_dashboard_metrics(
    periodo: int = Query(30, description="Días hacia atrás para filtrar"),
    usuario_filtro: Optional[str] = Query(None, description="Filtro opcional por Nombre de Reclutador"),
    current_user = Depends(get_current_user)  # Retorna el objeto User de tu BD
):
    try:
        # CORRECCIÓN: Accedemos como atributo de objeto (.id o .organization)
        # en lugar de usar .get() como si fuera un diccionario.
        # Ajusta "organization_id" u "organization" según cómo se llame el atributo en tu modelo User.
        org_id = None

        if hasattr(current_user, "organization_id"):
            org_id = current_user.organization_id
        elif hasattr(current_user, "organization"):
            org_id = current_user.organization

        if not org_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario actual no cuenta con un identificador de organización válido o el atributo no existe."
            )

        # Si usuario_filtro es None, le pasamos un string vacío "" para el tipado
        nombre_usuario_seguro = usuario_filtro if usuario_filtro is not None else ""

        # Invocamos al servicio de analíticas
        data = await AnalyticsService.obtener_dashboard_summary(
            org_id=str(org_id),
            periodo_dias=periodo,
            usuario_nombre_filtro=nombre_usuario_seguro
        )
        return data

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error interno procesando analiticas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno procesando analiticas."
        )
