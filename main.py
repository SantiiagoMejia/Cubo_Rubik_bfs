from collections import deque
import time


# =============================================================================
# SECCION 1: REPRESENTACION DEL ESTADO
# =============================================================================

def crear_cubo_resuelto():
    """
    Retorna el estado resuelto del cubo (estado objetivo / estado final f).
    Cada cara tiene sus 9 stickers del mismo color.
    Colores como enteros: 0=Blanco, 1=Rojo, 2=Azul, 3=Naranja, 4=Verde, 5=Amarillo
    """
    return [
        [0]*9,  # Cara 0: U - Arriba    (Blanco)
        [1]*9,  # Cara 1: F - Frente    (Rojo)
        [2]*9,  # Cara 2: R - Derecha   (Azul)
        [3]*9,  # Cara 3: B - Atras     (Naranja)
        [4]*9,  # Cara 4: L - Izquierda (Verde)
        [5]*9,  # Cara 5: D - Abajo     (Amarillo)
    ]


def estado_a_tupla(cubo):
    """Convierte cubo a tupla hashable (para usar en sets/dicts del BFS)."""
    return tuple(c for cara in cubo for c in cara)


def es_resuelto(cubo):
    """Verifica si cada cara tiene todos sus stickers del mismo color."""
    return all(len(set(cara)) == 1 for cara in cubo)


# =============================================================================
# SECCION 2: ROTACIONES AUXILIARES DE CARA
# =============================================================================

def rot_h(cara):
    """Rota cara 90 grados horario. Indices: 0..8 -> 6,3,0,7,4,1,8,5,2"""
    return [cara[6], cara[3], cara[0],
            cara[7], cara[4], cara[1],
            cara[8], cara[5], cara[2]]


def rot_a(cara):
    """Rota cara 90 grados antihorario. Indices: 0..8 -> 2,5,8,1,4,7,0,3,6"""
    return [cara[2], cara[5], cara[8],
            cara[1], cara[4], cara[7],
            cara[0], cara[3], cara[6]]


# =============================================================================
# SECCION 3: MOVIMIENTOS (18 en total)
# Cada funcion retorna un nuevo estado sin modificar el original.
# =============================================================================

