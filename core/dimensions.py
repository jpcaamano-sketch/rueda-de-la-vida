"""
Definición de las 8 dimensiones y 24 comportamientos de la Rueda de la Vida.
El campo 'orden' determina el orden de aparición en el formulario (fila.columna).
"""

DIMENSIONES = [
    {
        "id": 1,
        "nombre": "Trabajo y carrera",
        "color": "#1a3a5c",
        "icono": "💼",
        "comportamientos": [
            {
                "id": "1.1",
                "nombre": "Motivación cotidiana",
                "descripcion": "La mayoría de los días me levanto con algún nivel de motivación o interés genuino por lo que haré en el trabajo. No siento que estoy 'aguantando' sino que hay algo que me impulsa hacia adelante.",
                "orden": "1.1",
            },
            {
                "id": "1.2",
                "nombre": "Crecimiento y aprendizaje profesional",
                "descripcion": "En los últimos 6 meses he aprendido algo nuevo, asumido un desafío mayor o dado un paso concreto en mi desarrollo profesional. Siento que no estoy estancado/a.",
                "orden": "2.1",
            },
            {
                "id": "1.3",
                "nombre": "Alineación entre trabajo y valores",
                "descripcion": "Lo que hago en mi trabajo es coherente con lo que valoro y con quién quiero ser. No siento una contradicción permanente entre mi vida laboral y mis principios personales.",
                "orden": "3.1",
            },
        ],
    },
    {
        "id": 2,
        "nombre": "Salud y energía",
        "color": "#27ae60",
        "icono": "💪",
        "comportamientos": [
            {
                "id": "2.1",
                "nombre": "Calidad del sueño y descanso",
                "descripcion": "Duermo entre 7 y 8 horas la mayoría de las noches y me despierto sintiendo que he descansado. No dependo del café u otros estimulantes para funcionar durante el día.",
                "orden": "4.1",
            },
            {
                "id": "2.2",
                "nombre": "Actividad física regular",
                "descripcion": "Realizo algún tipo de movimiento o ejercicio físico al menos 3 veces por semana de manera consistente. Mi cuerpo recibe atención regular, no solo cuando algo duele.",
                "orden": "5.1",
            },
            {
                "id": "2.3",
                "nombre": "Energía disponible al final del día",
                "descripcion": "Al terminar la jornada tengo energía suficiente para hacer algo que disfruto o para estar presente con las personas que quiero. No llego agotado/a de manera crónica y sistemática.",
                "orden": "6.1",
            },
        ],
    },
    {
        "id": 3,
        "nombre": "Dinero y finanzas",
        "color": "#d4a017",
        "icono": "💰",
        "comportamientos": [
            {
                "id": "3.1",
                "nombre": "Control y claridad financiera",
                "descripcion": "Sé con claridad cuánto gano, cuánto gasto y en qué lo gasto. Tengo un registro o al menos una noción real de mis finanzas, no una sensación vaga de lo que entra y sale.",
                "orden": "7.1",
            },
            {
                "id": "3.2",
                "nombre": "Capacidad de ahorro o inversión",
                "descripcion": "Logro guardar o invertir alguna parte de mis ingresos de manera regular, aunque sea pequeña. No gasto todo lo que gano antes de que termine el mes.",
                "orden": "8.1",
            },
            {
                "id": "3.3",
                "nombre": "Tranquilidad financiera",
                "descripcion": "Mi situación económica actual no me genera una angustia constante ni ocupa una parte importante de mis pensamientos cotidianos. Tengo al menos un colchón básico de seguridad o un plan concreto para construirlo.",
                "orden": "1.2",
            },
        ],
    },
    {
        "id": 4,
        "nombre": "Familia y pareja",
        "color": "#e74c3c",
        "icono": "❤️",
        "comportamientos": [
            {
                "id": "4.1",
                "nombre": "Calidad del tiempo compartido",
                "descripcion": "Comparto tiempo de calidad real con mis personas más cercanas de manera regular. No es solo convivencia física: hay presencia, conversación y conexión genuina.",
                "orden": "2.2",
            },
            {
                "id": "4.2",
                "nombre": "Comunicación honesta y segura",
                "descripcion": "En mis vínculos familiares o de pareja más importantes puedo expresar lo que pienso y siento sin miedo a represalias o conflictos desproporcionados. Hay un espacio real para la honestidad.",
                "orden": "3.2",
            },
            {
                "id": "4.3",
                "nombre": "Reparación de conflictos",
                "descripcion": "Cuando hay conflictos o distancias en mis relaciones cercanas, existe la capacidad de hablarlos y resolverlos. Los problemas no quedan acumulados indefinidamente ni se barren bajo la alfombra.",
                "orden": "4.2",
            },
        ],
    },
    {
        "id": 5,
        "nombre": "Amistades y vida social",
        "color": "#9b59b6",
        "icono": "🤝",
        "comportamientos": [
            {
                "id": "5.1",
                "nombre": "Red de amistades activa",
                "descripcion": "Tengo al menos 2 o 3 amistades con quienes me relaciono de manera regular y con quienes puedo contar para compartir momentos, no solo para resolver problemas.",
                "orden": "5.2",
            },
            {
                "id": "5.2",
                "nombre": "Reciprocidad y nutrición mutua",
                "descripcion": "Mis amistades y relaciones sociales me dejan con más energía de la que tenía antes de verlos. No siento que la mayoría de mis vínculos son drenantes o basados solo en la obligación.",
                "orden": "6.2",
            },
            {
                "id": "5.3",
                "nombre": "Facilidad para conectar",
                "descripcion": "Me resulta relativamente natural iniciar o mantener relaciones sociales. No evito sistemáticamente el contacto con personas ni siento que el mundo social me genera más ansiedad que placer.",
                "orden": "7.2",
            },
        ],
    },
    {
        "id": 6,
        "nombre": "Desarrollo personal",
        "color": "#2980b9",
        "icono": "🌱",
        "comportamientos": [
            {
                "id": "6.1",
                "nombre": "Aprendizaje continuo activo",
                "descripcion": "En los últimos 3 meses he leído un libro, tomado un curso o tenido conversaciones que me han hecho pensar diferente. El aprendizaje es una práctica activa, no algo que 'algún día' voy a retomar.",
                "orden": "8.2",
            },
            {
                "id": "6.2",
                "nombre": "Trabajo sobre sí mismo/a",
                "descripcion": "Tengo alguna práctica regular de introspección o autoconocimiento: puede ser terapia, coaching, meditación, journaling o el hábito de hacerme preguntas honestas sobre quién soy y cómo estoy viviendo.",
                "orden": "1.3",
            },
            {
                "id": "6.3",
                "nombre": "Distancia entre quién soy y quién quiero ser",
                "descripcion": "Siento que la persona que soy hoy se parece razonablemente a la persona que quiero ser. La brecha entre mi yo actual y mi yo deseado no me genera frustración crónica ni sensación de traicionar mis valores.",
                "orden": "2.3",
            },
        ],
    },
    {
        "id": 7,
        "nombre": "Ocio y disfrute",
        "color": "#1abc9c",
        "icono": "🎨",
        "comportamientos": [
            {
                "id": "7.1",
                "nombre": "Tiempo de descanso sin culpa",
                "descripcion": "Tengo momentos regulares de descanso, ocio o entretenimiento en mi semana y puedo disfrutarlos sin sentir que debería estar haciendo algo productivo. El descanso no me genera culpa ni ansiedad.",
                "orden": "3.3",
            },
            {
                "id": "7.2",
                "nombre": "Actividades que disfruto genuinamente",
                "descripcion": "Tengo al menos una actividad en mi vida —un hobby, un deporte, una práctica creativa— que hago simplemente porque me gusta, no porque sea útil o productiva.",
                "orden": "4.3",
            },
            {
                "id": "7.3",
                "nombre": "Presencia en el momento de disfrute",
                "descripcion": "Cuando estoy en momentos de ocio o disfrute, logro estar presente y disfrutarlos realmente. No estoy pensando en el trabajo o revisando el celular de manera compulsiva mientras intento descansar.",
                "orden": "5.3",
            },
        ],
    },
    {
        "id": 8,
        "nombre": "Propósito y sentido",
        "color": "#e67e22",
        "icono": "🧭",
        "comportamientos": [
            {
                "id": "8.1",
                "nombre": "Claridad sobre lo que importa",
                "descripcion": "Tengo claridad razonable sobre qué es lo que más valoro en la vida y hacia dónde quiero ir. No siento que estoy viviendo en piloto automático ni que simplemente estoy cumpliendo con lo que se espera de mí.",
                "orden": "6.3",
            },
            {
                "id": "8.2",
                "nombre": "Coherencia entre decisiones y propósito",
                "descripcion": "Las decisiones importantes que tomo en mi vida son coherentes con lo que declaro que más importa. No hay una contradicción permanente entre lo que digo valorar y cómo realmente vivo.",
                "orden": "7.3",
            },
            {
                "id": "8.3",
                "nombre": "Sensación de contribución",
                "descripcion": "Siento que lo que hago tiene algún impacto positivo en otros o en algo más grande que yo mismo/a. No necesariamente de manera grandiosa, pero sí una sensación básica de que mi presencia en el mundo hace alguna diferencia.",
                "orden": "8.3",
            },
        ],
    },
]


