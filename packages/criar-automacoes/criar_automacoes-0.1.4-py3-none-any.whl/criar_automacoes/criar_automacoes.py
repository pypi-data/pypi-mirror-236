import pyautogui
import PySimpleGUI as sg
import json
import pyperclip
import keyboard as kb
import threading as Thread


class Automatization:
    def __init__(self):
        self.nomejson = f'Você ainda não carregou os pontos (self.CareegarPontos)'

        self.dic = {}

    def ObterPosicao(self):
        return pyautogui.position()

    def Criar_ponto(self):
        pyautogui.sleep(1)
        while (s := sg.popup(f'leve o mouse até local e pressione "enter". \nPara abortar a operação pressione "space', no_titlebar=True, grab_anywhere = True,keep_on_top=True, any_key_closes=True)) not in [' ', '\r']:
            pass
        if s == ' ':
            pass
        else:
            valor = self.ObterPosicao()
            nome_do_ponto = sg.popup_get_text(
                f'Digite um nome para este ponto e pressione "enter". \nPara abortar a operação pressione "space', no_titlebar=True,  keep_on_top=True)

            if nome_do_ponto == ' ':
                return None
            else:
                self.dic[nome_do_ponto] = valor
                return valor

    def Configurar(self):
        if self.nomejson in [f'Você ainda não carregou os pontos (self.CareegarPontos)', '']:
            self.nomejson = sg.popup_get_file(f'Localize o arquivo "a.txt"', save_as=True, no_titlebar=True, file_types=(
                (".json", ".json*"),), keep_on_top=True)

        if self.nomejson not in [f'Você ainda não carregou os pontos (self.CareegarPontos)', '']:
            pyautogui.sleep(1)
            for i in self.dic.keys():
                while (s := sg.popup(f'leve o mouse até "{i}" e pressione "enter". \nPara abortar a operação pressione "space', no_titlebar=True, keep_on_top=True, grab_anywhere - True, any_key_closes=True)) not in [' ', '\r']:
                    pass

                if s == ' ':
                    break
                else:
                    self.dic[i] = self.ObterPosicao()

            if s != ' ':
                # dic['local_a.txt'] = SelecionarPasta()
                sg.popup('Configuração realizada com sucesso!', auto_close=True)
                self.Escrever_json(self.dic, self.nomejson)
                print('configurações salvas')
                # return dic
            else:
                print('operação abortada')

    def Coordenada(self, nome):
        return self.dic.get(nome, None)

    def SalvarPontos(self, nomejson):
        self.Escrever_json(self.dic, nomejson)
        if nomejson[-4:] != 'json':
            nomejson = nomejson+'.json'
        print(f'Pontos salvos em {nomejson}')

    def CareegarPontos(self, nomejson):
        self.nomejson = nomejson
        self.dic = self.Ler_json(nomejson)
        print('pontos carregados com sucesso')

    def Pontos(self):
        return self.dic

    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'w') as f2:
            json.dump(nomedodicionario, f2, indent=4)

    def Ler_json(self, nomedoarquivo):  # retorna um dicionário
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'r') as f2:
            try:
                a = json.load(f2)
                return a
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                return {}