def aplicar_movimiento(cubo, nombre):
    """
    Dispatcher central: aplica el movimiento indicado al cubo.
    Retorna el nuevo estado.
    """
    c = [list(cara) for cara in cubo]

    if nombre == 'X1R':
        # Fila superior a la derecha. Cara U rota horario.
        c[0] = rot_h(cubo[0])
        c[1][0],c[1][1],c[1][2] = cubo[4][0],cubo[4][1],cubo[4][2]
        c[2][0],c[2][1],c[2][2] = cubo[1][0],cubo[1][1],cubo[1][2]
        c[3][0],c[3][1],c[3][2] = cubo[2][0],cubo[2][1],cubo[2][2]
        c[4][0],c[4][1],c[4][2] = cubo[3][0],cubo[3][1],cubo[3][2]
    elif nombre == 'X1L':
        # Fila superior a la izquierda. Cara U rota antihorario.
        c[0] = rot_a(cubo[0])
        c[1][0],c[1][1],c[1][2] = cubo[2][0],cubo[2][1],cubo[2][2]
        c[2][0],c[2][1],c[2][2] = cubo[3][0],cubo[3][1],cubo[3][2]
        c[3][0],c[3][1],c[3][2] = cubo[4][0],cubo[4][1],cubo[4][2]
        c[4][0],c[4][1],c[4][2] = cubo[1][0],cubo[1][1],cubo[1][2]
    elif nombre == 'X2R':
        # Fila central a la derecha. Sin rotacion de cara principal.
        c[1][3],c[1][4],c[1][5] = cubo[4][3],cubo[4][4],cubo[4][5]
        c[2][3],c[2][4],c[2][5] = cubo[1][3],cubo[1][4],cubo[1][5]
        c[3][3],c[3][4],c[3][5] = cubo[2][3],cubo[2][4],cubo[2][5]
        c[4][3],c[4][4],c[4][5] = cubo[3][3],cubo[3][4],cubo[3][5]
    elif nombre == 'X2L':
        c[1][3],c[1][4],c[1][5] = cubo[2][3],cubo[2][4],cubo[2][5]
        c[2][3],c[2][4],c[2][5] = cubo[3][3],cubo[3][4],cubo[3][5]
        c[3][3],c[3][4],c[3][5] = cubo[4][3],cubo[4][4],cubo[4][5]
        c[4][3],c[4][4],c[4][5] = cubo[1][3],cubo[1][4],cubo[1][5]
    elif nombre == 'X3R':
        # Fila inferior a la derecha. Cara D rota antihorario.
        c[5] = rot_a(cubo[5])
        c[1][6],c[1][7],c[1][8] = cubo[4][6],cubo[4][7],cubo[4][8]
        c[2][6],c[2][7],c[2][8] = cubo[1][6],cubo[1][7],cubo[1][8]
        c[3][6],c[3][7],c[3][8] = cubo[2][6],cubo[2][7],cubo[2][8]
        c[4][6],c[4][7],c[4][8] = cubo[3][6],cubo[3][7],cubo[3][8]
    elif nombre == 'X3L':
        # Fila inferior a la izquierda. Cara D rota horario.
        c[5] = rot_h(cubo[5])
        c[1][6],c[1][7],c[1][8] = cubo[2][6],cubo[2][7],cubo[2][8]
        c[2][6],c[2][7],c[2][8] = cubo[3][6],cubo[3][7],cubo[3][8]
        c[3][6],c[3][7],c[3][8] = cubo[4][6],cubo[4][7],cubo[4][8]
        c[4][6],c[4][7],c[4][8] = cubo[1][6],cubo[1][7],cubo[1][8]
    elif nombre == 'Y1U':
        # Columna izquierda hacia arriba. Cara L rota horario.
        c[4] = rot_h(cubo[4])
        c[0][0],c[0][3],c[0][6] = cubo[1][0],cubo[1][3],cubo[1][6]
        c[1][0],c[1][3],c[1][6] = cubo[5][0],cubo[5][3],cubo[5][6]
        c[5][0],c[5][3],c[5][6] = cubo[3][8],cubo[3][5],cubo[3][2]
        c[3][8],c[3][5],c[3][2] = cubo[0][0],cubo[0][3],cubo[0][6]
    elif nombre == 'Y1D':
        # Columna izquierda hacia abajo. Cara L rota antihorario.
        c[4] = rot_a(cubo[4])
        c[0][0],c[0][3],c[0][6] = cubo[3][8],cubo[3][5],cubo[3][2]
        c[1][0],c[1][3],c[1][6] = cubo[0][0],cubo[0][3],cubo[0][6]
        c[5][0],c[5][3],c[5][6] = cubo[1][0],cubo[1][3],cubo[1][6]
        c[3][8],c[3][5],c[3][2] = cubo[5][0],cubo[5][3],cubo[5][6]
    elif nombre == 'Y2U':
        # Columna central hacia arriba.
        c[0][1],c[0][4],c[0][7] = cubo[1][1],cubo[1][4],cubo[1][7]
        c[1][1],c[1][4],c[1][7] = cubo[5][1],cubo[5][4],cubo[5][7]
        c[5][1],c[5][4],c[5][7] = cubo[3][7],cubo[3][4],cubo[3][1]
        c[3][7],c[3][4],c[3][1] = cubo[0][1],cubo[0][4],cubo[0][7]
    elif nombre == 'Y2D':
        c[0][1],c[0][4],c[0][7] = cubo[3][7],cubo[3][4],cubo[3][1]
        c[1][1],c[1][4],c[1][7] = cubo[0][1],cubo[0][4],cubo[0][7]
        c[5][1],c[5][4],c[5][7] = cubo[1][1],cubo[1][4],cubo[1][7]
        c[3][7],c[3][4],c[3][1] = cubo[5][1],cubo[5][4],cubo[5][7]
    elif nombre == 'Y3U':
        # Columna derecha hacia arriba. Cara R rota antihorario.
        c[2] = rot_a(cubo[2])
        c[0][2],c[0][5],c[0][8] = cubo[1][2],cubo[1][5],cubo[1][8]
        c[1][2],c[1][5],c[1][8] = cubo[5][2],cubo[5][5],cubo[5][8]
        c[5][2],c[5][5],c[5][8] = cubo[3][6],cubo[3][3],cubo[3][0]
        c[3][6],c[3][3],c[3][0] = cubo[0][2],cubo[0][5],cubo[0][8]
    elif nombre == 'Y3D':
        # Columna derecha hacia abajo. Cara R rota horario.
        c[2] = rot_h(cubo[2])
        c[0][2],c[0][5],c[0][8] = cubo[3][6],cubo[3][3],cubo[3][0]
        c[1][2],c[1][5],c[1][8] = cubo[0][2],cubo[0][5],cubo[0][8]
        c[5][2],c[5][5],c[5][8] = cubo[1][2],cubo[1][5],cubo[1][8]
        c[3][6],c[3][3],c[3][0] = cubo[5][2],cubo[5][5],cubo[5][8]
    elif nombre == 'Z1R':
        # Capa frontal horario. Cara F rota horario.
        c[1] = rot_h(cubo[1])
        c[0][6],c[0][7],c[0][8] = cubo[4][8],cubo[4][5],cubo[4][2]
        c[2][0],c[2][3],c[2][6] = cubo[0][6],cubo[0][7],cubo[0][8]
        c[5][2],c[5][1],c[5][0] = cubo[2][0],cubo[2][3],cubo[2][6]
        c[4][8],c[4][5],c[4][2] = cubo[5][0],cubo[5][1],cubo[5][2]
    elif nombre == 'Z1L':
        # Capa frontal antihorario. Cara F rota antihorario.
        c[1] = rot_a(cubo[1])
        c[0][6],c[0][7],c[0][8] = cubo[2][0],cubo[2][3],cubo[2][6]
        c[4][8],c[4][5],c[4][2] = cubo[0][6],cubo[0][7],cubo[0][8]
        c[5][0],c[5][1],c[5][2] = cubo[4][8],cubo[4][5],cubo[4][2]
        c[2][0],c[2][3],c[2][6] = cubo[5][2],cubo[5][1],cubo[5][0]
    elif nombre == 'Z2R':
        # Capa central frontal horario.
        c[0][3],c[0][4],c[0][5] = cubo[4][7],cubo[4][4],cubo[4][1]
        c[2][1],c[2][4],c[2][7] = cubo[0][3],cubo[0][4],cubo[0][5]
        c[5][5],c[5][4],c[5][3] = cubo[2][1],cubo[2][4],cubo[2][7]
        c[4][7],c[4][4],c[4][1] = cubo[5][3],cubo[5][4],cubo[5][5]
    elif nombre == 'Z2L':
        c[0][3],c[0][4],c[0][5] = cubo[2][1],cubo[2][4],cubo[2][7]
        c[4][7],c[4][4],c[4][1] = cubo[0][3],cubo[0][4],cubo[0][5]
        c[5][3],c[5][4],c[5][5] = cubo[4][7],cubo[4][4],cubo[4][1]
        c[2][1],c[2][4],c[2][7] = cubo[5][5],cubo[5][4],cubo[5][3]
    elif nombre == 'Z3R':
        # Capa trasera. Cara B rota antihorario.
        c[3] = rot_a(cubo[3])
        c[0][0],c[0][1],c[0][2] = cubo[2][8],cubo[2][5],cubo[2][2]
        c[4][0],c[4][3],c[4][6] = cubo[0][2],cubo[0][1],cubo[0][0]
        c[5][8],c[5][7],c[5][6] = cubo[4][0],cubo[4][3],cubo[4][6]
        c[2][2],c[2][5],c[2][8] = cubo[5][6],cubo[5][7],cubo[5][8]
    elif nombre == 'Z3L':
        # Capa trasera antihorario. Cara B rota horario.
        c[3] = rot_h(cubo[3])
        c[0][0],c[0][1],c[0][2] = cubo[4][6],cubo[4][3],cubo[4][0]
        c[2][2],c[2][5],c[2][8] = cubo[0][0],cubo[0][1],cubo[0][2]
        c[5][6],c[5][7],c[5][8] = cubo[2][8],cubo[2][5],cubo[2][2]
        c[4][0],c[4][3],c[4][6] = cubo[5][8],cubo[5][7],cubo[5][6]
    return c


