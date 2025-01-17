import os
import time
import math
from deep_translator import GoogleTranslator
import streamlit as st


# Classe Tradutor
class Tradutor:
    def __init__(self, source_lang='auto', target_lang='pt'):
        self.tradutor = GoogleTranslator(source=source_lang, target=target_lang)
        self.lim_car = 4900  # Limite de caracteres por fatia

    def traduzir_texto(self, texto, barra_progresso=None, status=None):
        tamanho_texto = len(texto)
        fatias = math.ceil(tamanho_texto / self.lim_car)
        texto_fatiado = [texto[i * self.lim_car:((i + 1) * self.lim_car)] for i in range(fatias)]

        output = ""
        tempo_inicial = time.time()

        for cont, parte_texto in enumerate(texto_fatiado):
            output += self.tradutor.translate(parte_texto.strip()) + " "

            # Atualizar barra de progresso e status, se disponíveis
            if barra_progresso and status:
                progresso_atual = (cont + 1) / fatias
                barra_progresso.progress(progresso_atual)
                caracteres_traduzidos = (cont + 1) * self.lim_car
                status.text(f"Tradução em andamento... {progresso_atual:.2%} concluído. "
                            f"Caracteres traduzidos: {caracteres_traduzidos}, "
                            f"Tempo decorrido: {time.time() - tempo_inicial:.2f} segundos.")

        return output

    def traduzir_arquivo(self, arquivo_entrada, arquivo_saida, barra_progresso, status):
        with open(arquivo_entrada, 'r', encoding='utf-8') as file:
            texto = file.read()

        texto_traduzido = self.traduzir_texto(texto, barra_progresso, status)

        with open(arquivo_saida, 'w', encoding='utf-8') as file:
            file.write(texto_traduzido)


# Classe InterfaceGrafica
class InterfaceGrafica:
    def __init__(self):
        self.tradutor = Tradutor()

    def executar(self):
        st.title("Super Tradutor")

        st.write("Bem-vindo ao Super Tradutor! Escolha uma das opções abaixo para traduzir um arquivo ou um texto.")

        opcao = st.selectbox("Escolha o modo de tradução", ["Traduzir Arquivo", "Traduzir Texto"])

        if opcao == "Traduzir Arquivo":
            arquivo_entrada = st.file_uploader("Carregar arquivo de texto", type=["txt", "srt"])
            idioma_origem = st.selectbox("Idioma de Origem", options=['auto', 'en', 'fr', 'es', 'de'])
            idioma_destino = st.selectbox("Idioma de Destino", options=['pt', 'en', 'fr', 'es', 'de'])

            if st.button("Traduzir"):
                if arquivo_entrada is not None:
                    # Criar diretório de uploads se não existir
                    if not os.path.exists("uploads"):
                        os.makedirs("uploads")

                    caminho_entrada = os.path.join("uploads", arquivo_entrada.name)
                    caminho_saida = f"tradução_{arquivo_entrada.name}"

                    with open(caminho_entrada, 'wb') as f:
                        f.write(arquivo_entrada.getbuffer())

                    self.tradutor = Tradutor(source_lang=idioma_origem, target_lang=idioma_destino)

                    # Barra de progresso e status de tradução
                    barra_progresso = st.progress(0)
                    status = st.empty()

                    self.tradutor.traduzir_arquivo(caminho_entrada, caminho_saida, barra_progresso, status)

                    with open(caminho_saida, 'r', encoding='utf-8') as file:
                        texto_traduzido = file.read()

                    st.write("Tradução concluída! Veja abaixo:")
                    st.text_area("Texto Traduzido", texto_traduzido, height=300)

                    st.download_button(label="Baixar Tradução", data=texto_traduzido, file_name=caminho_saida,
                                       mime="text/plain")

        elif opcao == "Traduzir Texto":
            texto_entrada = st.text_area("Digite o texto a ser traduzido")
            idioma_origem = st.selectbox("Idioma de Origem", options=['auto', 'en', 'fr', 'es', 'de'],
                                         key="texto_origem")
            idioma_destino = st.selectbox("Idioma de Destino", options=['pt', 'en', 'fr', 'es', 'de'],
                                          key="texto_destino")

            if st.button("Traduzir", key="botao_traduzir_texto"):
                self.tradutor = Tradutor(source_lang=idioma_origem, target_lang=idioma_destino)

                # Barra de progresso e status de tradução
                barra_progresso = st.progress(0)
                status = st.empty()

                texto_traduzido = self.tradutor.traduzir_texto(texto_entrada, barra_progresso, status)

                st.write("Tradução concluída! Veja abaixo:")
                st.text_area("Texto Traduzido", texto_traduzido, height=300)

                st.download_button(label="Baixar Tradução", data=texto_traduzido, file_name="tradução.txt",
                                   mime="text/plain")


# Execução da Interface Gráfica
if __name__ == "__main__":
    InterfaceGrafica().executar()
