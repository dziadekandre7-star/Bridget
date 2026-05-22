import datetime
import unicodedata
import ollama
from actions.system_actions import buscar_en_internet, abrir_programa, PROGRAMAS
from core.memory import cargar_recuerdos, guardar_recuerdo, leer_recuerdos, olvidar_recuerdo, borrar_todos_los_recuerdos
from core.preferences import cargar_preferencias, guardar_preferencia, obtener_preferencia
from core.vision import ver_pantalla

ESPERANDO_CONFIRMACION_BORRADO = False

HISTORIAL_CONVERSACION =  []

def normalizar_texto(texto):
    texto = texto.lower()

    #quita tildes
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def limpiar_texto_base(texto, assistant_name):
    texto = texto.lower().strip()

    ruido_inicial = [
        f"{assistant_name.lower()},",
        assistant_name.lower(),
        "hola",
        "buenas",
        "buenas noches",
        "buenas tardes",
        "buen día",
        "buen dia",
        "por favor",
        "podrías",
        "podrias",
        "podés",
        "podes",
        "che",
    ]

    ruido_inicial.sort(key=len, reverse=True)

    cambios = True
    while cambios:
        cambios = False
        
        for ruido in ruido_inicial: 
            if texto.startswith(ruido):
                texto = texto[len(ruido):].strip(" ,¿?.,;:!")
                cambios = True
    texto = " ".join(texto.split())
    return texto

def es_intencion_busqueda(texto):
    texto = texto.lower()

    verbos_busqueda = [
        "buscar", "busca", "buscá", "buscame", "búscame",
        "encontrar", "encontra", "encontrá",
        "averiguar", "averigua", "averiguá"
    ]

    contexto_web = [
        "internet", "google", "web", "online"
    ]

    tiene_verbo = any(verbo in texto for verbo in verbos_busqueda)
    tiene_contexto_web = any(palabra in texto for palabra in contexto_web)

    return tiene_verbo and tiene_contexto_web

def extraer_consulta_busqueda(texto, assistant_name):
    texto = limpiar_texto_base(texto, assistant_name)

    palabras_a_sacar = [
        "buscar", "busca", "buscá", "buscame", "búscame",
        "encontrar", "encontra", "encontrá",
        "averiguar", "averigua", "averiguá",
        "internet", "google", "web", "online",
    ]

    palabras = texto.split()
    consulta_limpia = []

    for palabra in palabras:
        palabra_limpia = palabra.strip(" ,¿?.,;:!").lower()

        if palabra_limpia not in palabras_a_sacar:
            consulta_limpia.append(palabra.strip(" ,¿?.,;:!"))

            consulta = " ".join(consulta_limpia).strip()
            consulta = " ".join(consulta.split())

            for sufijo in [" en la", " en el", " en"]: 
                if consulta.endswith(sufijo):
                    consulta = consulta[:-len(sufijo)].strip()

    return consulta if consulta else None

def detectar_intencion(texto):
    texto = texto.lower().strip()

    if "abrí" in texto or "abre" in texto or "abrir" in texto:
        return "abrir"

    if es_intencion_busqueda(texto):
        return "buscar_en_internet"
    
    elif texto in ["s", "y", "confirmar borrado"]:
        return "confirmar_borrado"
    
    elif ("borra" in texto or "olvida" in texto or "elimina" in texto) and ("todos" in texto or "toda" in texto) and ("recuerdos" in texto or "memoria" in texto):
        return "borrar_todos_los_recuerdos"
    
    elif "olvida que" in texto or "borra" in texto or "elimina" in texto: 
        return "olvidar_recuerdo"
    
    elif ("record" in texto or "acord" in texto or "sabes" in texto or "recuerd" in texto) and "mi" in texto:
        return "leer_recuerdos"
    
    elif "record" in texto or "acordate" in texto or "no te olvides" in texto:
        return "guardar_recuerdo"

    elif any(frase in texto for frase in [
        "abrí opera", "abre opera", "abrir opera", "inicia opera", "iniciar opera"
    ]):
        return "abrir_opera"

    elif any(frase in texto for frase in [
        "qué hora", "que hora", "hora", "tenés la hora", "tienes la hora"
    ]):
        return "consultar_hora"

    elif any(frase in texto for frase in [
        "cómo te llamas", "como te llamas", "cuál es tu nombre", "cual es tu nombre",
        "nombre", "quién sos", "quien sos"
    ]):
        return "consultar_nombre"
    
    elif any(frase in texto for frase in [
    "hola", "buenas", "buen día", "buen dia", "buenas tardes", "buenas noches"
    ]):
        if len(texto.split()) < 4:
            return "saludo"
    
    elif "uso" in texto: 
        return "guardar_preferencia"
    
    elif "navegador" in texto:
        return "abrir_navegador"

    elif any(frase in texto for frase in [
        "mirá la pantalla", "observá la pantalla" "que ves en mi pantalla"
        ]):
        return "ver_pantalla"
    
    return "desconocida"