# Los 18 movimientos 
TODOS_MOVIMIENTOS = [
    'X1R','X1L','X2R','X2L','X3R','X3L',
    'Y1U','Y1D','Y2U','Y2D','Y3U','Y3D',
    'Z1R','Z1L','Z2R','Z2L','Z3R','Z3L',
]

# Movimiento inverso de cada uno
INVERSO = {
    'X1R':'X1L','X1L':'X1R','X2R':'X2L','X2L':'X2R','X3R':'X3L','X3L':'X3R',
    'Y1U':'Y1D','Y1D':'Y1U','Y2U':'Y2D','Y2D':'Y2U','Y3U':'Y3D','Y3D':'Y3U',
    'Z1R':'Z1L','Z1L':'Z1R','Z2R':'Z2L','Z2L':'Z2R','Z3R':'Z3L','Z3L':'Z3R',
}


# =============================================================================
# SECCION 4: BFS BIDIRECCIONAL
# =============================================================================

def bfs_bidireccional(estado_inicial, estado_objetivo):
    """
    BFS Bidireccional: busca simultáneamente desde s0 (inicio) y desde f
    (objetivo), uniendose al encontrar un estado comun.

    Ventaja clave sobre BFS simple:
        - BFS simple:        O(b^d) nodos     donde b=18, d=pasos solución
        - BFS bidireccional: O(2 x b^(d/2))  — exponencialmente menor
        - Ejemplo d=4: simple=104,976 nodos vs bidireccional=648 nodos

    Pseudocodigo (extension del BFS del taller):
        BFS_Bidirecional(inicio, objetivo):
            cola_fwd = {inicio: []}    -- caminos desde inicio
            cola_bwd = {objetivo: []}  -- caminos desde objetivo
            mientras ambas colas no esten vacias:
                expandir la cola mas pequena
                para cada vecino del estado actual:
                    si el vecino esta en la otra cola:
                        UNION: concatenar caminos --> solucion encontrada
                    si no visitado: encolar vecino

    Args:
        estado_inicial:  Cubo mezclado (estado s0).
        estado_objetivo: Cubo resuelto (estado f).
    Returns:
        (solucion, estadisticas)
    """
    print("\n" + "="*60)
    print("  INICIANDO BFS BIDIRECCIONAL")
    print("  Buscando desde inicio Y desde objetivo simultaneamente")
    print("="*60)

    t_inicio = time.time()

    if es_resuelto(estado_inicial):
        return [], {'nodos_explorados': 0, 'tiempo': 0, 'profundidad': 0}

    tup_ini = estado_a_tupla(estado_inicial)
    tup_obj = estado_a_tupla(estado_objetivo)

    # Fronteras activas: estado_tupla -> camino de movimientos
    frontera_fwd = {tup_ini: []}      # Desde el inicio
    frontera_bwd = {tup_obj: []}      # Desde el objetivo

    # Todos los estados visitados con su camino
    visitados_fwd = {tup_ini: []}
    visitados_bwd = {tup_obj: []}

    # Cubos reales para aplicar movimientos
    cubos_fwd = {tup_ini: estado_inicial}
    cubos_bwd = {tup_obj: estado_objetivo}

    nodos = 0
    nivel = 0

    while frontera_fwd and frontera_bwd:
        nivel += 1
        print(f"  Nivel {nivel}: fwd={len(frontera_fwd)} estados | bwd={len(frontera_bwd)} estados")

        # Expandir la frontera mas pequeña (estrategia de balance)
        expandir_fwd = len(frontera_fwd) <= len(frontera_bwd)

        nueva_frontera = {}
        nuevos_cubos = {}

        if expandir_fwd:
            fuente       = frontera_fwd
            fuente_cubos = cubos_fwd
            vis_propio   = visitados_fwd
            vis_otro     = visitados_bwd
        else:
            fuente       = frontera_bwd
            fuente_cubos = cubos_bwd
            vis_propio   = visitados_bwd
            vis_otro     = visitados_fwd

        for tup, camino in fuente.items():
            cubo_actual = fuente_cubos[tup]

            for mov in TODOS_MOVIMIENTOS:
                # Poda: no deshacer inmediatamente el ultimo movimiento
                if camino and mov == INVERSO[camino[-1]]:
                    continue

                # Al expandir hacia adelante: aplica el movimiento normal
                # Al expandir hacia atras:    aplica el inverso (deshace desde objetivo)
                mov_real  = mov if expandir_fwd else INVERSO[mov]
                nuevo_cubo   = aplicar_movimiento(cubo_actual, mov_real)
                nuevo_tup    = estado_a_tupla(nuevo_cubo)
                nuevo_camino = camino + [mov]
                nodos += 1

                # PUNTO DE UNION: encontramos un estado visitado por la otra busqueda
                if nuevo_tup in vis_otro:
                    camino_otro = vis_otro[nuevo_tup]

                    if expandir_fwd:
                        # nuevo_camino = camino FWD desde inicio hasta nodo union
                        # camino_otro  = camino BWD registrado como lista de movs 'M'
                        #   donde cada 'M' significa que se aplico INVERSO(M) desde objetivo.
                        #   Para ir del nodo union al objetivo, simplemente se aplica M.
                        solucion = nuevo_camino + camino_otro
                    else:
                        # nuevo_camino = camino BWD desde objetivo hasta nodo union
                        # camino_otro  = camino FWD desde inicio hasta nodo union
                        #   Para ir del nodo union al objetivo, aplicamos nuevo_camino directamente.
                        solucion = camino_otro + nuevo_camino

                    t_total = time.time() - t_inicio
                    print(f"\n  Union encontrada en nivel {nivel}!")
                    print(f"  Nodos explorados: {nodos:,}")
                    print(f"  Tiempo: {t_total:.4f}s")
                    return solucion, {
                        'nodos_explorados': nodos,
                        'tiempo': t_total,
                        'profundidad': len(solucion)
                    }

                if nuevo_tup not in vis_propio:
                    vis_propio[nuevo_tup] = nuevo_camino
                    nueva_frontera[nuevo_tup] = nuevo_camino
                    nuevos_cubos[nuevo_tup] = nuevo_cubo

        if expandir_fwd:
            frontera_fwd = nueva_frontera
            cubos_fwd    = nuevos_cubos
        else:
            frontera_bwd = nueva_frontera
            cubos_bwd    = nuevos_cubos

    t_total = time.time() - t_inicio
    return None, {'nodos_explorados': nodos, 'tiempo': t_total, 'profundidad': 0}


