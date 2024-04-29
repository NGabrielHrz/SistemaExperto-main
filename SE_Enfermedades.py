from io import BytesIO
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
# import mysql.connector
from tkinter import ttk
from PIL import Image, ImageTk

# MÉTODO PARA ABRIR LA VENTANA EXPERTO
ventana_experto = None
def abrir_ventana_experto():
    #MÉTODO PARA GUARDAR EN LA BASE DE HECHOS
    def guardar_en_base_de_hechos():

        global imagen_blob
        edad = combo_edad.get()
        factor_riesgo = combo_factores_riesgo.get()

        sintoma =""
        #--------- Esta sección hay que cambiarla, ya que no vamos a usar lo mismo ---------#
        if Grupo1_var.get():
            sintoma = "Grupo1"
        else:
            print("El Checkbutton Grupo 1 no está seleccionado.")
        if Grupo2_var.get():
            sintoma = "Grupo2"
        else:
            print("El Checkbutton Grupo 2 no está seleccionado.")
        if Grupo3_var.get():
            sintoma = "Grupo3"
        else:
            print("El Checkbutton Grupo 3 no está seleccionado.")
        if Grupo4_var.get():
            sintoma = "Grupo 4"
        else:
            print("Haz una seleccion")

        tiempo = combo_tiempo.get()
        respuesta = text_respuesta.get("0.0", tk.END)
        explicacion = text_explicacion.get("0.0", tk.END)

        conexion = mysql.connector.connect(user='root',password='root',
                                        host='localhost',
                                        database='se_database',
                                        port='3306')
        print(conexion)
        cursor = conexion.cursor()
        # Valores para la base de datos
        valores = (edad, factor_riesgo, sintoma, tiempo, respuesta, explicacion, imagen_blob)

        # Crea la consulta SQL para insertar un nuevo registro
        consulta = "INSERT INTO enf(edad, factor_riesgo, sintomas, tiempo, resp, explicacion, img) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        # Ejecuta la consulta con los valores
        valores = (edad, factor_riesgo, sintoma, tiempo, respuesta, explicacion, imagen_blob)
        cursor.execute(consulta, valores)

        # Confirma la inserción de datos en la base de datos
        conexion.commit()

        # Cierra el cursor y la conexión
        cursor.close()
        conexion.close()

    # ------------------------CARGAR IMAGEN--------------------- #
    def cargar_imagen():

        global imagen_blob
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.webp;*.png;*.jpg;*.jpeg;*.gif")])

        if ruta_imagen:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((200, 200))  # Ajusta el tamaño de la imagen según tus necesidades
            imagen_tk = ImageTk.PhotoImage(imagen)

            # Convertir la imagen a formato BLOB
            buffer = BytesIO()
            imagen.save(buffer, format="JPEG")  # El formato se obtiene automáticamente del original
            imagen_blob = buffer.getvalue()

            etiqueta_imagen.config(image=imagen_tk)
            etiqueta_imagen.image = imagen_tk  # ¡Importante! Evita que la imagen se elimine debido a la recolección de basura


    # ----------------------------INTERFAZ DE USUARIO EXPERTO-----------------------------#==================
    global ventana_experto
    ventana.withdraw()  # Oculta la ventana principal
    ventana_experto = tk.Toplevel(ventana)  # Crea una nueva ventana secundaria
    ventana_experto.title("Sistema Experto para escoger novio/a para tu hija/o")
    ancho_ventana = 625
    alto_ventana = 580

    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana_experto.winfo_screenwidth()
    alto_pantalla = ventana_experto.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x_pos = (ancho_pantalla - ancho_ventana) // 2
    y_pos = (alto_pantalla - alto_ventana) // 2

    # Configurar la geometría de la ventana
    ventana_experto.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    # Interfaz de Usuario
    fuente_Title = ('Times', 16)  # Tipo de letra Arial, tamaño 16

    # Titulo
    etiqueta_titulo = ttk.Label(ventana_experto, text="Sistema Experto escoger novio/a para tu hija/o:", font=fuente_Title)
    etiqueta_titulo.grid(row=0, column = 0, columnspan=2, pady=10)

    # Configurar las columnas para expandirse
    ventana_experto.columnconfigure(0, weight=1)
    ventana_experto.columnconfigure(1, weight=1)

    # Edad y combobox
    Genero = {
        "Masculino":"Ser humano que nacio Hombre y se identifica como tal",
        "Femenino": "Ser humano que nacio Mujer y se identifica como tal",
        "39 tipos de gay": "Ser humano que nacio Hombre/Mujer y se no esta conforme con nada"
    }
    etiqueta_edad = ttk.Label(ventana_experto, text="¿Qué genero eres?:")
    etiqueta_edad.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

    combo_edad = ttk.Combobox(ventana_experto, values=list(Genero.keys()), state="readonly")
    combo_edad.grid(row=1, column=0, padx=(147,0), pady=10, sticky ="w")

    # Etiqueta y Combo Box para Factores de Riesgo
    Edad = { # ESTE ES EL noSQL
        "15-18": "Adolescente tardío",
        "19-21": "Joven adulto",
        "21-25": "Adulto joven",
        "26-30": "Adulto"
    } # ESTE ES EL noSQL

    etiqueta_factores_riesgo = ttk.Label(ventana_experto, text="¿Que eddad tiene su hijo/a?:")
    etiqueta_factores_riesgo.grid(row=2, column=0, padx=(20,0), pady=10, sticky ="w")

    combo_factores_riesgo = ttk.Combobox(ventana_experto, values=list(Edad.keys()), state="readonly")
    combo_factores_riesgo.grid(row=2, column=0, padx=(207,0), pady=10, sticky ="w")

    # Etiqueta sintomas
    etiqueta_sintomas = ttk.Label(ventana_experto, text="¡Que orientacion sexual tiene tu hija/hijo?:")
    etiqueta_sintomas.grid(row=3, column=0, padx=(20,0), pady=5, sticky ="w")

    # Sintomas # Cambiar ya que no se usaran grupos, se usaran noSQL
    #Grupo 1
    Grupo1_var = tk.BooleanVar()
    cuadro_Grupo1 = ttk.Checkbutton(ventana_experto, text="Grupo 1. \n-Fiebre y tos\n-Dolor de garganta\n-Secreción nasal, \n-Congestión nasal.", variable=Grupo1_var)
    cuadro_Grupo1.grid(row=4, column=0, padx=(20,0), sticky="w")

    # Grupo 2
    Grupo2_var = tk.BooleanVar()
    cuadro_Grupo2 = ttk.Checkbutton(ventana_experto, text="Grupo 2. \n-Dificultad para respirar\n-Opresión en el pecho\n-Respiración rápida", variable=Grupo2_var)
    cuadro_Grupo2.grid(row=4, column=0, padx=(160,0), sticky="w")

    # Grupo 3
    Grupo3_var = tk.BooleanVar()
    cuadro_Grupo3 = ttk.Checkbutton(ventana_experto, text="Grupo 3.\n-Secreción de moco\n-Fiebre alta\n-Dolor de cabeza", variable=Grupo3_var)
    cuadro_Grupo3.grid(row=4, column=0, padx=(330,0), sticky="w")

    # Grupo 4
    Grupo4_var = tk.BooleanVar()
    cuadro_Grupo4 = ttk.Checkbutton(ventana_experto, text="Grupo 4.\n-Pérdida de apetito\n-Pérdida de peso\n-Fatiga", variable=Grupo4_var)
    cuadro_Grupo4.grid(row=4, column=0, padx=(470,0), sticky="w")

    # Etiqueta y combo box para tiempo de los sintomas
    tiempo = { # Cambier este noSQL por el que tenemos
        "1 día":"Poco tiempo",
        "1 semana": "Tiempo considerable",
        "1 mes": "Bastante tiempo"
    }
    etiqueta_tiempo = ttk.Label(ventana_experto, text="¿Que intereses tiene tu hija/o?:")
    etiqueta_tiempo.grid(row=5, column=0, padx=(20,0), pady=10, sticky ="w")

    combo_tiempo = ttk.Combobox(ventana_experto, values=list(tiempo.keys()), state="readonly")
    combo_tiempo.grid(row=5, column=0, padx=(224,0), pady=10, sticky ="w")

    # Boton Agregar Imagen
    boton_img = ttk.Button(ventana_experto, text="Subir imagen", command=cargar_imagen)
    boton_img.grid(row=6, column=0, padx=(370,0), pady= 5)

    # Crear la primera área de texto
    text_respuesta = scrolledtext.ScrolledText(ventana_experto, wrap=tk.WORD, width=42, height=5)
    text_respuesta.grid(row=7, column=0, padx=(20,0), pady=10, sticky ="w")

    # Crear la segunda área de texto debajo de la primera
    text_explicacion = scrolledtext.ScrolledText(ventana_experto, wrap=tk.WORD, width=42, height=5)
    text_explicacion.grid(row=8, column=0, padx=(20,0), pady=10, sticky ="w")

    # Definir el tamaño deseado
    nuevo_tamano = (200, 200)  # Cambia estos valores según tu preferenScia

    # Redimensionar la imagen
    imagen_redimensionada = imagen_pillow.resize(nuevo_tamano)

    # Convertir la imagen a formato Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

    # Crear un widget Label para mostrar la imagen
    etiqueta_imagen = tk.Label(ventana_experto, image=imagen_tk)
    etiqueta_imagen.grid(row=7, rowspan=2, column=0, padx=(380,0))

    # Botón para abrir modo usuario
    boton_modo_usuario = ttk.Button(ventana_experto, text="Regresar al modo usuario", command=abrir_ventana_usuario)
    boton_modo_usuario.grid(row=9, column=0, padx=(20,0), sticky ="w")

    # Botón para Guardar Factores de Riesgo
    boton_guardar_datos = ttk.Button(ventana_experto, text="Guardar datos", command=guardar_en_base_de_hechos)
    boton_guardar_datos.grid(row=9, column=0, padx=(20,0))
    # ----------------------------CIERRE DE INTERFAZ DE USUARIO EXPERTO-----------------------------#=====================

