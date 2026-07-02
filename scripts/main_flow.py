from prefect import flow, task
import subprocess
import os
import sys

# Importamos la función de ingesta que ya creaste
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.ingest import ejecutar_ingesta

@task(name="1. Ingesta de Datos con Polars", retries=1)
def tarea_ingesta():
    print("--- INICIANDO TAREA DE INGESTA ---")
    ejecutar_ingesta()
    print("--- TAREA DE INGESTA COMPLETADA ---")

@task(name="2. Transformacion ELT con dbt")
def tarea_transformacion():
    print("--- INICIANDO TAREA DE TRANSFORMACION (DBT) ---")
    
    # Definimos la ruta exacta de la carpeta dbt
    dbt_dir = "/home/gonsa/mi_proyecto_mining/dbt_mining"
    
    # Ejecutamos el comando de dbt desde Python
    resultado = subprocess.run(
        ["dbt", "run", "--profiles-dir", "."],
        cwd=dbt_dir,
        capture_output=True,
        text=True
    )
    
    # Imprimimos lo que dbt arroja en consola
    print(resultado.stdout)
    
    # Si dbt falla, hacemos que Prefect registre el error
    if resultado.returncode != 0:
        print(resultado.stderr)
        raise Exception("Falló la ejecución de dbt. Revisa los logs arriba.")
        
    print("--- TAREA DE TRANSFORMACION COMPLETADA ---")

@flow(name="Pipeline Minero Maestro", description="Flujo completo: Ingesta -> dbt")
def flujo_principal():
    # Ejecutamos el paso 1
    tarea_ingesta()
    
    # Ejecutamos el paso 2
    tarea_transformacion()

if __name__ == "__main__":
    flujo_principal()