# =============================================================================
# SECCION 5: BFS SIMPLE (para comparacion en tabla del informe)
# =============================================================================

def bfs_simple(estado_inicial, limite_prof=4):
    """
    BFS simple clasico con limite de profundidad para comparacion.
    Implementa el pseudocodigo del taller directamente:

        BFS(grafo, inicio):
            crear cola Q
            marcar inicio como visitado
            Q.encolar(inicio)
            mientras Q no este vacia:
                v = Q.desencolar()
                para cada vecino u de v:
                    si u no ha sido visitado:
                        marcar u como visitado
                        Q.encolar(u)
    """
    t_inicio = time.time()
    if es_resuelto(estado_inicial):
        return [], {'nodos': 0, 'tiempo': 0}

    # Cola FIFO: (cubo_actual, camino)
    cola = deque()
    cola.append((estado_inicial, []))
    visitados = {estado_a_tupla(estado_inicial)}
    nodos = 0

    while cola:
        estado_actual, camino = cola.popleft()
        nodos += 1
        if len(camino) >= limite_prof:
            continue
        for mov in TODOS_MOVIMIENTOS:
            if camino and mov == INVERSO[camino[-1]]:
                continue
            nuevo = aplicar_movimiento(estado_actual, mov)
            tup = estado_a_tupla(nuevo)
            if tup in visitados:
                continue
            nuevo_camino = camino + [mov]
            if es_resuelto(nuevo):
                return nuevo_camino, {'nodos': nodos, 'tiempo': time.time()-t_inicio}
            visitados.add(tup)
            cola.append((nuevo, nuevo_camino))

    return None, {'nodos': nodos, 'tiempo': time.time()-t_inicio}