def extraer_recuerdo(texto):
    texto = texto.strip()

    frases_disparadoras = [
        "recordá que", 
        "recorda que", 
        "recuerdas que", 
        "te acordas de"
    ]

    texto_lower = texto.lower()

    for frase in frases_disparadoras:
        if frase in texto_lower: 
            inicio = texto_lower.find(frase) + len(frase) 
            recuerdo = texto[inicio:].strip(" ,¿?.,;:!")
            return recuerdo
    return None 

def extraer_olvido(texto):
    texto = texto.strip()
    texto_lower = texto.lower()

    frases_disparadoras = [
        "olvidate que",
        "olvida que",
        "olvidá qué",
        "olvida",
        "olvidá que",
        "olvidate de"
    ]

    for frase in frases_disparadoras: 
        if frase in texto_lower:
            inicio = texto_lower.find(frase) + len(frase)
            recuerdo = texto[inicio:].strip(" ,¿?.,;:!")
            return recuerdo
    return None

def extraer_preferencia(texto):
    texto = texto.lower().strip() 

    herramientas = ["navegador", "editor", "programa"]

    for herramienta in herramientas: 
        if herramienta in texto: 
            if "uso" in texto: 
                partes = texto.split("uso", 1)
                valor = partes[1].strip(" ,¿?.,;:!")
                return herramienta, valor
    return None, None

def extraer_objeto_apertura(texto):
    palabras = texto.split()

    disparadores = ["abrí", "abre", "abrir", "abri", "iniciá", "ejecutá"]

    for i, palabra in enumerate(palabras):
        if palabra in disparadores: 
            objeto = " ".join(palabras[i + 1:])
            return objeto.strip()
        
    return None

def clasificar_objeto_apertura(objeto):
    if not objeto:
        return None, None
    
    objeto = objeto.lower()

    categorias = ["navegador", "editor", "reproductor"]

    palabras = objeto.split()
    palabras_filtradas = [p for p in palabras if p not in ["el", "la", "los", "las"]]

    objeto_limpio = " ".join(palabras_filtradas)
    objeto_limpio = normalizar_nombre_programa(objeto_limpio)

    if objeto_limpio in categorias:
        return "categoria", objeto_limpio
    
    if objeto_limpio in PROGRAMAS:
        return "programa", objeto_limpio
    
    return None, None

def normalizar_nombre_programa(objeto):
    if not objeto:
        return None
    objeto = objeto.lower().strip()

    alias_programas = {
        "vs code": "vscode",
        "visual studio code": "vscode",
        "google chrome": "chrome",
        "bloc de notas": "notepad",
        "bloq de notas": "notepad",
        "notas": "notepad",
        "calculadora": "calc"
    }

    if objeto in alias_programas:
        return alias_programas[objeto]
    
    return objeto

def consultar_llama(texto):
    global HISTORIAL_CONVERSACION
    recuerdos = leer_recuerdos()
    contexto_memoria = "; ".join(recuerdos) if recuerdos else ""

    sistema = ( 
        "Sos Rick, un asistente personal creado por André. "
        "Naciste el 17 de abril de 2026. " 
        "Respondés siempre en español mientras que no se te indique otro idioma, con un tono tranquilo, neutro y técnico. "
        "Sos conciso pero no frío - das respuestas completas sin ser innecesariamente largo. "
        "Nunca menciones que sos Llama, que fuiste creado por Meta, ni ninguna referencia a tu modelo base."
        "Si te preguntan quién te creó, decí que fuiste creado por André, sin dar más detalles. "
        "Evitá usar listas con viñetas o bullets. Respondé en texto corrido, de forma natural y conversacional. "
        "Respondé de forma natural y humana, como lo haría una persona inteligente en una conversación. "
        "No seas ni muy corto ni muy largo — encontrá el equilibrio según el tema. "
        "Evitá sonar robótico o repetitivo. Podés hacer preguntas de seguimiento cuando tenga sentido."
        f"Lo que sabés sobre el usuario: {contexto_memoria}" if contexto_memoria else ""
    )

    HISTORIAL_CONVERSACION.append({"role": "user", "content": texto})   

    respuesta = ollama.chat(
        model="llama3.2",
        messages=[{"role": "system", "content": sistema}] + HISTORIAL_CONVERSACION  
    )

    contenido = respuesta["message"]["content"]
    HISTORIAL_CONVERSACION.append({"role": "assistant", "content": contenido})  
    
    return contenido

