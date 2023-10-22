# pacote para criacao de automacoes

Para importar: from criar_automacoes import Automatization, pyautogui, sg,hread, kb


Estrutura básica de uma automação:

from criar_automacoes import *

p = Automatization()

# Esta parte é usada apenas no momento da criação
# novo = p.Criar_ponto()
# campopesquisar = p.Criar_ponto()
# pesquisar = p.Criar_ponto()
# juiz = p.Criar_ponto()
# nomejuiz = p.Criar_ponto()
# banco = p.Criar_ponto()
# nomebanco = p.Criar_ponto()
# proximo = p.Criar_ponto()
# novaordem = p.Criar_ponto()


# p.SalvarPontos('pontos_alvara')
def Main():
    p.CareegarPontos('pontos_alvara')
    novo = p.Coordenada('novo')
    campopesquisar = p.Coordenada('campopesquisar')
    pesquisar = p.Coordenada('pesquisar')
    juiz = p.Coordenada('juiz')
    nomejuiz = p.Coordenada('nomejuiz')
    banco = p.Coordenada('banco')
    nomebanco = p.Coordenada('nomebanco')
    proximo = p.Coordenada('proximo')
    novaordem = p.Coordenada('novaordem')

    pyautogui.sleep(2)
    t = 1
    pyautogui.click(novo, duration=t)
    pyautogui.click(campopesquisar, duration=t+2)
    pyautogui.sleep(0.5)
    # pyperclip.copy('202271101648')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.sleep(1)
    # pyautogui.hotkey('enter', 'v')

    pyautogui.click(pesquisar, duration=t)
    pyautogui.click(juiz, duration=t+5)
    pyautogui.click(nomejuiz, duration=t)
    pyautogui.click(banco, duration=t)
    pyautogui.click(nomebanco, duration=t)
    pyautogui.click(proximo, duration=t)
    pyautogui.click(novaordem, duration=t+2)


def Configurar():
    p.CareegarPontos('pontos_alvara')
    p.Configurar()


if __name__ == '__main__':
    print(
        f'''
        shift+space: roda a automação
        "config": configura os pontos da tela
    '''
    )
    kb.add_word_listener('config', Configurar)
    kb.add_hotkey('shift+space', Main)
    kb.wait()
