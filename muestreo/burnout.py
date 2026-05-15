import numpy as np
import pandas as pd

from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, Label, HoverTool

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
np.random.seed(42)  # Fija semilla para reproducibilidad predecile 

trabajadores = 4  # Define cantidad de empleados
semanas = 12  # Define semanas de estudio

output_file("burnout.html")  # Establece archivo de salida HTML

# -----------------------------
# DATOS
# -----------------------------
def generar_datos():  # Define función para crear dataset simulado
    data = []  # Inicializa lista vacía para almacenar registros

    for t in range(1, trabajadores + 1):  # Itera sobre cada trabajador
        for semana in range(1, semanas + 1):  # Itera sobre cada semana
            for dia in ["Martes", "Viernes"]:  # Itera sobre dos días por semana

                if t in [1, 2]:  # Condición para trabajadores 1 y 2
                    low, high = 1, 4  # Asigna rango bajo de valores
                else:  # Caso contrario (trabajadores 3 y 4)
                    low, high = 3, 6  # Asigna rango alto de valores

                data.append({  # Agrega un nuevo registro al dataset
                    "ID": t,  # Identificador del trabajador
                    "Semana": semana,  # Número de semana
                    "Dia": dia,  # Día de medición
                    "Label": f"{dia} S{semana}",  # Etiqueta para eje X

                    "Agotamiento": np.random.randint(low, high),  # Genera variable agotamiento 
                    "Cinismo": np.random.randint(low, high),  # Genera variable cinismo
                    "Motivación": np.random.randint(low, high),  # Genera variable falta de motivacion
                    "Concentración": np.random.randint(low, high),  # Genera variable falta de concentración
                    "Estrés": np.random.randint(low, high),  # Genera variable Estrés
                    "Carga": np.random.randint(low, high),  # Genera variable Carga Laboral
                    "IA (h)": np.random.randint(low, high)  # Genera variable IA
                })

    return pd.DataFrame(data)  # Convierte lista a DataFrame y lo retorna

df = generar_datos()  # Ejecuta función y almacena resultado

# -----------------------------
# GRÁFICA
# -----------------------------
def graficar_trabajador(data, trabajador_id):  # Define función para graficar un empleado

    d = data[data["ID"] == trabajador_id].copy()  # Filtra datos del trabajador específico
    x = d["Label"].tolist()  # Extrae etiquetas para eje X

    variables = [  # Lista de variables a graficar
        "Agotamiento",
        "Cinismo",
        "Motivación",
        "Concentración",
        "Estrés",
        "Carga"
    ]

    colores = ["red", "orange", "green", "blue", "purple", "black"]  # Asigna colores a variables

    # -----------------------------
    # FIGURA
    # -----------------------------
    p = figure(  # Crea nueva figura de Bokeh
        x_range=x,  # Define categorías del eje X
        y_range=(1, 5),  # Define rango del eje Y (escala Likert 1-5)
        width=1200,  # Ancho de la gráfica en píxeles
        height=500,  # Alto de la gráfica en píxeles
        title=f"Trabajador {trabajador_id} - Burnout"  # Título dinámico
    )

    # -----------------------------
    # VARIABLES
    # -----------------------------
    for var, color in zip(variables, colores):  # Itera sobre cada variable y su color

        y = d[var].values  # Extrae valores numéricos de la variable

        source = ColumnDataSource(data=dict(  # Crea fuente de datos para Bokeh
            x=x,  # Asigna etiquetas del eje X
            y=y,  # Asigna valores del eje Y
            var=[var]*len(x)  # Repite nombre de variable para cada punto
        ))

        p.line("x", "y", source=source, color=color, line_width=2, legend_label=var)  # Dibuja línea
        p.scatter("x", "y", source=source, color=color, size=6)  # Dibuja puntos

    # -----------------------------
    # DEBUG: VER DATOS
    # -----------------------------
    print(f"\n==============================")  # Imprime separador en consola
    print(f"TRABAJADOR {trabajador_id}")  # Imprime identificador
    print(f"==============================")  # Imprime separador

    valores = d[variables].values.flatten()  # Aplana matriz de valores a vector

    print("\nValores Y (todos):")  # Imprime encabezado
    print(valores.tolist())  # Imprime todos los valores generados

    for var in variables:  # Itera variables para depuración
        print(f"\n{var}:")  # Imprime nombre de variable
        print(d[var].tolist())  # Imprime lista de valores
    # -----------------------------
    # MEDIA
    # -----------------------------
    todos_valores = d[variables].values.flatten()  # Obtiene todos los valores numéricos
    media_trabajador = np.mean(todos_valores)  # Calcula media personal del trabajador

    p.line(x, [media_trabajador]*len(x),  # Dibuja línea horizontal en la media
           color="black",  # Color negro
           line_width=3,  # Grosor mayor
           line_dash="dashed",  # Línea segmentada
           legend_label="Media trabajador")  # Etiqueta de leyenda

    # -----------------------------
    # PROBABILIDAD
    # -----------------------------
    probabilidad = (media_trabajador - 1) / 4  # Normaliza media a escala 0-1 (1=mínimo, 5=máximo)

    p.line(x, [probabilidad*5]*len(x),  # Dibuja línea con probabilidad escalada
           color="red",  # Color rojo
           line_width=3,  # Grosor mayor
           line_dash="dotdash",  # Línea mixta puntos y rayas
           legend_label="Probabilidad renuncia")  # Etiqueta explicativa

    # -----------------------------
    # TOOLTIP (HOVER)
    # -----------------------------
    hover = HoverTool(tooltips=[  # Crea herramienta de información al pasar mouse
        ("Semana", "@x"),  # Muestra etiqueta de semana
        ("Valor", "@y"),  # Muestra valor numérico
        ("Variable", "@var")  # Muestra nombre de variable
    ])

    p.add_tools(hover)  # Agrega herramienta a la figura

    # -----------------------------
    # TEXTO
    # -----------------------------
    texto = f"""  # Construye texto informativo multilínea
Media: {media_trabajador:.2f}
Probabilidad renuncia: {probabilidad*100:.1f}%
"""

    label = Label(  # Crea etiqueta de texto en la gráfica
        x=0,  # Posición X en coordenadas de datos
        y=4.8,  # Posición Y cerca del tope
        x_units='data',  # Unidades base en datos
        y_units='data',  # Unidades base en datos
        text=texto,  # Texto a mostrar
        background_fill_color='white',  # Fondo blanco
        background_fill_alpha=0.8  # Opacidad 80%
    )

    p.add_layout(label)  # Agrega etiqueta al layout

    # -----------------------------
    # ESTILO
    # -----------------------------
    p.legend.click_policy = "hide"  # Permite ocultar líneas al hacer clic en leyenda
    p.xaxis.major_label_orientation = 1.2  # Rota etiquetas del eje X (radianes)
    p.legend.location = "top_left"  # Ubica leyenda en esquina superior izquierda

    show(p)  # Muestra la gráfica en el navegador

# -----------------------------
# EJECUCIÓN
# -----------------------------
for i in range(1, trabajadores + 1):  # Itera del trabajador 1 al 4
    graficar_trabajador(df, i)  # Genera gráfica para cada trabajador