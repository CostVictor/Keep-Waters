from Script.loading import *

class KeepWaters:
    def __init__(self) -> None:
        self.init = True

        # ~~ Inicialização Pygame
        pygame.init()
        self.display = display
        self.rect = self.display.get_rect()
        self.time = pygame.time.Clock()
        self.clock = Clock()

        # ~~ Inputs
        self.mouse = Mouse(mouse, self.clock)
        self.keyboard = Keyboard()

        # ~~ Gerenciadores
        self.allgroupsPanel = PriorityArray()
        self.allGroupsMap = PriorityArray()
        self.allgroupPause = PriorityArray()
        self.allTextMap = TextManager(proporcoes)
        self.textPause = TextManager(proporcoes)
        self.allMessages = MessageManager(sprites_mensagem, self.allTextMap)
        self.allBoxInfo = BoxInfo(sprites_box, self.mouse, proporcoes)

        # ~~ Classes principais
        self.reprodutor = ReprodutorVideo(icon_video, self.mouse, Clock(), PriorityArray())
        self.blur = Blur(self.display)
        
        # ~~ Menu principal
        self.group_panel_tutorial = self.allgroupsPanel.createGroupSingle(priority=0)
        self.panel_tutorial = Panel(proporcoes, sprite_creditos[0], sprites_botao_panel, self.mouse, self.allgroupsPanel, self.display, self.group_panel_tutorial)
        self.group_panel_conquistas = self.allgroupsPanel.createGroupSingle(priority=0)
        self.panel_conquistas = PanelUpdate(proporcoes, sprite_creditos[0], sprites_botao_panel, self.mouse, self.allgroupsPanel, self.display, self.group_panel_conquistas)
        self.group_panel_ajuda = self.allgroupsPanel.createGroupSingle(priority=0)
        self.panel_ajuda = Panel(proporcoes, sprite_creditos[0], sprites_botao_panel, self.mouse, self.allgroupsPanel, self.display, self.group_panel_ajuda)
        self.menu_inicial = PrincipalInterface(interface, 64, PriorityArray(), proporcoes, self.group_panel_tutorial, self.group_panel_conquistas)
        
        # ~~ Jogo
        posFPS = (int(self.rect.right - 40 * proporcoes.x), int(self.rect.top + 20 * proporcoes.y))
        self.fps = self.allTextMap.createText(str(int(self.time.get_fps())), 20, posFPS, (0, 0, 0))
        self.player = self.allGroupsMap.createGroupSingle(priority=2)
        self.mapa = self.allGroupsMap.createGroupSingle(priority=0)
        self.pdp = Pdp(sprites_pdp, self.clock, self.allTextMap, proporcoes)
        self.structures = Structures(sprites_struturas, self.mapa, self.allGroupsMap, proporcoes)

        # ~~ Pause
        self.groupPause = self.allgroupPause.createGroupSingle(priority=0)
        self.pause = Pause(sprites_pause, self.rect.center, self.allgroupPause, self.clock, 'abrir', self.groupPause)

        # ~~ Game Over

    # ~~~~~~~~~ Remover ~~~~~~~~
        self.iniciar_teste = False
        self.timer_desafio = self.clock.createTimer(manage=True)
        self.timer_desafio.countdown(time=10.0, format=60)
        self.timer_desafio.pause = True

        self.timer_contador = self.clock.createTimer(manage=True)
        self.time_surgimento = 4.0
        self.timer_teste_pause = True

        self.trocar_musica = True
    
    def reset(self):
        pygame.mixer.music.load(musica_menu_inicial)
        pygame.mixer.music.play(loops=-1)
        self.trocar_musica = True

        self.allTextMap = TextManager(proporcoes)
        posFPS = (int(self.rect.right - 40 * proporcoes.x), int(self.rect.top + 20 * proporcoes.y))
        self.fps = self.allTextMap.createText(str(int(self.time.get_fps())), 20, posFPS, (0, 0, 0))
        self.allGroupsMap.remove(self.objPlayer.particulas.particulas)
        self.player.add(Player(sprites_player, proporcoes, self.rect.center, self.allGroupsMap, self.allMessages, 'parado'))
        self.objPlayer = self.player.sprite
        self.objPlayer.loading(sprites_life, self.mouse, self.clock)
        self.objPlayer.loadingInventory(sprites_inventory, sprites_hub)
        self.objMapa.ref = self.objPlayer
        self.allBoxInfo = BoxInfo(sprites_box, self.mouse, proporcoes)
        self.allBoxInfo.createBoxSolid((self.rect.left+5, self.rect.top+5), reference='topleft')

        self.pdp = Pdp(sprites_pdp, self.clock, self.allTextMap, proporcoes)
        self.residuoMap.residuosMap.remove(self.residuoMap.residuosMap)
        self.iniciar_teste = False

        self.timer_desafio.restart()
        self.timer_desafio.pause = True
        self.timer_contador.restart()
        self.timer_contador.pause = True
    
    def criar_caixa(self):
        if not self.allBoxInfo.boxAnimation:
            texto = self.allTextMap.createText('!', 17, (-30, -30))
            iconeTeste = Icon(texto.image, texto.pos)
            self.allBoxInfo.createBoxAnimation(iconeTeste, self.timer_desafio, audio=False)
    
    @staticmethod
    def sortear_pos():
        posX = random.randint(850, 1900)
        posY = random.randint(2250, 3130)
        return pygame.Vector2(posX, posY)
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    def loading(self):
        self.panel_tutorial.load_imgs(sprite_creditos)
        self.group_panel_tutorial.exibir = False

        self.panel_conquistas.load_imgs(sprites_conquistas)
        self.group_panel_conquistas.exibir = False

        self.panel_ajuda.load_imgs(sprites_ajuda)
        self.group_panel_ajuda.exibir = False

        self.menu_inicial.loading(list_bottom_keys)
        self.allBoxInfo.createBoxSolid((self.rect.left+5, self.rect.top+5), reference='topleft')
        self.lixeiras = Lixeiras(self.mapa, sprites_lixeira, self.allGroupsMap, proporcoes)
        self.player.add(Player(sprites_player, proporcoes, self.rect.center, self.allGroupsMap, self.allMessages, 'parado'))
        self.mapa.add(Map(self.player.sprite, self.display, proporcoes))
        self.mapa.sprite.loading()
        self.residuoMap = ResiduoInMap(sprites_residuo, self.mapa.sprite, self.allGroupsMap, proporcoes)
        self.lixeiras.loading()

        self.structures.createStructure(None, 'estrutura upgrade')

        self.objPlayer = self.player.sprite
        self.objMapa = self.mapa.sprite

        self.objPlayer.loading(sprites_life, self.mouse, self.clock)
        self.objPlayer.loadingInventory(sprites_inventory, sprites_hub)

        self.pause.loading(proporcoes, self.display, self.blur, self.textPause)
        self.pause.loadingButton(sprites_botao)

        pygame.mixer.music.load(musica_menu_inicial)
        pygame.mixer.music.play(loops=-1)

    def events(self):
        self.keyboard.evento = None
        self.keyboard.resizable = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.init = False
            if event.type == pygame.KEYDOWN:
                self.keyboard.evento = event.key
                if self.keyboard.event(pygame.K_F11):
                    if config['resolucao_tela'] != (largura, altura) and proporcoes.y >= 1:
                        pygame.display.toggle_fullscreen()

    def run(self):
        while self.init:
            # ~~ FPS
            self.time.tick(config['limite_fps'])
            self.fps.set_text(str(int(self.time.get_fps())))

            # ~~ Mouse
            self.mouse.update()
            self.mouse.click()
            self.mouse.image.set_posMap(self.objMapa.get_posMap(self.mouse.image.rect))

            # ~~ Eventos
            self.events()

            # ~~~~~~~~ Área de Testes na repetição ~~~~~~~~ #
            self.timer_contador.countdown(time=self.time_surgimento)
            self.timer_desafio.countdown(self.timer_desafio.register)

            if self.iniciar_teste:
                if not self.timer_desafio.finished:
                    if self.timer_contador.finished:
                        self.residuoMap.createResiduoAreia(self.sortear_pos())
                        self.timer_contador.restart()
                        if 360 < int(self.timer_desafio.get_score(format_min_sec=False)) < 480 and self.timer_desafio != 2:
                            self.time_surgimento = 3.5
                            self.objPlayer.speed = 6 * proporcoes.x
                        elif 240 < int(self.timer_desafio.get_score(format_min_sec=False)) < 360 and self.timer_desafio != 1.5:
                            self.time_surgimento = 3.0
                            self.objPlayer.speed = 8 * proporcoes.x
                        elif 120 < int(self.timer_desafio.get_score(format_min_sec=False)) < 240 and self.timer_desafio != 1:
                            self.time_surgimento = 2.5
                            self.objPlayer.speed = 10 * proporcoes.x
                else:
                    if self.residuoMap.residuosMap:
                        self.residuoMap.residuosMap.remove(self.residuoMap.residuosMap)
                        for indice, slot in enumerate(self.objPlayer.objBag.slots):
                            self.objPlayer.objBag.storage[indice] = 0
                            slot.item.remove(slot.item)
                            slot.reset()
            else:
                if not self.residuoMap.residuosMap:
                    self.residuoMap.createResiduoAreia(self.sortear_pos())
                if self.objPlayer.objBag.slots.sprites()[0].item:
                    self.iniciar_teste = True
                    self.timer_desafio.pause = False
                    self.timer_contador.pause = False
                    self.timer_teste_pause = False
                    self.criar_caixa()

            # if self.mouse.botaoL and self.keyboard.key(pygame.K_LSHIFT):
            #     self.residuoMap.createResiduoAreia(self.mouse.image.posMap)

            # self.timerTest.countdown(10, format=60)
            # if self.keyboard.event(pygame.K_t):
            #     iconeTeste = Icon(loadImage(icone_apagar, proporcoes, 'list')[0], (-20, -20))
            #     self.allBoxInfo.createBoxAnimation(iconeTeste, self.timerTest, audio=False)
            
            # if self.keyboard.event(pygame.K_g):
            #     self.objPlayer.life.cure(100)

            # if self.keyboard.event(pygame.K_p):
            #     self.objPlayer.life.damage(25)

            # if self.keyboard.event(pygame.K_t):
            #     self.blur.apply(pygame.display.get_surface().copy(), desfoque=2)
            
            # if self.keyboard.event(pygame.K_r):
            #     self.blur.remove()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            # ~~ Logo

            # ~~ Delta
            self.delta = self.clock.delta()
            
            # ~~ Menu inicial
            botao = self.mouse.collideId(self.menu_inicial.buttons)
            inputs = self.menu_inicial.inputs(botao)
            self.init = inputs if inputs is not None else self.init
            self.menu_inicial.run(self.mouse, self.delta)

            # ~~ Jogo
            if not self.menu_inicial.init:
                if self.trocar_musica:
                    pygame.mixer.music.load(musica_jogo)
                    pygame.mixer.music.play(loops=-1)
                    self.trocar_musica = False

                # ~~ Ativação do Pause
                if not self.objPlayer.objBag.open:
                    if self.keyboard.event(pygame.K_ESCAPE):
                        if not self.pause.animation: self.pause.pausar()

                if not self.pause.paused and not self.blur.active:

                    # ~~ Descarte
                    perimetroDescarte = self.lixeiras.descarte()
                    if perimetroDescarte:
                        if self.objPlayer.objBag.open and self.mouse.botaoL:
                            self.objPlayer.objBag.descartar(perimetroDescarte, self.pdp)
                        else: self.objPlayer.hub.descartar(perimetroDescarte, self.objPlayer, self.pdp, self.keyboard)

                    # ~~ Atualizações
                    self.allGroupsMap.draw(self.display)

                    self.mapa.update()
                    self.structures.update(self.keyboard)
                    self.lixeiras.update(self.delta)
                    self.allBoxInfo.update(self.display, self.delta)
                    self.player.update(mapa=self.mapa.sprite, keyboard=self.keyboard, delta=self.delta)
                    self.residuoMap.update(self.keyboard, self.delta)
                    self.pdp.update(self.objMapa, self.delta)
                    self.allMessages.update(self.delta, self.display, proporcoes)

            self.allTextMap.blit(self.display)
            self.blur.update(self.delta)

            # ~~ Execução do Pause
            if self.pause.paused:
                self.clock.config_all_timers('pausar')
                self.allMessages.clock.config_all_timers('pausar')

                self.allgroupPause.draw(self.display)
                self.pause.update(self.delta)
                self.textPause.blit(self.display)
                if not self.panel_ajuda.exibindo and not self.panel_conquistas.exibindo:
                    match self.pause.updateButton(self.delta, self.mouse):
                        case ('Continuar', True): self.pause.pausar()
                        case ('Ajuda', True): self.panel_ajuda.exibir(self.group_panel_ajuda)
                        case ('Conquistas', True): self.panel_conquistas.exibir(self.group_panel_conquistas)
                        case ('Voltar ao menu', True): self.reset(); self.pause.pausar(); self.menu_inicial.init = True; self.timer_teste_pause = True
                        case ('Sair do jogo', True): self.init = False
            elif self.clock.pause:
                self.clock.config_all_timers('despausar')
                self.allMessages.clock.config_all_timers('despausar')
                if self.timer_teste_pause:
                    self.timer_desafio.pause = True
                    self.timer_contador.pause = True

            self.allgroupsPanel.draw(self.display)
            self.panel_tutorial.update(self.delta, self.group_panel_tutorial)
            self.panel_conquistas.update(self.delta, self.group_panel_conquistas)
            self.panel_ajuda.update(self.delta, self.group_panel_ajuda)
            pygame.display.update()

keep_waters = KeepWaters()
keep_waters.loading()
keep_waters.run()