def abrir_ventana_usuario():
    ventana_experto.destroy() # Cierra la ventana experto
    ventana.deiconify()  # Muestra la ventana principal

   

# ----------------------------INTERFAZ DE USUARIO NORMAL-----------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ventana = tk.Tk()
ventana.title("Sistema Experto para la Detección de Enfermedades Comunes")
ancho_ventana = 625
alto_ventana = 580

# Obtener el ancho y alto de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x_pos = (ancho_pantalla - ancho_ventana) // 2
y_pos = (alto_pantalla - alto_ventana) // 2

# Configurar la geometría de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Interfaz de Usuario
fuente_Title = ('Times', 16)  # Tipo de letra Arial, tamaño 16

# Titulo
etiqueta_titulo = ttk.Label(ventana, text="Sistema Experto de Enfermedades Comunes:", font=fuente_Title)
etiqueta_titulo.grid(row=0, column = 0, columnspan=2, pady=10)

# Configurar las columnas para expandirse
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)

# Edad y combobox
Genero = {
    "Masculino":"Ser humano que nacio Hombre y se identifica como tal",
    "Femenino": "Ser humano que nacio Mujer y se identifica como tal",
    "39 tipos de gay": "Ser humano que nacio Hombre/Mujer y se no esta conforme con nada"
}
etiqueta_edad = ttk.Label(ventana, text="¿Qué genero eres?:")
etiqueta_edad.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

