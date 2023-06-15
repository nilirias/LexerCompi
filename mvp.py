dir_memory = [
  #glbl
  [ 
    [0, 499],
    [500, 999 ],
    [1000, 1499],
  ],
  #lcl
  [ 
    [1500, 1999],
    [2000, 2499],
    [2500, 2999],
  ],
  #cte
  [
    [3000, 3499],
    [3500, 3999],
    [4000, 4499 ],
  ],
]

# Estructura para validación de límite de memoria 
# del segmento correspondien
limitesVarsLocales = [
  # Normales Temporales
  [4665, 5500 ], # Enteros
  [7164, 8000 ], # Flotantes
  [8666, 9000 ], # Caracteres
]

# Contador de cuántas variables hay cuando estemos en memoria local
cantVarsLocales = [
  # Normales Temporales
  [ 0,     0 ], # Enteros
  [ 0,     0 ], # Flotantes
  [ 0,     0 ], # Caracteres
]

# Template que agarra cada función para la estructura de memoria local
auxLocales = [
  # Normales Temporales
  [ [],      [] ], # Enteros
  [ [],      [] ], # Flotantes
  [ [],      [] ], # Caracteres
]

# Mapa de para guardar toda la memoria
mapa_memoria = [
  [ # Globales
    # Normales Temporales
    [ [],      [] ], # Enteros
    [ [],      [] ], # Flotantes
    [ [],      [] ], # Caracteres
  ],
  [], # Locales,
  [ # Constantes
    # Normales
    [ [] ], # Enteros
    [ [] ], # Flotantes
    [ [] ], # Caracteres
  ]
]

funciones = [] # Guarda temporalmente la información de las funciones
memoriaFuncionEnProgreso = [] # Guarda las funciones pendientes por procesar

pila_cuadruplos = [] # Stack de cuadruplos pendientes por procesar
lista_cuadruplos = [] # Guarda todos los cuadruplos a ejecutar

num_cuadruplo = [0] # Cuadruplo que se esta leyendo actualmente