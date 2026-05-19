# Proyecto Final de programación
# Equipo: Marco Antonio Reyes Cuevas, Rubén Sánchez Suárez y Atziry Flores Rentería
# Docente: Pierre Antoine Delice
# Fecha: 18-05-2026

# Historia: El precio del silencio

import tkinter as tk
from tkinter import messagebox
import os

# =====================================================================
# VARIABLES GLOBALES (Estudiante 1 y 3)
# =====================================================================
puntos = 0
decisiones_tomadas = []
escena_actual = "MENU" 

# Archivos de texto planos (Estilo Principiante)
ARCHIVO_HISTORIAL = "historial_finales.txt"
ARCHIVO_SAVEGAE = "progreso_guardado.txt" # Archivo clave para retomar la partida

# =====================================================================
# LÓGICA DE PERSISTENCIA, GUARDADO Y RETORNO (Estudiante 3)
# =====================================================================
def guardar_en_historial(texto_a_guardar):
    """Escribe en el archivo general de registro histórico (modo append)"""
    try:
        archivo = open(ARCHIVO_HISTORIAL, "a", encoding="utf-8")
        archivo.write(texto_a_guardar)
        archivo.close()
    except Exception as e:
        print("Error al escribir en el historial:", e)

def guardar_partida_actual():
    """Guarda la escena y puntos actuales sobreescribiendo el archivo de progreso"""
    if escena_actual in ["MENU", "FINAL"]:
        messagebox.showwarning("Guardar Partida", "No puedes guardar progreso en el menú o en un final.")
        return

    try:
        # Guardamos solo los datos vitales para poder retomar (Sobreescritura 'w')
        archivo = open(ARCHIVO_SAVEGAE, "w", encoding="utf-8")
        archivo.write(f"{escena_actual}\n")
        archivo.write(f"{puntos}\n")
        archivo.close()
        
        # También dejamos registro en el historial general de texto
        bloque_historial = f"💾 PROGRESO GUARDADO: En la escena '{escena_actual}' con {puntos} puntos.\n"
        guardar_en_historial(bloque_historial)
        
        messagebox.showinfo("Guardar Partida", "¡Progreso guardado con éxito! Puedes cerrar el juego y retomar después.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la partida: {e}")