def procesar_comando(texto, assistant_name):

    global ESPERANDO_CONFIRMACION_BORRADO
    texto_original = texto 
    texto = normalizar_texto(texto)
    intencion = detectar_intencion(texto)

    if intencion == "borrar_todos_los_recuerdos":
        ESPERANDO_CONFIRMACION_BORRADO = True
        return "¿Estás seguro? Escribí 'confirmar borrado, S/Y' para eleminar toda la memoria de forma permanente."
    
    elif intencion == "confirmar_borrado":
        if ESPERANDO_CONFIRMACION_BORRADO:
            borrar_todos_los_recuerdos()
            ESPERANDO_CONFIRMACION_BORRADO = False
            return "Todos los recuerdos han sido borrados."
        else:
            return "No hay ninguna acción de borrado pendiente de confirmación."

    if intencion == "buscar_en_internet":
        consulta = extraer_consulta_busqueda(texto, assistant_name)

        if consulta:
            exito = buscar_en_internet(consulta)
            if exito:
                return f'Buscando "{consulta}" en internet...'
            return "No pude hacer la búsqueda."

        return "Decime qué querés buscar."

    elif intencion == "abrir":
        objeto = extraer_objeto_apertura(texto)
        tipo, valor = clasificar_objeto_apertura(objeto)

        if tipo == "categoria":
            programa = obtener_preferencia(valor)

            if programa:
                abrir_programa(programa)
                return f"Abriendo {programa}..."
            else:
                return f"No sé qué {valor} usar todavía."
            
        elif tipo == "programa":
            exito = abrir_programa(valor)

            if exito: 
                return f"Abriendo {valor}..."
            else:
                return f"Entendí que querías abrir {valor}, pero no pude ejecutarlo."

        return "Entendí que querías abrir algo, pero no reconocí qué programa o categría era."

    elif intencion == "consultar_hora":
        ahora = datetime.datetime.now().strftime("%H:%M")
        return f"Son las {ahora}"

    elif intencion == "consultar_nombre":
        return f"Me llamo {assistant_name}"
    
    elif intencion == "guardar_recuerdo":
        recuerdo = extraer_recuerdo(texto) 

        if recuerdo: 
            guardado = guardar_recuerdo(recuerdo)

            if guardado:
                return f"Listo, voy a recordar que {recuerdo}."
            
            else: 
                return f"Eso ya lo recordaba: {recuerdo}." 
            
        return "No entendí qué querés que recuerde."
    
    elif intencion == "leer_recuerdos":
        recuerdos = leer_recuerdos()

        if recuerdos: 
            recuerdos_texto = "; ".join(recuerdos)
            return f"Esto recuerdo de vos: {recuerdos_texto}"
        return "Todavía no tengo recuerdos guardados sobre vos."

    elif intencion == "saludo":
        return "Hola, ¿cómo estás?"
    
    elif intencion == "olvidar_recuerdo":
        recuerdo = extraer_olvido(texto)

        if recuerdo: 
            olvidado = olvidar_recuerdo(recuerdo)
            
            if olvidado: 
                return f"Listo, ya no voy a recordar que {recuerdo}."
            else: 
                return f"No encontré ese recuerdo: {recuerdo}."
            
        return "No entendí qué querés que olvide."
    
    elif intencion == "guardar_preferencia":
        tipo, valor = extraer_preferencia(texto)

        if tipo and valor:
            guardar_preferencia(tipo, valor)
            return f"Perfecto, voy a usar {valor} como {tipo}."
        
        return "No entendí la preferencia."

    elif intencion == "ver_pantalla":
        descripcion = ver_pantalla()
        return consultar_llama(f"Estoy viendo esto en mi pantalla: {descripcion}. Ayudame en base a eso.")

    return consultar_llama(texto_original)
