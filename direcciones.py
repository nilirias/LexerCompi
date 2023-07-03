dir_memoria = [
  #NUM  WORD   BOOL
  [  0,  500,  1000 ], #GLB
  [ 1500, 2000, 2500], #LCL
  [ 3000, 3500, 4000], #TEMP
  [ 4500, 5000, 5500]  #CTE
]

# Estructura para validación de límite de memoria 
# del segmento correspondien
limitesVarsLocales = [
    #NUM  WORD   BOOL
  [  499,  999,  1499], #GLB
  [ 1999, 2499,  2999], #LCL
  [ 3499, 3999,  4499], #TEMP
  [ 4999, 5499,  4999]  #CTE
]

# Contador de cuántas variables hay cuando estemos en memoria local
cantVarsLocales = [
  #NUM   WORD   BOOL
  [0,     0,     0], # Enteros
  [0,     0,     0], # LCL
  [0,     0,     0], # TEMP
  [0,     0,     0], # CTE
]

# Template que agarra cada función para la estructura de memoria local
auxLocales = [
  #NUM     WORD    BOOL
  [[],     [],     []], # GLB
  [[],     [],     []], # LCL
  [[],     [],     []], # TEMP
  [[],     [],     []], # CTE
]

# Mapa de para guardar toda la memoria
mapa_memoria = [] #[None] * 60*100 --> [none, none ... 6000]

funciones = [] # Guarda temporalmente la información de las funciones
memoriaFuncionEnProgreso = [] # Guarda las funciones pendientes por procesar

pila_cuadruplos = [] # Stack de cuadruplos pendientes por procesar
lista_cuadruplos = [] # Guarda todos los cuadruplos a ejecutar

num_cuadruplo = [0] # Cuadruplo que se esta leyendo actualmente