combo_edad = ttk.Combobox(ventana, values=list(Genero.keys()), state="readonly")
combo_edad.grid(row=1, column=0, padx=(147,0), pady=10, sticky ="w")

# Etiqueta y Combo Box para Factores de Riesgo
Edad = { # ESTE ES EL noSQL
    "15-18": "Adolescente tardío",
    "19-21": "Joven adulto",
    "21-25": "Adulto joven",
    "26-30": "Adulto"
} # ESTE ES EL noSQL

etiqueta_factores_riesgo = ttk.Label(ventana, text="¿Que eddad tiene su hijo/a?:")
etiqueta_factores_riesgo.grid(row=2, column=0, padx=(20,0), pady=10, sticky ="w")

combo_factores_riesgo = ttk.Combobox(ventana, values=list(Edad.keys()), state="readonly")
combo_factores_riesgo.grid(row=2, column=0, padx=(207,0), pady=10, sticky ="w")

# Etiqueta sintomas
etiqueta_sintomas = ttk.Label(ventana, text="¡Que orientacion sexual tiene tu hija/hijo?:")
etiqueta_sintomas.grid(row=3, column=0, padx=(20,0), pady=5, sticky ="w")

# Sintomas # Cambiar ya que no se usaran grupos, se usaran noSQL
#Grupo 1
Grupo1_var = tk.BooleanVar()
cuadro_Grupo1 = ttk.Checkbutton(ventana, text="Grupo 1. \n-Fiebre y tos\n-Dolor de garganta\n-Secreción nasal, \n-Congestión nasal.", variable=Grupo1_var)
cuadro_Grupo1.grid(row=4, column=0, padx=(20,0), sticky="w")

