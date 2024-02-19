from Script.interagiveis.button import Botao
from Script.gerenciadores.text import TextManager
import pygame, numpy


class Panel(pygame.sprite.Sprite):
    def __init__(self, proporcoes, sprite_null, sprites_button, mouse, priorityArray, display, *group) -> None:
        super().__init__(*group)
        self.exibindo = False

        self.sprite_null = numpy.array([sprite_null])
        self.sprites_botao = sprites_button
        self.display = display
        self.mouse = mouse
        self.proporcoes = proporcoes

        self.allgroups = priorityArray
        self.allText = TextManager(self.proporcoes)
        self.button_close = self.allgroups.createGroupSingle(priority=1)
        self.button_close.exibir = False

        self.image = self.sprite_null[0]
        self.rect = self.image.get_rect(center=self.display.get_rect().center)

        self.pos_text_info = (self.rect.left + (55 * self.proporcoes.x), self.rect.top + (35 * self.proporcoes.y))
        self.text_info = self.allText.createText('', 20, self.pos_text_info)
        self.index_sprites = 0


    def _load_button(self):
        posX_btn_voltar = self.rect.left + (30 * self.proporcoes.x)
        posX_btn_proximo = self.rect.right - (25 * self.proporcoes.x)
        pos_close = (self.rect.right - (37 * self.proporcoes.x), self.rect.top + (37 * self.proporcoes.y))

        self.botao_voltar = self.allText.createText('<', 30, (posX_btn_voltar, self.rect.centery))
        self.botao_voltar.exibir = False
        self.botao_proximo = self.allText.createText('>', 30, (posX_btn_proximo, self.rect.centery))
        self.botao_proximo.exibir = False

        self.botao_close = Botao(self.sprites_botao, '', pos_close, 'botao_acao', 'x', self.allText, 20)
        pos_text_close = (self.botao_close.rect.centerx + 2, self.botao_close.rect.centery - 4)

        self.botao_close.set_pos_textButton(pos_text_close)
        self.button_close.add(self.botao_close)
        self.check_button()


    def load_imgs(self, sprites_exibicao):
        if sprites_exibicao.size:
            self.sprites_exibicao = sprites_exibicao
        else: self.sprites_exibicao = self.sprite_null
        self._load_button()
    

    def check_button(self):
        self.button_close.exibir = False
        if self.exibindo:
            self.button_close.exibir = True
        
    
    def exibir(self, group_panel):
        group_panel.exibir = True
        self.exibindo = True
        self.index_sprites = 0
        self.check_button()

    
    def remover(self, group_panel):
        group_panel.exibir = False
        self.exibindo = False
        self.check_button()


    def update(self, delta, group_panel):
        if self.exibindo:
            pos_mouse = pygame.mouse.get_pos()
            condict_voltar = (
                self.rect.left <= pos_mouse[0] <= self.rect.left + (60 * self.proporcoes.x) and
                self.rect.centery - (50 * self.proporcoes.y) <= pos_mouse[1] <= self.rect.centery + (50 * self.proporcoes.y)
            )
            condict_proximo = (
                self.rect.right - (60 * self.proporcoes.x) <= pos_mouse[0] <= self.rect.right and
                self.rect.centery - (50 * self.proporcoes.y) <= pos_mouse[1] <= self.rect.centery + (50 * self.proporcoes.y)
            )
            
            self.image = self.sprites_exibicao[self.index_sprites]
            
            self.button_close.update(self.display, delta, '_vermelho', self.mouse.botaoL)
            if self.botao_close.estado:
                self.remover(group_panel)
            
            if self.sprites_exibicao.size > 1:
                self.text_info.set_text(f'{self.index_sprites + 1}/{self.sprites_exibicao.size}')

                if condict_voltar:
                    self.botao_voltar.exibir = True
                    if self.mouse.botaoL and self.index_sprites > 0:
                         self.index_sprites -= 1
                else: self.botao_voltar.exibir = False
                    
                if condict_proximo:
                    self.botao_proximo.exibir = True
                    if self.mouse.botaoL and self.index_sprites < self.sprites_exibicao.size - 1:
                        self.index_sprites += 1
                else: self.botao_proximo.exibir = False

            else: self.text_info.exibir = False
            self.allText.blit(self.display)


class PanelUpdate(Panel):
    def __init__(self, proporcoes, sprite_null, sprites_button, mouse, priorityArray, display, *group) -> None:
        super().__init__(proporcoes, sprite_null, sprites_button, mouse, priorityArray, display, *group)
        self.__qnt_exibicao = 0
    
    
    @property
    def qnt(self):
        return self.__qnt_exibicao


    @qnt.setter
    def qnt(self, value):
        self.__qnt_exibicao = value


    def load_imgs(self, sprites_exibicao):
        self.sprites_total = sprites_exibicao
        self.update_exibicao()
        self._load_button()


    def update_exibicao(self):
        if self.__qnt_exibicao:
            if self.__qnt_exibicao > self.sprites_total.size:
                self.__qnt_exibicao = self.sprites_total.size

            self.sprites_exibicao = self.sprites_total[:self.__qnt_exibicao]
        else: self.sprites_exibicao = self.sprite_null
        self.check_button()


    def liberar_exibicao(self, qnt=1):
        self.__qnt_exibicao += abs(qnt)
        self.update_exibicao()
        