# =============================================================================
# SECCION 6: VISUALIZACION EN CONSOLA
# =============================================================================

NOMBRES = {0:'W', 1:'R', 2:'B', 3:'O', 4:'G', 5:'Y'}


def imprimir_cubo(cubo, titulo=""):
    """Imprime el cubo en formato de cruz desplegada."""
    if titulo:
        print(f"\n  {titulo}")
        print("  " + "-"*40)
    print("            [U - Arriba/Blanco]")
    for i in range(3):
        print("            " + " ".join(NOMBRES[cubo[0][i*3+j]] for j in range(3)))
    print("  [L-Izq]  [F-Frente]  [R-Der]  [B-Atras]")
    for i in range(3):
        L = " ".join(NOMBRES[cubo[4][i*3+j]] for j in range(3))
        F = " ".join(NOMBRES[cubo[1][i*3+j]] for j in range(3))
        R = " ".join(NOMBRES[cubo[2][i*3+j]] for j in range(3))
        B = " ".join(NOMBRES[cubo[3][i*3+j]] for j in range(3))
        print(f"  {L}    {F}     {R}    {B}")
    print("            [D - Abajo/Amarillo]")
    for i in range(3):
        print("            " + " ".join(NOMBRES[cubo[5][i*3+j]] for j in range(3)))
    print()


