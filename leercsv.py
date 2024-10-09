import tkinter as tk
from tkinter import filedialog
import pandas as pd

def leer_datos_archivo(ruta_archivo: str) -> pd.DataFrame:
    try:
        datos = pd.read_csv(ruta_archivo)
        return datos
    except FileNotFoundError:
        print(f"El archivo '{ruta_archivo}' no existe")
        return None
    except pd.errors.EmptyDataError:
        print(f"El archivo '{ruta_archivo}' está vacío")
        return None
    except pd.errors.ParserError:
        print(f"Error al parsear el archivo '{ruta_archivo}'")
        return None

def analizar_datos(datos: pd.DataFrame) -> None:
    texto_resultados.delete(1.0, tk.END)
    texto_resultados.insert(tk.END, "Datos leídos con éxito!\n")
    texto_resultados.insert(tk.END, "Estadísticas de los datos:\n")
    texto_resultados.insert(tk.END, str(datos.describe()) + "\n")
    texto_resultados.insert(tk.END, "\nInformación de los datos:\n")
    texto_resultados.insert(tk.END, str(datos.info()) + "\n")
    texto_resultados.insert(tk.END, "\nPrimeras filas de los datos:\n")
    texto_resultados.insert(tk.END, str(datos.head()) + "\n")

    preguntas = datos.columns.tolist()
    for pregunta in preguntas:
        texto_resultados.insert(tk.END, f"\nResultados de la pregunta '{pregunta}':\n")
        resultados = datos[pregunta].value_counts()
        texto_resultados.insert(tk.END, str(resultados) + "\n")

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("Archivos CSV", "*.csv")])
    if ruta_archivo:
        entrada_ruta_archivo.delete(0, tk.END)
        entrada_ruta_archivo.insert(0, ruta_archivo)

def procesar_datos():
    ruta_archivo = entrada_ruta_archivo.get()
    datos = leer_datos_archivo(ruta_archivo)
    if datos is not None:
        analizar_datos(datos)

ventana = tk.Tk()
ventana.title("Análisis de datos")
ventana.geometry("800x600")  # Establece el tamaño inicial de la ventana
ventana.resizable(True, True)  # Permite ajustar el tamaño de la ventana

etiqueta_ruta_archivo = tk.Label(ventana, text="Ruta del archivo CSV:")
etiqueta_ruta_archivo.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

entrada_ruta_archivo = tk.Entry(ventana, width=50)
entrada_ruta_archivo.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

boton_seleccionar_archivo = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar_archivo.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

boton_procesar_datos = tk.Button(ventana, text="Procesar datos", command=procesar_datos)
boton_procesar_datos.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

texto_resultados = tk.Text(ventana, width=80, height=20)
texto_resultados.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_columnconfigure(2, weight=1)
ventana.grid_rowconfigure(0, weight=0)
ventana.grid_rowconfigure(1, weight=0)
ventana.grid_rowconfigure(2, weight=1)

ventana.mainloop()