# Grupo 2
Grupo2_var = tk.BooleanVar()
cuadro_Grupo2 = ttk.Checkbutton(ventana, text="Grupo 2. \n-Dificultad para respirar\n-Opresión en el pecho\n-Respiración rápida", variable=Grupo2_var)
cuadro_Grupo2.grid(row=4, column=0, padx=(160,0), sticky="w")

# Grupo 3
Grupo3_var = tk.BooleanVar()
cuadro_Grupo3 = ttk.Checkbutton(ventana, text="Grupo 3.\n-Secreción de moco\n-Fiebre alta\n-Dolor de cabeza", variable=Grupo3_var)
cuadro_Grupo3.grid(row=4, column=0, padx=(330,0), sticky="w")

# Grupo 4
Grupo4_var = tk.BooleanVar()
cuadro_Grupo4 = ttk.Checkbutton(ventana, text="Grupo 4.\n-Pérdida de apetito\n-Pérdida de peso\n-Fatiga", variable=Grupo4_var)
cuadro_Grupo4.grid(row=4, column=0, padx=(470,0), sticky="w")

# Etiqueta y combo box para tiempo de los sintomas
tiempo = { # Cambier este noSQL por el que tenemos
    "1 día":"Poco tiempo",
    "1 semana": "Tiempo considerable",
    "1 mes": "Bastante tiempo"
}
etiqueta_tiempo = ttk.Label(ventana, text="¿Que intereses tiene tu hija/o?:")
etiqueta_tiempo.grid(row=5, column=0, padx=(20,0), pady=10, sticky ="w")

combo_tiempo = ttk.Combobox(ventana, values=list(tiempo.keys()), state="readonly")
combo_tiempo.grid(row=5, column=0, padx=(224,0), pady=10, sticky ="w")

# Crear la primera área de texto
text_respuesta = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=42, height=5, state=tk.DISABLED)
text_respuesta.grid(row=7, column=0, padx=(20,0), pady=10, sticky ="w")


# Crear la segunda área de texto debajo de la primera
text_explicacion = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=42, height=5, state=tk.DISABLED)
text_explicacion.grid(row=8, column=0, padx=(20,0), pady=10, sticky ="w")


# METODO PARA MOSTRAR LA EXPLICACION
def mostrar_explicacion():
    edad = combo_edad.get()
    factor_riesgo = combo_factores_riesgo.get()

    sintoma =""

    if Grupo1_var.get():
        sintoma = "Grupo1"
    else:
        print("El Checkbutton dolor cuadro_fiebre_tos_var no está seleccionado.")
    if Grupo2_var.get():
        sintoma = "Grupo2"
    else:
        print("El Checkbutton dolor cuadro_dolormuscular_var no está seleccionado.")
    if Grupo3_var.get():
        sintoma = "Grupo3"
    else:
        print("El Checkbutton dolor cuadro_nauseas_var no está seleccionado.")
    if Grupo4_var.get():
        sintoma = "Grupo4"
    else:
        print("Pon algo")

    tiempo = combo_tiempo.get()

    conexion2 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion2)
    cursor2 = conexion2.cursor()

    valores = (edad, factor_riesgo, sintoma, tiempo)

    # Crea la consulta SQL para rescatar una imagen
    consulta_existencia = "SELECT explicacion FROM enf WHERE edad = %s AND factor_riesgo = %s AND sintomas = %s AND tiempo = %s"

    # Ejecuta la consulta con los valores
    cursor2.execute(consulta_existencia, valores)

    # Verificar si hay algún resultado
    resultados = cursor2.fetchall()

    # Limpiar el contenido actual del text_respuesta
    text_explicacion.config(state=tk.NORMAL)
    text_explicacion.delete('1.0', tk.END)

    for resultado in resultados:
        explicacion, = resultado
        print(explicacion)

        # Establecer un valor inicial
        text_explicacion.insert(tk.END, f"Según los datos ingresados, puede tener: {explicacion}\nNota. Se recomienda que busque atención médica para un diagnóstico adecuado y un tratamiento oportuno.")
        break
    else:
        print("No hay nada")

    # Confirma la inserción de datos en la base de datos
    conexion2.commit()

    # Cierra el cursor y la conexión
    cursor2.close()
    conexion2.close()

    # Configurar el text_respuesta como de solo lectura
    text_explicacion.config(state=tk.DISABLED)



