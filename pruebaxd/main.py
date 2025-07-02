import pygame

pygame.init()
pygame.mixer.init()

def detener_musica():
    pygame.mixer.music.stop()

musica_actual = None

def cambiar_musica(estado):
    global musica_actual
    ruta = musicas.get(estado)
    if ruta and ruta != musica_actual:
        reproducir_musica(ruta)
        musica_actual = ruta

def reproducir_musica(ruta, bucle=True, volumen=0.5):
    global musica_actual
    if musica_actual != ruta:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1 if bucle else 0)
        musica_actual = ruta

def obtener_rango(indice_nivel, ganador):
    if ganador:
        return "Reponedor legendario"
    rangos = [
        "Pésimo reponedor",
        "Reponedor mediocre",
        "Reponedor regular",
        "Reponedor ordinario",
        "Reponedor decente",
        "Reponedor bueno",
        "Reponedor muy bueno",
        "Reponedor casi perfecto"
    ]
    return rangos[min(indice_nivel, len(rangos) - 1)]

fuente_personalizada = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 40)
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Adolmoi Stock System")

icono_juego = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\iconojuego.png")
pygame.display.set_icon(icono_juego)

imagen_titulo = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\Adolmoi.jpg").convert()
imagen_titulo = pygame.transform.scale(imagen_titulo, (800, 600))

imagen_bodega = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\pared.jpg").convert()
imagen_bodega = pygame.transform.scale(imagen_bodega, (800, 600))

imagen_instrucciones = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\bodega interior.jpg").convert()
imagen_instrucciones = pygame.transform.scale(imagen_instrucciones,(800, 600))

imagen_fin = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\bodega interior 2.jpg").convert()
imagen_fin = pygame.transform.scale(imagen_fin, (800, 600))

imagen_gameover = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\Game over o time out.png").convert()
imagen_gameover = pygame.transform.scale(imagen_gameover, (800, 600))

sprite_circulo = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\sprites\\circulo.png").convert_alpha()
sprite_cuadrado = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\sprites\\cuadrado.png").convert_alpha()
sprite_triangulo = pygame.image.load("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\sprites\\triangulo.png").convert_alpha()

etiqueta_circulo = pygame.transform.scale(sprite_circulo, (40, 40))
etiqueta_cuadrado = pygame.transform.scale(sprite_cuadrado, (40, 40))
etiqueta_triangulo = pygame.transform.scale(sprite_triangulo, (40, 40))

estado = "intro"
tiempo_inicio = pygame.time.get_ticks()

musicas = {
    "intro": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Splash Screen.mp3",
    "titulo": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Titulo.mp3",
    "instrucciones": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\musica\\Instrucciones.mp3",
    "nivel": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Nivel.mp3",
    "alarma": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Alarma.mp3",
    "gameover": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Game Over.mp3",
    "fin": "C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Fin.mp3"
}

TAM_CELDA = 80
MARGEN = 10
ORIGEN_X = 100
ORIGEN_Y = 150
tiempos_por_nivel = [
    35000,  # Nivel 1 - 35s
    30000,  # Nivel 2 - 30s
    30000,  # Nivel 3 - 30s
    30000,  # Nivel 4 - 30s
    30000,  # Nivel 5 - 30s
    35000,  # Nivel 6 - 35s
    30000,  # Nivel 7 - 40s
    25000   # Nivel 8 - 25s
]
tiempo_nivel_actual = None

niveles = [
    [["", "", "□", "", "", ""], ["", "△", "", "○", "", ""], ["", "", "", "", "", ""]],
    [["", "○", "□", "", "", ""], ["△", "", "○", "", "", ""], ["", "□", "△", "", "", ""]],
    [["△", "", "○", "", "", "□"], ["", "", "△", "□", "", ""], ["", "", "○", "", "", ""]],
    [["□", "", "△", "", "○", ""], ["", "○", "", "△", "", ""], ["", "□", "", "", "", ""]],
    [["□", "△", "○", "□", "△", ""], ["○", "□", "△", "○", "", "△"], ["", "○", "□", "△", "□", "○"]],
    [["△", "○", "□", "△", "○", "□"], ["□", "△", "○", "", "", ""], ["○", "□", "△", "", "", ""]],
    [["○", "△", "", "○", "○", "△"], ["△", "", "○", "○", "△", ""], ["△", "□", "□", "", "", "△"]],
    [["△", "□", "△", "△", "△", "○"], ["○", "△", "○", "○", "", "□"], ["□", "□", "□", "△", "□", "○"]]
]