# =============================================================================
# SECCION 7: PROGRAMA PRINCIPAL
# =============================================================================

def main():
    print("\n" + "="*60)
    print("  TALLER: BFS PARA EL CUBO RUBIK")
    print("  Nomenclatura: X/Y/Z")
    print("="*60)

    # 1. Estado resuelto (objetivo)
    cubo_objetivo = crear_cubo_resuelto()
    imprimir_cubo(cubo_objetivo, "Estado Objetivo — Cubo Resuelto (f)")

    # 2. Mezcla con 3 movimientos usando nomenclatura 
    mezcla = ['X1R', 'Y3D', 'Z1R']
    print(f"  Secuencia de mezcla aplicada: {' -> '.join(mezcla)}")
    inv_esperada = ' -> '.join(INVERSO[m] for m in reversed(mezcla))
    print(f"  Solucion optima esperada (inversos): {inv_esperada}")

    cubo_inicial = cubo_objetivo
    for mov in mezcla:
        cubo_inicial = aplicar_movimiento(cubo_inicial, mov)
    print()
    imprimir_cubo(cubo_inicial, f"Estado Inicial s0 (mezclado con {len(mezcla)} movimientos)")

    # 3. BFS Bidireccional
    solucion, stats_bi = bfs_bidireccional(cubo_inicial, cubo_objetivo)

    # 4. BFS Simple para comparacion
    print("\n" + "="*60)
    print("  BFS SIMPLE — referencia para tabla comparativa del informe")
    print("="*60)
    _, stats_simple = bfs_simple(cubo_inicial, limite_prof=len(mezcla)+1)
    print(f"  Nodos BFS simple (hasta prof {len(mezcla)+1}): {stats_simple['nodos']:,}")
    print(f"  Tiempo BFS simple: {stats_simple['tiempo']:.4f}s")

    # 5. Mostrar y verificar solucion
    if solucion:
        print("\n" + "="*60)
        print("  SOLUCION — Secuencia minima de movimientos:")
        print("="*60)
        for i, mov in enumerate(solucion, 1):
            print(f"    Paso {i}: {mov}")

        cubo_v = cubo_inicial
        for mov in solucion:
            cubo_v = aplicar_movimiento(cubo_v, mov)
        imprimir_cubo(cubo_v, "Cubo tras aplicar la solucion")
        ok = es_resuelto(cubo_v)
        print(f"  Verificacion: {'CORRECTO — Cubo resuelto!' if ok else 'ERROR — Revisar logica'}")

    # 6. Tabla comparativa para el informe
    n_sol = len(solucion) if solucion else 'N/A'
    print("\n" + "="*60)
    print("  TABLA COMPARATIVA — BFS Simple vs BFS Bidireccional")
    print("="*60)
    print(f"  {'Metrica':<36} {'BFS Simple':>12} {'BFS Bidir.':>12}")
    print(f"  {'-'*60}")
    print(f"  {'Movimientos en la solucion':<36} {len(mezcla):>12} {n_sol:>12}")
    print(f"  {'Nodos explorados':<36} {stats_simple['nodos']:>12,} {stats_bi['nodos_explorados']:>12,}")
    print(f"  {'Tiempo de busqueda (seg)':<36} {stats_simple['tiempo']:>12.4f} {stats_bi['tiempo']:>12.4f}")
    print(f"  {'Optimalidad garantizada':<36} {'Si':>12} {'Si':>12}")
    print(f"  {'Complejidad temporal':<36} {'O(b^d)':>12} {'O(2*b^d/2)':>12}")
    print(f"  {'Complejidad espacial':<36} {'O(b^d)':>12} {'O(2*b^d/2)':>12}")
    print(f"  {'Movimientos (b) disponibles':<36} {18:>12} {18:>12}")
    print("="*60)

    return solucion, stats_bi, stats_simple


if __name__ == "__main__":
    solucion, stats_bi, stats_simple = main()