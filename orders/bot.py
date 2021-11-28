import nltk
from nltk.chat.util import Chat, reflections


reflections = {
    "yo soy": "tu eres",
    "Yo era": "tú eras",
    "Yo": "tú",
    "yo soy": "tú eres",
    "yo haría": "tú lo harías",
    "tengo": "tienes",
    "lo haré": "lo harás",
    "mio": "tuyo",
    "tu eres": "yo soy",
    "tú eras": "yo era",
    "tienes": "yo tengo",
    "usted": "lo haré",
    "tu": "mi",
    "tuyo": "mío",
    "tu": "yo",
    "yo": "tú",
}

pairs = [
    [
        r"mi nombre es(.*)",
        ["Hola %1, Como estás ?", ]
    ],
    [
        r"hola|oye|buenas",
        ["Hola", "¿Que tal en que le puedo ayudar?", ]
    ],
    [
        r"cual es tu nombre(.*)",
        ["Mi nombre es androide 19, fui diseñado por el doctor Gero, especificamente para servir a los clientes como usted.", ]
    ],
    [
        r"sorry(.*)",
        ["No hay problema", "No te preocupes", ]
    ],

    [
        r"ayuda(.*)|instrucciones(.*)",
        [
            "-Instruccioens -1 para xd \n -2 para xd2 \n -3 para xd3"]
    ],
    [
        r"ingredientes (.*)",
        [
            "Le recomiendo este plato"]
    ],
    [
        r"(.*)",
        [
            "No he entendido su solicitud por favor intentelo nuevamente"]
    ],
]
