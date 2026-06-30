import polars as pl
import duckdb

def ejecutar_ingesta():
    print("Iniciando fase de ingesta con Polars...")
    
    # RUTAS ABSOLUTAS: Evitan que se creen archivos fantasma en otras carpetas
    csv_path = "/home/gonsa/mi_proyecto_mining/data/inventory_mining_dataset.csv"
    db_path = "/home/gonsa/mi_proyecto_mining/data/mining_analytics.db"
    
    columnas_clave = [
        "MINERAL_FILE_NUMBER", "MINFILE_NAME1", "YEAR", 
        "INVENTORY_CATEGORY_CODE", "INVENTORY_CATEGORY_DESCRIPTION",
        "COMMODITY_CODE_1", "COMMODITY_DESCRIPTION1", 
        "quantity", "GRADE1", 
        "DECIMAL_LATITUDE", "DECIMAL_LONGITUDE", 
        "UTM_ZONE", "UTM_NORTHING", "UTM_EASTING", 
        "ORE_ZONE_DESCRIPTION"
    ]
    
    df = pl.read_csv(csv_path, columns=columnas_clave, ignore_errors=True)
    
    df_limpio = df.filter(
        pl.col("DECIMAL_LATITUDE").is_not_null() & 
        pl.col("DECIMAL_LONGITUDE").is_not_null()
    ).with_columns([
        pl.col("quantity").fill_null(0.0),
        pl.col("GRADE1").fill_null(0.0)
    ])
    
    if df_limpio.shape[0] > 8000:
        df_final = df_limpio.sample(n=8000, seed=42)
    else:
        df_final = df_limpio
        
    print(f"Dataset reducido final: {df_final.shape[0]} filas y {df_final.shape[1]} columnas.")
    
    # --- CONEXIÓN BLINDADA A DUCKDB ---
    print(f"Conectando a la base de datos en: {db_path}")
    con = duckdb.connect(db_path)
    
    # 1. Registrar el DataFrame temporalmente en la memoria del motor
    con.register("df_temporal", df_final)
    
    # 2. Crear la tabla física leyendo de la memoria
    con.execute("CREATE OR REPLACE TABLE raw_inventory AS SELECT * FROM df_temporal")
    
    # 3. Forzar la escritura en el disco duro
    con.commit()
    
    # 4. Verificación interna obligatoria
    tablas = con.execute("SHOW TABLES").fetchall()
    print(f"¡Éxito! Tablas físicas detectadas en disco: {tablas}")
    
    con.close()

if __name__ == "__main__":
    ejecutar_ingesta()