indice_nivel = 0
bodega_1 = [fila[:] for fila in niveles[indice_nivel]]

arrastrando = False
pieza_seleccionada = None
pos_relativa_mouse = (0, 0)
pos_inicial = None

ganador = False
tiempo_ganador = None

boton_jugar = None
boton_instrucciones = None
boton_reinicio = None
boton_gameover = None

def verificar_ganador(tablero):
    for fila in range(3):
        for col in range(6):
            figura = tablero[fila][col]
            if figura == "○" and fila != 0:
                return False
            elif figura == "□" and fila != 1:
                return False
            elif figura == "△" and fila != 2:
                return False
    return True

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if estado == "titulo" and evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_jugar and boton_jugar.collidepoint(evento.pos):
                estado = "instrucciones"

        if estado == "instrucciones" and evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_instrucciones and boton_instrucciones.collidepoint(evento.pos):
                estado = "bodega_1"
                tiempo_nivel_actual = pygame.time.get_ticks()

        if estado == "bodega_1" and not ganador:
            if evento.type == pygame.MOUSEBUTTONDOWN and not arrastrando:
                mx, my = evento.pos
                for fila in range(3):
                    for col in range(6):
                        x = ORIGEN_X + col * (TAM_CELDA + MARGEN)
                        y = ORIGEN_Y + fila * (TAM_CELDA + MARGEN)
                        rect_celda = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
                        if rect_celda.collidepoint(mx, my) and bodega_1[fila][col] != "":
                            arrastrando = True
                            pieza_seleccionada = bodega_1[fila][col]
                            pos_relativa_mouse = (mx - x, my - y)
                            pos_inicial = (fila, col)
                            bodega_1[fila][col] = ""
                            break
                    if arrastrando:
                        break

            elif evento.type == pygame.MOUSEBUTTONUP and arrastrando:
                mx, my = evento.pos
                col_dest = (mx - ORIGEN_X) // (TAM_CELDA + MARGEN)
                fila_dest = (my - ORIGEN_Y) // (TAM_CELDA + MARGEN)
                if 0 <= fila_dest < 3 and 0 <= col_dest < 6:
                    correcto = False
                    if pieza_seleccionada == "○" and fila_dest == 0:
                        correcto = True
                    elif pieza_seleccionada == "□" and fila_dest == 1:
                        correcto = True
                    elif pieza_seleccionada == "△" and fila_dest == 2:
                        correcto = True
                    if correcto and bodega_1[fila_dest][col_dest] == "":
                        bodega_1[fila_dest][col_dest] = pieza_seleccionada
                    else:
                        fila_ini, col_ini = pos_inicial
                        bodega_1[fila_ini][col_ini] = pieza_seleccionada
                else:
                    fila_ini, col_ini = pos_inicial
                    bodega_1[fila_ini][col_ini] = pieza_seleccionada

                arrastrando = False
                pieza_seleccionada = None
                pos_inicial = None

                if verificar_ganador(bodega_1):
                    ganador = True
                    tiempo_ganador = pygame.time.get_ticks()

        if estado in ["fin", "game_over"] and evento.type == pygame.MOUSEBUTTONDOWN:
            if (estado == "fin" and boton_reinicio and boton_reinicio.collidepoint(evento.pos)) or \
               (estado == "game_over" and boton_gameover and boton_gameover.collidepoint(evento.pos)):
                estado = "titulo"
                indice_nivel = 0
                bodega_1 = [fila[:] for fila in niveles[indice_nivel]]
                ganador = False
                tiempo_ganador = None

    if estado == "intro":
        cambiar_musica("intro")
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 60)
        texto = fuente.render("AndyGames Presenta", True, (0, 0, 128))
        texto_rect = texto.get_rect(center=(400, 300))
        pantalla.blit(texto, texto_rect)

        if pygame.time.get_ticks() - tiempo_inicio > 3000:
            estado = "titulo"

    elif estado == "titulo":
        cambiar_musica("titulo")
        pantalla.blit(imagen_titulo, (0, 0))
        fuente = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 76)
        texto = fuente.render("Adolmoi Stock System", True, (255, 172, 28))
        pantalla.blit(texto, (100, 100))

        boton_jugar = pygame.Rect(300, 300, 200, 80)
        pygame.draw.rect(pantalla, (0, 143, 80), boton_jugar)

        fuente_boton = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf",20)
        texto_jugar = fuente_boton.render("Comenzar a ordenar stocks", True, (0, 0, 0))
        texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
        pantalla.blit(texto_jugar, texto_rect)

    elif estado == "instrucciones":
        cambiar_musica("instrucciones")
        pantalla.blit(imagen_instrucciones, (0, 0))
        fuente = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 40)
        instrucciones = [
            "Instrucciones",
            "- Arrastra las formas en los estantes que van",
            "- Cada figura solo puede colocarse en su fila correcta",
            "- Ganas cuando todas las formas están en su lugar",
            "- No dejes que se te acabe el tiempo"
        ]

        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, (255, 255, 0))
            pantalla.blit(texto, (50, 50 + i * 50))

        boton_instrucciones = pygame.Rect(250, 450, 300, 80)
        pygame.draw.rect(pantalla, (0, 143, 80), boton_instrucciones)
        texto_boton = fuente.render("Comenzar de una vez", True, (255, 255, 255))
        texto_rect = texto_boton.get_rect(center=boton_instrucciones.center)
        pantalla.blit(texto_boton, texto_rect)


        def obtener_tiempo_restante():
            if tiempo_nivel_actual is None:
                return None
            transcurrido = pygame.time.get_ticks() - tiempo_nivel_actual
            return max(0, (tiempos_por_nivel[indice_nivel] - transcurrido) // 1000)
        


    elif estado == "bodega_1":
        tiempo_restante = obtener_tiempo_restante()
        if tiempo_restante is not None and tiempo_restante <= 15:
            cambiar_musica("alarma")
        else:
            cambiar_musica("nivel")
        pantalla.blit(imagen_bodega, (0, 0))
        fuente_nivel = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 100)
        texto_nivel = fuente_nivel.render(f"Bodega {indice_nivel + 1}", True, (50, 50, 50))
        rect_nivel = texto_nivel.get_rect(center=(400, 40))
        pantalla.blit(texto_nivel, rect_nivel)

        if not ganador:
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_nivel_actual
        else:
            tiempo_transcurrido = tiempos_por_nivel[indice_nivel]
        tiempo_restante = max(0, (tiempos_por_nivel[indice_nivel] - tiempo_transcurrido) // 1000)
        if not ganador:
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_nivel_actual
        else:
            tiempo_transcurrido = tiempos_por_nivel[indice_nivel]
        tiempo_restante = max(0, (tiempos_por_nivel[indice_nivel] - tiempo_transcurrido) // 1000)
        color_tiempo = (255, 0, 0) if tiempo_restante <= 15 else (0, 255, 0)
        fuente_tiempo = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 60)
        texto_tiempo = fuente_tiempo.render(f"Tiempo restante: {tiempo_restante}s", True, color_tiempo)
        pantalla.blit(texto_tiempo, (300, 70))
        if not ganador and tiempo_transcurrido >= tiempos_por_nivel[indice_nivel]:
            estado = "game_over"

        estante_ancho = 6 * (TAM_CELDA + MARGEN) + MARGEN
        estante_alto = 3 * (TAM_CELDA + MARGEN) + MARGEN
        pygame.draw.rect(pantalla, (139, 69, 19), (ORIGEN_X - MARGEN, ORIGEN_Y - MARGEN, estante_ancho, estante_alto))

        for fila in range(3):
            y = ORIGEN_Y + fila * (TAM_CELDA + MARGEN) + (TAM_CELDA - 40) // 2
            if fila == 0:
                pantalla.blit(etiqueta_circulo, (ORIGEN_X - 50, y))
            elif fila == 1:
                pantalla.blit(etiqueta_cuadrado, (ORIGEN_X - 50, y))
            elif fila == 2:
                pantalla.blit(etiqueta_triangulo, (ORIGEN_X - 50, y))
            for col in range(6):
                x = ORIGEN_X + col * (TAM_CELDA + MARGEN)
                y = ORIGEN_Y + fila * (TAM_CELDA + MARGEN)
                pygame.draw.rect(pantalla, (245, 222, 179), (x, y, TAM_CELDA, TAM_CELDA))
                pygame.draw.rect(pantalla, (101, 67, 33), (x, y, TAM_CELDA, TAM_CELDA), 4)

                figura = bodega_1[fila][col]
                if figura == "○":
                    pantalla.blit(sprite_circulo, (x, y))
                elif figura == "□":
                    pantalla.blit(sprite_cuadrado, (x, y))
                elif figura == "△":
                    pantalla.blit(sprite_triangulo, (x, y))

        

        if arrastrando and pieza_seleccionada is not None:
            mx, my = pygame.mouse.get_pos()
            x_dibujo = mx - pos_relativa_mouse[0]
            y_dibujo = my - pos_relativa_mouse[1]

            if pieza_seleccionada == "○":
                pantalla.blit(sprite_circulo, (x_dibujo, y_dibujo))
            elif pieza_seleccionada == "□":
                pantalla.blit(sprite_cuadrado, (x_dibujo, y_dibujo))
            elif pieza_seleccionada == "△":
                pantalla.blit(sprite_triangulo, (x_dibujo, y_dibujo))

        if ganador:
            fuente_ganador = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 72)
            texto_ganador = fuente_ganador.render("¡Ganaste!", True, (0, 128, 0))
            rect_ganador = texto_ganador.get_rect(center=(400, 550))
            pantalla.blit(texto_ganador, rect_ganador)

            if pygame.time.get_ticks() - tiempo_ganador > 3000:
                indice_nivel += 1
                if indice_nivel < len(niveles):
                    bodega_1 = [fila[:] for fila in niveles[indice_nivel]]
                    ganador = False
                    tiempo_ganador = None
                    tiempo_nivel_actual = pygame.time.get_ticks()
                else:
                    estado = "fin"

    elif estado == "fin":
        tiempo_estado = pygame.time.get_ticks()
        sonido_rango_reproducido = False
        cambiar_musica("fin")
        pantalla.blit(imagen_fin, (0, 0))
        fuente_fin = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 72)
        texto_fin = fuente_fin.render("¡Completaste todas las bodegas!", True, (204, 255, 0))
        rect_fin = texto_fin.get_rect(center=(400, 200))
        pantalla.blit(texto_fin, rect_fin)


        rango = obtener_rango(indice_nivel, ganador=True)
        fuente_rango = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 60)
        texto_rango = fuente_rango.render(f"RANGO: {rango}", True, (255, 255, 255))
        rect_rango = texto_rango.get_rect(midtop=(rect_fin.centerx, rect_fin.bottom + 10))
        pantalla.blit(texto_rango, rect_rango)
        boton_reinicio = pygame.Rect(300, 400, 200, 80)
        pygame.draw.rect(pantalla, (200, 50, 50), boton_reinicio)
        texto_reiniciar = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 36).render("Reiniciar Juego", True, (255, 255, 255))
        pantalla.blit(texto_reiniciar, texto_reiniciar.get_rect(center=boton_reinicio.center))

    elif estado == "game_over":
        tiempo_estado = pygame.time.get_ticks()
        sonido_rango_reproducido = False
        reproducir_musica("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\musica\\Game Over.mp3", bucle=False)
        pantalla.blit(imagen_gameover, (0, 0))
        fuente_go = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 72)
        texto_go = fuente_go.render("¡Se acabó el tiempo!", True, (255, 0, 0))
        rect_go = texto_go.get_rect(center=(400, 200))
        pantalla.blit(texto_go, rect_go)


        rango = obtener_rango(indice_nivel, ganador=False)
        fuente_rango = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 60)
        texto_rango = fuente_rango.render(f"RANGO: {rango}", True, (255, 165, 0))
        rect_rango = texto_rango.get_rect(midtop=(rect_go.centerx, rect_go.bottom + 10))
        pantalla.blit(texto_rango, rect_rango)
        boton_gameover = pygame.Rect(250, 400, 300, 80)
        pygame.draw.rect(pantalla, (100, 100, 200), boton_gameover)
        texto_retry = pygame.font.Font("C:\\Users\\andyo\\OneDrive\\Escritorio\\pruebaxd\\assets\\fonts\\m5x7.ttf", 36).render("Intentar de nuevo", True, (255, 255, 255))
        pantalla.blit(texto_retry, texto_retry.get_rect(center=boton_gameover.center))
    pygame.display.flip()
pygame.quit()