# LIMPIA LAS CASILLAS CUANDO SE QUIERE REALIZAR OTRA CONSULTA
def limpiar_casillas():
    combo_factores_riesgo.set("")
    combo_edad.set("")
    combo_tiempo.set("")
    Grupo1_var.set(False)
    Grupo2_var.set(False)
    Grupo3_var.set(False)
    Grupo4_var.set(False)
    text_explicacion.config(state=tk.NORMAL)
    text_explicacion.delete('1.0', tk.END)
    text_explicacion.insert(tk.END, "")
    text_explicacion.config(state=tk.DISABLED)
    text_respuesta.config(state=tk.NORMAL)
    text_respuesta.delete('1.0', tk.END)
    text_respuesta.insert(tk.END, "")
    text_respuesta.config(state=tk.DISABLED)



imagen_pillow = Image.open("Logo.webp")

# Definir el tamaño deseado
nuevo_tamano = (200, 200)  # Cambia estos valores según tu preferencia

# Redimensionar la imagen
imagen_redimensionada = imagen_pillow.resize(nuevo_tamano)

# Convertir la imagen a formato Tkinter
imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

# Crear un widget Label para mostrar la imagen
etiqueta_imagen = tk.Label(ventana, image=imagen_tk)
etiqueta_imagen.grid(row=7, rowspan=2, column=0, padx=(380,0))

# MÉTODO PARA MOSTRAR LA IMAGEN
def obtener_img():
    edad = combo_edad.get()
    factor_riesgo = combo_factores_riesgo.get()

    sintoma =""

    if Grupo1_var.get():
        sintoma = "Grupo1"
    else:
        print("El Checkbutton dolor cuadro_fiebre_tos_var no está seleccionado.")
    if Grupo2_var.get():
        sintoma = "Grupo2"
    else:
        print("El Checkbutton dolor cuadro_dolormuscular_var no está seleccionado.")
    if Grupo3_var.get():
        sintoma = "Grupo3"
    else:
        print("El Checkbutton dolor cuadro_nauseas_var no está seleccionado.")
    if Grupo4_var.get():
        sintoma = "Grupo4"
    else:
        print("test")

    tiempo = combo_tiempo.get()

    # CONEXION CON LA BD PARA VER SI COINCIDEN LOS DATOS CON ALGO YA GUARDADO
    conexion3 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion3)
    cursor3 = conexion3.cursor()

    valores = (edad, factor_riesgo, sintoma, tiempo)

    consulta_imagen = "SELECT img FROM enf WHERE edad = %s AND factor_riesgo = %s AND sintomas = %s AND tiempo = %s"

    # Ejecuta la consulta con los valores
    cursor3.execute(consulta_imagen, valores)

    # Verificar si hay algún resultado
    resultadoImg = cursor3.fetchone()

    if resultadoImg is not None:

        imagen_bytes2 = resultadoImg[0]

        # Abrir la imagen con Pillow
        imagen_pillow2 = Image.open(BytesIO(imagen_bytes2))

        # Redimensionar la imagen
        imagen_redimensionada2 = imagen_pillow2.resize(nuevo_tamano)

        # Convertir la imagen a formato Tkinter
        imagen_tk2 = ImageTk.PhotoImage(imagen_redimensionada2)

        # Actualizar la imagen en el widget Label
        etiqueta_imagen.config(image=imagen_tk2)

        # Mantener la referencia global a la imagen_tk para evitar que sea eliminada
        etiqueta_imagen.image = imagen_tk2
    else:

        imagen_pillow = Image.open("Logo.webp")

        # Redimensionar la imagen
        imagen_redimensionada2 = imagen_pillow.resize(nuevo_tamano)

        # Convertir la imagen a formato Tkinter
        imagen_tk2 = ImageTk.PhotoImage(imagen_redimensionada2)

        # Actualizar la imagen en el widget Label
        etiqueta_imagen.config(image=imagen_tk2)

        # Mantener la referencia global a la imagen_tk para evitar que sea eliminada
        etiqueta_imagen.image = imagen_tk2





    # Confirma la inserción de datos en la base de datos
    conexion3.commit()

    # Cierra el cursor y la conexión
    cursor3.close()
    conexion3.close()
    ventana.update()

