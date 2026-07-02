# 🚀 Plataforma de Análisis e Inventario Minero (Pipeline ELT)

Este proyecto es un pipeline de datos End-to-End diseñado para procesar, transformar y visualizar datos de inventario minero utilizando tecnologías modernas de Big Data.

## 🛠️ Arquitectura y Tecnologías
- **Ingesta:** `Polars` (Procesamiento ultra-rápido en memoria)
- **Almacenamiento:** `DuckDB` (Base de datos analítica OLAP)
- **Transformación (ELT):** `dbt` (Modelado dimensional, capa Staging y Marts)
- **Orquestación:** `Prefect` (Gestión del flujo y dependencias)
- **Visualización:** `Plotly / Dash` (Dashboard interactivo web)
- **Infraestructura:** `Docker` e `Integración WSL` (Reproducibilidad total)

## ⚙️ Instrucciones de Ejecución

Este proyecto está completamente dockerizado para garantizar su reproducibilidad (Criterio 1). Para ejecutar el pipeline completo, siga estos pasos:

1. Clone este repositorio.
2. Abra una terminal en la raíz del proyecto.
3. Ejecute el siguiente comando:
   ```bash
   docker compose up --build
