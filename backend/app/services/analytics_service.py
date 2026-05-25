import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from database import engine

class AnalyticsService:
    @staticmethod
    def _tiempo_transcurrido(fecha_query):
        """Calcula el tiempo transcurrido desde una fecha en formato legible"""
        ahora = datetime.now(timezone.utc)
        if fecha_query.tzinfo is None:
            fecha_query = fecha_query.replace(tzinfo=timezone.utc)

        diferencia = ahora - fecha_query

        if diferencia.total_seconds() < 60:
            return "Hace segundos"
        elif diferencia.total_seconds() < 3600:
            minutos = int(diferencia.total_seconds() / 60)
            return f"Hace {minutos} min" if minutos > 1 else "Hace 1 min"
        elif diferencia.total_seconds() < 86400:
            horas = int(diferencia.total_seconds() / 3600)
            return f"Hace {horas}h"
        elif diferencia.days < 7:
            return f"Hace {diferencia.days}d"
        else:
            return "Hace más de una semana"

    @staticmethod
    async def obtener_dashboard_summary(org_id: str, periodo_dias: int, usuario_nombre_filtro: str = ""):
        fecha_limite = datetime.now(timezone.utc) - timedelta(days=periodo_dias)
        fecha_limite_anterior = fecha_limite - timedelta(days=periodo_dias)

        filtros_sql = "WHERE organization_id = :org_id AND created_at >= :fecha_limite"
        params = {"org_id": str(org_id), "fecha_limite": fecha_limite}

        filtros_sql_anterior = "WHERE organization_id = :org_id AND created_at >= :fecha_limite_anterior AND created_at < :fecha_limite"
        params_anterior = {"org_id": str(org_id), "fecha_limite_anterior": fecha_limite_anterior, "fecha_limite": fecha_limite}

        if usuario_nombre_filtro:
            filtros_sql += " AND usuario_nombre = :usuario_nombre"
            params["usuario_nombre"] = str(usuario_nombre_filtro)
            filtros_sql_anterior += " AND usuario_nombre = :usuario_nombre"
            params_anterior["usuario_nombre"] = str(usuario_nombre_filtro)

        async with engine.connect() as conn:
            # 1. TARJETAS (Métricas Superiores) - Período actual
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

            # 1b. Período anterior para deltas
            res_total_anterior = await conn.execute(text(f"SELECT count(*) FROM analytics_queries {filtros_sql_anterior}"), params_anterior)
            total_queries_anterior = res_total_anterior.scalar() or 0

            res_cache_anterior = await conn.execute(text(f"SELECT count(*) FROM analytics_queries {filtros_sql_anterior} AND cached = true"), params_anterior)
            cache_queries_anterior = res_cache_anterior.scalar() or 0
            hit_rate_anterior = int((cache_queries_anterior / total_queries_anterior) * 100) if total_queries_anterior > 0 else 0

            res_latencia_anterior = await conn.execute(text(f"SELECT avg(latencia) FROM analytics_queries {filtros_sql_anterior}"), params_anterior)
            latencia_media_anterior = res_latencia_anterior.scalar() or 0

            res_tokens_anterior = await conn.execute(text(f"""
                SELECT COALESCE(SUM(tokens_input), 0) + COALESCE(SUM(tokens_output), 0)
                FROM analytics_queries {filtros_sql_anterior}
            """), params_anterior)
            total_tokens_anterior = res_tokens_anterior.scalar() or 0

            # Calcular deltas
            delta_queries = total_queries - total_queries_anterior if total_queries_anterior > 0 else total_queries
            delta_queries_pct = int((delta_queries / total_queries_anterior * 100)) if total_queries_anterior > 0 else 0
            delta_queries_texto = f"↑ {abs(delta_queries_pct)}%" if delta_queries > 0 else f"↓ {abs(delta_queries_pct)}%"

            delta_tokens = total_tokens - total_tokens_anterior if total_tokens_anterior > 0 else total_tokens
            delta_tokens_pct = int((delta_tokens / total_tokens_anterior * 100)) if total_tokens_anterior > 0 else 0
            delta_tokens_texto = f"↑ {abs(delta_tokens_pct)}%" if delta_tokens > 0 else f"↓ {abs(delta_tokens_pct)}%"

            delta_latencia = latencia_media_anterior - float(latencia_media_raw or 0)
            delta_latencia_texto = f"↓ Mejora {abs(delta_latencia):.2f}s" if delta_latencia > 0 else f"↑ {abs(delta_latencia):.2f}s"

            delta_cache = hit_rate - hit_rate_anterior
            delta_cache_texto = f"↑ {abs(delta_cache)}%" if delta_cache > 0 else f"↓ {abs(delta_cache)}%"

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
                    "id": idx + 1, "query": row[0], "usuario": row[1] if row[1] else "Sin usuario",
                    "skills": skills_data, "count": row[3] or 0, "score": float(row[4] or 0.0),
                    "cached": bool(row[5]), "ultima": row[6] or "Reciente"
                })

            # 6. MURO: Actividad Reciente
            res_actividad = await conn.execute(text(f"""
                SELECT id, usuario_nombre, query, created_at, resultados_count, latencia
                FROM analytics_queries WHERE organization_id = :org_id
                ORDER BY created_at DESC LIMIT 4
            """), {"org_id": str(org_id)})

            actividad_list = []
            for r in res_actividad.fetchall():
                actividad_list.append({
                    "id": r[0],
                    "usuario": r[1] if r[1] else "Sin usuario",
                    "query": f'"{r[2]}"' if r[2] else '"Búsqueda"',
                    "hace": AnalyticsService._tiempo_transcurrido(r[3]),
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
                {"label": "Total búsquedas", "icon": "bi-search", "valor": f"{total_queries:,}", "delta": delta_queries_texto, "deltaPositivo": delta_queries > 0},
                {"label": "Tokens Consumidos", "icon": "bi-cpu", "valor": f"{total_tokens:,}", "delta": delta_tokens_texto, "deltaPositivo": delta_tokens > 0},
                {"label": "Latencia media", "icon": "bi-clock", "valor": latencia_media, "delta": delta_latencia_texto, "deltaPositivo": delta_latencia > 0},
                {"label": "Cache Hit Rate", "icon": "bi-lightning-charge", "valor": f"{hit_rate}%", "delta": delta_cache_texto, "deltaPositivo": delta_cache > 0}
            ],
            "volumenDiario": {"labels": labels_vol, "data": values_vol},
            "tipoQueryData": [
                {"label": "Habilidades técnicas", "pct": pct_tecnico, "color": "#378ADD"},
                {"label": "Por cargo", "pct": pct_cargo, "color": "#1a6f3c"},
                {"label": "Por experiencia", "pct": pct_exp, "color": "#BA7517"}
            ],
            "tokensUso": tokens_data,
            "queries": queries_list,
            "actividad": actividad_list,
            "usuarios": usuarios_unificados
        }