def llamar_funciones():
    obtener_consulta()
    obtener_img()



# MÉTODO PARA MOSTRAR LA RESPUESTA
def obtener_consulta():
    edad = combo_edad.get()
    factor_riesgo = combo_factores_riesgo.get()

    sintoma =""

    if Grupo1_var.get():
        sintoma = "Grupo1"
    else:
        print("El Checkbutton dolor cuadro_fiebre_tos_var no está seleccionado.")
    if Grupo2_var.get():
        sintoma = "Grupo2"
    else:
        print("El Checkbutton dolor cuadro_dolormuscular_var no está seleccionado.")
    if Grupo3_var.get():
        sintoma = "Grupo3"
    else:
        print("El Checkbutton dolor cuadro_nauseas_var no está seleccionado.")
    if Grupo4_var.get():
        sintoma = "Grupo4"
    else:
        print("Pon algo")

    tiempo = combo_tiempo.get()

    # CONEXION CON LA BD PARA VER SI COINCIDEN LOS DATOS CON ALGO YA GUARDADO
    conexion2 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion2)
    cursor2 = conexion2.cursor()

    valores = (edad, factor_riesgo, sintoma, tiempo)

    consulta_existencia = "SELECT resp FROM enf WHERE edad = %s AND factor_riesgo = %s AND sintomas = %s AND tiempo = %s"

    # Ejecuta la consulta con los valores
    cursor2.execute(consulta_existencia, valores)

    # Verificar si hay algún resultado
    resultados = cursor2.fetchall()

    # Limpiar el contenido actual del text_respuesta
    text_respuesta.config(state=tk.NORMAL)
    text_respuesta.delete('1.0', tk.END)

    for resultado in resultados:
        enfermedad, = resultado
        print(enfermedad)

        # Establecer un valor inicial
        text_respuesta.insert(tk.END, f"Según los datos ingresados, puede tener: {enfermedad}\nNota. Se recomienda que busque atención médica para un diagnóstico adecuado y un tratamiento oportuno.")

        text_explicacion.config(state=tk.NORMAL)
        text_explicacion.delete('1.0', tk.END)
        text_explicacion.insert(tk.END, "")
        text_explicacion.config(state=tk.DISABLED)

        break
    else:
        text_respuesta.insert(tk.END, f"No se encontró ninguna enfermedad asociada a sus síntomas, si requiere añadir información por favor vaya a la interfaz de experto")
        text_explicacion.config(state=tk.NORMAL)
        text_explicacion.delete('1.0', tk.END)
        text_explicacion.insert(tk.END, "")
        text_explicacion.config(state=tk.DISABLED)

    # Confirma la inserción de datos en la base de datos
    conexion2.commit()

    # Cierra el cursor y la conexión
    cursor2.close()
    conexion2.close()

    # Configurar el text_respuesta como de solo lectura
    text_respuesta.config(state=tk.DISABLED)


# Boton Obtener consulta
boton_consultar = ttk.Button(ventana, text="Obtener consulta", command=llamar_funciones)
boton_consultar.grid(row=6, column=0, sticky ="w", pady= 5, padx=(200,0))

# Boton Ver Explicación
boton_consultar = ttk.Button(ventana, text="Ver explicación", command=mostrar_explicacion)
boton_consultar.grid(row=6, column=0, sticky ="e", pady= 5, padx=(0,160))

# Botón realizar otra consulta
boton_realizar_consulta = ttk.Button(ventana, text="Realizar otra consulta",command=limpiar_casillas)
boton_realizar_consulta.grid(row=9, column=0, padx=(20,0), sticky ="w")

# Botón para abrir ventana experto
boton_abrir_experto = ttk.Button(ventana, text="Entrar a Modo Experto", command=abrir_ventana_experto)
boton_abrir_experto.grid(row=9, column=0, padx=(20,0))

ventana.mainloop()


