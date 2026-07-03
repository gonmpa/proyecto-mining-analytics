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

Este proyecto está completamente dockerizado para garantizar su reproducibilidad. Para ejecutar el pipeline completo, siga estos pasos:

1. Clone este repositorio.
2. Abra una terminal en la raíz del proyecto.
3. Ejecute el siguiente comando:
   ```bash
   docker compose up --build



## 🧊 Modelo Multidimensional (Data Cube)

Como parte de los requisitos del proyecto, se identifica y documenta el modelo multidimensional presente en la solución mediante un esquema estrella (Star Schema):

**Tabla de hechos (Fact Table):**
* `fct_inventory`: Tabla central del esquema estrella. Almacena las medidas numéricas y contiene las claves foráneas (`mineral_id`, `commodity_code`) para conectar con los ejes de análisis.

**Medidas (Measures / Facts):**
* `tonnage`: Volumen total de toneladas registradas del mineral (métrica principal de agregación).
* `grade`: Nivel de ley, pureza o concentración del mineral extraído.

**Dimensiones (Dimensions):**
* `dim_mines`: Eje geográfico y operativo. Permite filtrar y agrupar por nombre de la faena minera, coordenadas (`latitude`, `longitude`) y zonas UTM.
* `dim_commodities`: Eje categórico de los materiales. Permite segmentar el análisis por tipo de mineral (`commodity_desc`) y su respectiva familia o categoría comercial (`category_desc`).