def retomar_partida():
    """Lee el archivo de progreso y salta directamente a la escena guardada"""
    global puntos, escena_actual
    
    if not os.path.exists(ARCHIVO_SAVEGAE):
        messagebox.showinfo("Retomar Partida", "No tienes ninguna partida guardada de momento.")
        return
    
    try:
        archivo = open(ARCHIVO_SAVEGAE, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
        
        # Limpiamos los saltos de línea (\n)
        escena_guardada = lineas[0].strip()
        puntos_guardados = int(lineas[1].strip())
        
        # Cargamos los datos en nuestras variables globales
        puntos = puntos_guardados
        decisiones_tomadas = [f"Partida retomada desde {escena_guardada}"]
        
        # Activamos los botones que se deshabilitan en el menú
        btn_volver.config(state=tk.NORMAL)
        btn_guardar.config(state=tk.NORMAL)
        
        # Evaluamos a qué función de la historia debemos brincar (Estructura de novato simple)
        if escena_guardada == "INICIO":
            escena_inicio()
        elif escena_guardada == "CAMINO_A":
            camino_a()
        elif escena_guardada == "CAMINO_A_OPCION_A":
            camino_a_opcion_a()
        elif escena_guardada == "CAMINO_B":
            camino_b()
        elif escena_guardada == "HISTORIA_CENTRAL":
            historia_central()
        elif escena_guardada == "HISTORIA_FINAL":
            historia_final()
            
        messagebox.showinfo("Retomar Partida", f"¡Partida cargada! Retomas con {puntos} puntos.")
        
    except Exception as e:
        messagebox.showerror("Error", f"El archivo de guardado está dañado o vacío: {e}")

def registrar_final_partida(final_alcanzado):
    """Registra el desenlace definitivo y borra el archivo temporal de progreso"""
    bloque_final = f"""=========================================
🏆 PARTIDA TERMINADA
Final obtenido: {final_alcanzado}
Puntos totales: {puntos}
=========================================\n\n"""
    
    guardar_en_historial(bloque_final)
    
    # Si terminó el juego con éxito, borramos el progreso temporal para que no retome un juego ya acabado
    if os.path.exists(ARCHIVO_SAVEGAE):
        os.remove(ARCHIVO_SAVEGAE)

def ver_historial():
    """Muestra todo el archivo de historial en una ventana flotante"""
    if not os.path.exists(ARCHIVO_HISTORIAL):
        messagebox.showinfo("Historial", "Aún no hay ningún registro histórico.")
        return
    
    archivo = open(ARCHIVO_HISTORIAL, "r", encoding="utf-8")
    contenido = archivo.read()
    archivo.close()
    
    ventana_historial = tk.Toplevel(root)
    ventana_historial.title("Historial General")
    ventana_historial.geometry("450x400")
    
    txt_historial = tk.Text(ventana_historial, wrap=tk.WORD, font=("Arial", 9))
    txt_historial.insert(tk.END, contenido)
    txt_historial.config(state=tk.DISABLED)
    txt_historial.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# =====================================================================
# PROCESAMIENTO DE DECISIONES
# =====================================================================
def procesar_decision(puntos_escena, texto_decision, funcion_siguiente):
    global puntos
    puntos += puntos_escena
    decisiones_tomadas.append(texto_decision)
    funcion_siguiente()

# =====================================================================
# FLUJO DE LA HISTORIA ORIGINAL (Estudiante 1 y 2)
# =====================================================================
def mostrar_menu():
    global puntos, decisiones_tomadas, escena_actual
    puntos = 0
    decisiones_tomadas = []
    escena_actual = "MENU"
    
    lbl_texto.config(text="""🎭 EL PESO DEL SILENCIO 🎭
    
Una novela interactiva sobre amistad y dolor.
Eres Noah, y tu mejor amiga Zaí la está pasando muy mal. 

¿Qué deseas hacer?""")
    
    btn_opcion_a.config(text="▶ Iniciar Nueva Historia", command=escena_inicio, state=tk.NORMAL)
    btn_opcion_b.config(text="🔄 Retomar Partida Guardada", command=retomar_partida, state=tk.NORMAL)
    btn_volver.config(state=tk.DISABLED)
    btn_guardar.config(state=tk.DISABLED) 

def escena_inicio():
    global escena_actual
    escena_actual = "INICIO"
    
    lbl_texto.config(text="""🎬 ESCENA: INICIO

Eres Noah. Has sido amigo de Zaí desde la primaria. Pero este semestre su madre falleció y ella se ha cerrado por completo. Te responde con monosílabos y cancela todos los planes. Sientes que la estás perdiendo.

Un día en el pasillo de la escuela, tras otra respuesta fría de su parte, la tensión estalla...

¿QUÉ HACES?""")
    
    btn_opcion_a.config(text="A) Mantener la calma, tragarme mi orgullo y ofrecerle un abrazo en silencio.", 
                        command=lambda: procesar_decision(10, "Abrazo silencioso", camino_a))
    btn_opcion_b.config(text="B) Confrontarla, reclamarle por su actitud y decirle que estoy harto.", 
                        command=lambda: procesar_decision(-10, "Confrontación", camino_b))
    btn_volver.config(state=tk.NORMAL)
    btn_guardar.config(state=tk.NORMAL) 

def camino_a():
    global escena_actual
    escena_actual = "CAMINO_A"
    
    lbl_texto.config(text="""🌿 ESCENA: CAMINO A (Empatía)

Le ofreces un abrazo, pero Zaí te empuja levemente diciendo que no quiere compasión y se va. Para desahogarte, pasas más tiempo hablando con Zoe, una amiga en común. Zaí se entera y se deprime más, sintiéndose reemplazada.

Un sábado, estás en el súper con Zoe y te cruzas a Zaí demacrada. Al verte, llora y corre a su casa. La sigues hasta su puerta.

¿QUÉ HACES?""")
    
    btn_opcion_a.config(text="A) Hablar con suavidad, pedirle perdón por haber ido con Zoe y explicarle tu miedo a perderla.", 
                        command=lambda: procesar_decision(20, "Disculpa por Zoe", camino_a_opcion_a))
    btn_opcion_b.config(text="B) Reclamarle por su actitud evasiva y decirle que Zoe sí te escucha.", 
                        command=lambda: procesar_decision(10, "Acusación por actitud", historia_central))

def camino_a_opcion_a():
    global escena_actual
    escena_actual = "CAMINO_A_OPCION_A"
    
    lbl_texto.config(text="""🏠 ESCENA: CAMINO A - OPCIÓN A (En la puerta de su casa)

Zaí se queda en silencio detrás de la puerta. Se nota que tus palabras la conmovieron, pero sigue teniendo miedo de abrirse contigo y lastimarte con su dolor. El silencio se vuelve prolongado...

¿QUÉ HACES?""")
    
    btn_opcion_a.config(text="A) Insistir en entrar a su casa para no dejarla sola en ese estado.", 
                        command=lambda: procesar_decision(20, "Insistir en entrar", historia_central))
    btn_opcion_b.config(text="B) Respetar su espacio, decirle que estarás ahí cuando esté lista y marcharte.", 
                        command=lambda: procesar_decision(0, "Respetar espacio", historia_central))

def camino_b():
    global escena_actual
    escena_actual = "CAMINO_B"
    
    lbl_texto.config(text="""🔥 ESCENA: CAMINO B (Confrontación)

Le gritas que estás harto. Ella te grita que la dejes en paz. La relación se rompe. Al sentirte culpable, buscas refugio en Zoe y se vuelven muy unidos. Zaí los ve juntos en la escuela y cae en una profunda depresión.

Un sábado en el súper, te topas a Zaí demacrada. Sale corriendo y la persigues hasta su casa. En la puerta la tensión es máxima...

¿QUÉ HACES?""")
    
    btn_opcion_a.config(text="A) Exigirle una explicación a gritos por haber huido.", 
                        command=lambda: procesar_decision(-20, "Exigir explicación", historia_central))
    btn_opcion_b.config(text="B) Bajar la voz, contener las lágrimas y decirle: 'Zaí, por favor, mírame...'", 
                        command=lambda: procesar_decision(10, "Calma y dolor", historia_central))

def historia_central():
    global escena_actual
    escena_actual = "HISTORIA_CENTRAL"
    
    lbl_texto.config(text="""⚫ ESCENA: HISTORIA CENTRAL (Cinco años después)

La discusión o plática en su puerta aclara las cosas a medias, pero ella te dice que la amistad se rompió y entra a su casa. Se gradúan de la preparatoria sin volverse a hablar. El tiempo pasa...

⏳ CINCO AÑOS DESPUÉS...
Estás en una cafetería de la estación de tren y ahí está Zaí, sentada junto a la ventana. Se ve más madura. Ella levanta la mirada y sus ojos se cruzan con los yours de golpe.

¿QUÉ HACES?""")
    
    btn_opcion_a.config(text="A) Caminar hacia su mesa con una sonrisa nostálgica y preguntarle si puedes sentarte.", 
                        command=lambda: procesar_decision(10, "Acercarse amable", historia_final))
    btn_opcion_b.config(text="B) Darte la vuelta disimuladamente y salir de la cafetería.", 
                        command=lambda: procesar_decision(-10, "Evitar contacto", historia_final))

def historia_final():
    global escena_actual
    escena_actual = "HISTORIA_FINAL"
    
    lbl_texto.config(text="""💬 ESCENA: HISTORIA FINAL (La conversación definitiva)

Están frente a frente en la cafetería (o te quedaste pensando afuera si huiste). El ambiente está lleno de recuerdos de la adolescencia y cuentas pendientes. Es el momento de decidir cómo vas a actuar en esta interacción crucial.

¿CÓMO TE COMPORTAS?""")
    
    btn_opcion_a.config(text="A) Hablar con total madurez, admitir tus errores y pedirle una disculpa sincera.", 
                        command=lambda: procesar_decision(10, "Madurez/Disculpa", calcular_final))
    btn_opcion_b.config(text="B) Hablar de forma superficial, evitando el pasado como si nada hubiera pasado.", 
                        command=lambda: procesar_decision(-10, "Hablar superficial", calcular_final))

# =====================================================================
# EVALUACIÓN DE FINALES
# =====================================================================
def calcular_final():
    global puntos, escena_actual
    escena_actual = "FINAL"
    
    if puntos == 80:
        nombre_final = "FINAL SECRETO: AMISTAD RECONCILIADA PERFECTAMENTE"
        texto_final = f"⭐ {nombre_final} ⭐\n\n¡Tu empatía fue impecable! Zaí te perdona de inmediato. Se levantan listos para recuperar los años perdidos.\n\nPuntos: {puntos}."
    elif puntos > 30:
        nombre_final = "FINAL 3: RECONCILIACIÓN ESPERANZADORA"
        texto_final = f"✨ {nombre_final} ✨\n\nLas disculpas fueron sinceras. Intercambian números para reconstruir su amistad desde cero.\n\nPuntos: {puntos}."
    elif puntos >= 0:
        nombre_final = "FINAL 2: DESPEDIDA MADURA"
        texto_final = f"🚶 {nombre_final} 🚶\n\nSe piden perdón por el pasado, pero sus vidas ya van por rumbos diferentes. Se despiden en paz.\n\nPuntos: {puntos}."
    else:
        nombre_final = "FINAL 1: TRAGEDIA"
        texto_final = f"💀 {nombre_final} 💀\n\nLa conversación sale mal. Zaí cruza la calle llorando y un auto no alcanza a frenar. El remordimiento te acompañará siempre.\n\nPuntos: {puntos}."

    lbl_texto.config(text=texto_final)
    
    btn_opcion_a.config(text="🔄 Volver al Menú Principal", command=mostrar_menu)
    btn_opcion_b.config(text="📋 Ver Historial de Juegos", command=ver_historial)
    btn_volver.config(state=tk.DISABLED)
    btn_guardar.config(state=tk.DISABLED) 
    
    registrar_final_partida(nombre_final)

# =====================================================================
# INTERFAZ GRÁFICA
# =====================================================================
root = tk.Tk()
root.title("Proyecto Final - Novela Interactiva")
root.geometry("680x520")

lbl_texto = tk.Label(root, text="", font=("Arial", 11), justify="left", wraplength=600, pady=20)
lbl_texto.pack(padx=20)

btn_opcion_a = tk.Button(root, text="", width=65, height=2, font=("Arial", 10))
btn_opcion_a.pack(pady=5)

btn_opcion_b = tk.Button(root, text="", width=65, height=2, font=("Arial", 10))
btn_opcion_b.pack(pady=5)

frame_controles = tk.Frame(root)
frame_controles.pack(pady=20)

btn_volver = tk.Button(frame_controles, text="⬅ Menu Principal", command=mostrar_menu, bg="#ffcccb", width=18)
btn_volver.pack(side=tk.LEFT, padx=10)

btn_guardar = tk.Button(frame_controles, text="💾 Guardar Progreso", command=guardar_partida_actual, bg="#bdfcc9", width=18)
btn_guardar.pack(side=tk.LEFT, padx=10)

mostrar_menu()
root.mainloop()