def _enriquecer(dim, comp):
    return {
        "dim_id":     dim["id"],
        "dim_nombre": dim["nombre"],
        "dim_color":  dim["color"],
        "dim_icono":  dim["icono"],
        **comp,
    }


def get_comportamientos_formulario():
    """
    Orden para el formulario: agrupado por dimensión (1.1, 1.2, 1.3, 2.1, 2.2, ...).
    """
    items = []
    for dim in DIMENSIONES:
        for comp in dim["comportamientos"]:
            items.append(_enriquecer(dim, comp))
    # Ordenar por (dim_id, posición dentro de la dimensión)
    def sort_key(x):
        dim_id, pos = x["id"].split(".")
        return (int(dim_id), int(pos))
    return sorted(items, key=sort_key)


def get_comportamientos_informe():
    """
    Orden para el informe: intercalado por posición dentro de cada dimensión
    (1.1, 2.1, 3.1…8.1,  1.2, 2.2…8.2,  1.3, 2.3…8.3).
    """
    items = []
    for dim in DIMENSIONES:
        for comp in dim["comportamientos"]:
            items.append(_enriquecer(dim, comp))
    def sort_key(x):
        dim_id, pos = x["id"].split(".")
        return (int(pos), int(dim_id))
    return sorted(items, key=sort_key)


# Alias de compatibilidad
def get_comportamientos_ordenados():
    return get_comportamientos_formulario()


def calcular_puntajes(respuestas: dict) -> dict:
    """
    Calcula el promedio por dimensión.
    respuestas: {"1.1": 7, "1.2": 8, ...}
    Retorna: {dim_id: {"nombre": ..., "promedio": ..., "color": ..., "detalle": [...]}}
    Cada item de detalle incluye 'id' para poder construir lookups por comportamiento.
    """
    resultado = {}
    for dim in DIMENSIONES:
        scores = []
        detalle = []
        for comp in dim["comportamientos"]:
            val = respuestas.get(comp["id"], 0)
            scores.append(val)
            detalle.append({
                "id":      comp["id"],
                "nombre":  comp["nombre"],
                "puntaje": val,
            })
        promedio = round(sum(scores) / len(scores), 2) if scores else 0
        resultado[dim["id"]] = {
            "nombre":   dim["nombre"],
            "color":    dim["color"],
            "icono":    dim["icono"],
            "promedio": promedio,
            "detalle":  detalle,
        }
    return resultado
