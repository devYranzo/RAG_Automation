import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from database import engine

class AnalyticsService:
    @staticmethod
    async def obtener_dashboard_summary(org_id: str, periodo_dias: int, usuario_nombre_filtro: str = ""):
        fecha_limite = datetime.now(timezone.utc) - timedelta(days=periodo_dias)

        filtros_sql = "WHERE organization_id = :org_id AND created_at >= :fecha_limite"
        params = {"org_id": str(org_id), "fecha_limite": fecha_limite}

        if usuario_nombre_filtro:
            filtros_sql += " AND usuario_nombre = :usuario_nombre"
            params["usuario_nombre"] = str(usuario_nombre_filtro)

        async with engine.connect() as conn:
            # 1. TARJETAS (Métricas Superiores)
            res_total = await conn.execute(text(f"SELECT count(*) FROM analytics_queries {filtros_sql}"), params)
            total_queries = res_total.scalar() or 0

            res_cache = await conn.execute(text(f"SELECT count(*) FROM analytics_queries {filtros_sql} AND cached = true"), params)
            cache_queries = res_cache.scalar() or 0
            hit_rate = int((cache_queries / total_queries) * 100) if total_queries > 0 else 0

            res_latencia = await conn.execute(text(f"SELECT avg(latencia) FROM analytics_queries {filtros_sql}"), params)
            latencia_media_raw = res_latencia.scalar()
            latencia_media = f"{float(latencia_media_raw):.2f}s" if latencia_media_raw else "0.00s"

            res_tokens_sum = await conn.execute(text(f"""
                SELECT COALESCE(SUM(tokens_input), 0) + COALESCE(SUM(tokens_output), 0)
                FROM analytics_queries {filtros_sql}
            """), params)
            total_tokens = res_tokens_sum.scalar() or 0

            # 2. GRÁFICO: Volumen Diario
            res_volumen = await conn.execute(text(f"""
                SELECT to_char(created_at, 'Dy') as dia, count(*)
                FROM analytics_queries
                {filtros_sql}
                GROUP BY to_char(created_at, 'Dy'), date_trunc('day', created_at)
                ORDER BY date_trunc('day', created_at) DESC LIMIT 7
            """), params)
            volumen_raw = res_volumen.fetchall()
            labels_vol = [row[0] for row in reversed(volumen_raw)] if volumen_raw else ["Sin datos"]
            values_vol = [row[1] for row in reversed(volumen_raw)] if volumen_raw else [0]

            # 3. GRÁFICO: Distribución de Tipo de Query
            res_tipos = await conn.execute(text(f"""
                SELECT
                    COUNT(CASE WHEN query ILIKE '%senior%' OR query ILIKE '%junior%' OR query ILIKE '%experiencia%' THEN 1 END) as exp,
                    COUNT(CASE WHEN query ILIKE '%developer%' OR query ILIKE '%engineer%' OR query ILIKE '%manager%' THEN 1 END) as cargo,
                    COUNT(*) as total
                FROM analytics_queries {filtros_sql}
            """), params)
            tipos_raw = res_tipos.fetchone()
            if tipos_raw and tipos_raw[2] is not None and tipos_raw[2] > 0:
                t_total = tipos_raw[2]
                pct_exp = int((tipos_raw[0] or 0) / t_total * 100)
                pct_cargo = int((tipos_raw[1] or 0) / t_total * 100)
                pct_tecnico = max(0, 100 - (pct_exp + pct_cargo))
            else:
                pct_exp, pct_cargo, pct_tecnico = 0, 0, 100

            # 4. TOKENS INPUT VS OUTPUT
            res_uso_tokens = await conn.execute(text(f"""
                SELECT COALESCE(SUM(tokens_input), 0), COALESCE(SUM(tokens_output), 0)
                FROM analytics_queries {filtros_sql}
            """), params)
            tokens_raw = res_uso_tokens.fetchone()
            tokens_data = {"input": tokens_raw[0] if tokens_raw else 0, "output": tokens_raw[1] if tokens_raw else 0}

            # 5. TABLA: Top Queries
            res_queries = await conn.execute(text(f"""
                SELECT query, usuario_nombre, skills_detectadas::text, count(*), avg(latencia), bool_or(cached), to_char(max(created_at), 'DD/MM HH:24')
                FROM analytics_queries {filtros_sql}
                GROUP BY query, usuario_nombre, skills_detectadas::text
                ORDER BY count(*) DESC LIMIT 6
            """), params)
            queries_list = []
            for idx, row in enumerate(res_queries.fetchall()):
                try:
                    skills_data = json.loads(row[2]) if row[2] else ["RAG"]
                except:
                    skills_data = ["RAG"]
                queries_list.append({
                    "id": idx + 1, "query": row[0], "usuario": row[1] or "Usuario General",
                    "skills": skills_data, "count": row[3] or 0, "score": float(row[4] or 0.0),
                    "cached": bool(row[5]), "ultima": row[6] or "Reciente"
                })

            # 6. MURO: Actividad Reciente (SOLUCIONADO EL ERROR DE VARIABLE NO DEFINIDA)
            res_actividad = await conn.execute(text(f"""
                SELECT id, usuario_nombre, query, created_at, resultados_count, latencia
                FROM analytics_queries WHERE organization_id = :org_id
                ORDER BY created_at DESC LIMIT 4
            """), {"org_id": str(org_id)})

            actividad_list = []
            for r in res_actividad.fetchall():
                actividad_list.append({
                    "id": r[0],
                    "usuario": r[1] or "Consultor RAG",
                    "query": f'"{r[2]}"' if r[2] else '"Búsqueda"',
                    "hace": "Reciente",
                    "resultados": r[4] or 0,
                    "score": float(r[5] or 0.0)
                })

            # 7. FILTRO: Usuarios únicos para el selector del frontend
            res_users_list = await conn.execute(text("""
                SELECT DISTINCT usuario_nombre FROM analytics_queries
                WHERE organization_id = :org_id AND usuario_nombre IS NOT NULL
            """), {"org_id": str(org_id)})
            usuarios_unificados = [{"id": i+1, "nombre": r[0]} for i, r in enumerate(res_users_list.fetchall())]

        return {
            "metricas": [
                {"label": "Total búsquedas", "icon": "bi-search", "valor": f"{total_queries:,}", "delta": "↑ Actividad", "deltaPositivo": True},
                {"label": "Tokens Consumidos", "icon": "bi-cpu", "valor": f"{total_tokens:,}", "delta": "Histórico API", "deltaPositivo": False},
                {"label": "Latencia media", "icon": "bi-clock", "valor": latencia_media, "delta": "Tiempo respuesta", "deltaPositivo": True},
                {"label": "Cache Hit Rate", "icon": "bi-lightning-charge", "valor": f"{hit_rate}%", "delta": "Queries optimizadas", "deltaPositivo": True}
            ],
            "volumenDiario": {"labels": labels_vol, "data": values_vol},
            "tipoQueryData": [
                {"label": "Habilidades técnicas", "pct": pct_tecnico, "color": "#1a6f3c"},
                {"label": "Por cargo", "pct": pct_cargo, "color": "#378ADD"},
                {"label": "Por experiencia", "pct": pct_exp, "color": "#BA7517"}
            ],
            "tokensUso": tokens_data,
            "queries": queries_list,
            "actividad": actividad_list,
            "usuarios": usuarios_unificados
        }
