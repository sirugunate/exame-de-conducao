import flet as ft
import json
import os
import random
import time

# --- FUNÇÕES DE LEITURA E ESCRITA ---
pasta_do_script = os.path.dirname(os.path.abspath(__file__))

def carregar_perguntas():
    caminho_completo = os.path.join(pasta_do_script, 'perguntas.json')
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler JSON: {e}")
        return []

def carregar_historico():
    caminho = os.path.join(pasta_do_script, 'historico_app.txt')
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.readlines()
    return []

def guardar_historico(linha):
    caminho = os.path.join(pasta_do_script, 'historico_app.txt')
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(linha + "\n")
# ------------------------------------

def main(page: ft.Page):
    page.title = "Código da Estrada MZ"
    page.window_width = 400 
    page.window_height = 700
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    
    dados = carregar_perguntas()
    
    estado_exame = {
        "perguntas_atuais": [],
        "indice": 0,
        "pontuacao": 0,
        "tipo_exame": "Exame Completo"
    }

    def ver_progresso(e):
        page.clean()
        historico = carregar_historico()
        
        page.add(ft.Text("MEU PROGRESSO", size=24, weight="bold", color="blue"))
        page.add(ft.Divider(height=20, color="transparent"))
        
        if len(historico) == 0:
            page.add(ft.Text("Ainda não realizou nenhum exame."))
        else:
            for registo in historico:
                page.add(ft.Text(registo.strip(), size=14))
                
        page.add(ft.Divider(height=40, color="transparent"))
        page.add(ft.ElevatedButton("Voltar ao Menu", on_click=desenhar_menu, icon="arrow_back"))
        page.update()

    def finalizar_exame(e=None):
        page.clean()
        total = len(estado_exame["perguntas_atuais"])
        pontos = estado_exame["pontuacao"]
        percentagem = (pontos / total) * 100 if total > 0 else 0
        tipo = estado_exame["tipo_exame"]
        
        page.add(ft.Text("EXAME TERMINADO!", size=24, weight="bold", color="blue"))
        page.add(ft.Text(tipo, size=16, color="grey", weight="bold"))
        page.add(ft.Text(f"Acertou {pontos} de {total} perguntas."))
        page.add(ft.Text(f"Nota Final: {percentagem:.1f}%", size=20))
        
        if percentagem >= 75:
            page.add(ft.Text("🎉 APROVADO!", color="green", size=22, weight="bold"))
        else:
            page.add(ft.Text("📚 REPROVADO. Estude mais.", color="red", size=22, weight="bold"))
            
        data_atual = time.strftime("%Y-%m-%d %H:%M")
        novo_registo = f"[{data_atual}] {tipo} | Res: {pontos}/{total} ({percentagem:.0f}%)"
        guardar_historico(novo_registo)
        
        page.add(ft.Divider(height=30, color="transparent"))
        page.add(ft.ElevatedButton("Voltar ao Menu Principal", on_click=desenhar_menu, icon="home"))
        page.update()

    def verificar_resposta(resposta_escolhida, resposta_correta, artigo):
        page.clean()
        letra_escolhida = resposta_escolhida[0].upper()
        
        if letra_escolhida == resposta_correta:
            estado_exame["pontuacao"] += 1
            page.add(ft.Icon("check_circle", color="green", size=60))
            page.add(ft.Text("RESPOSTA CORRETA!", color="green", size=20, weight="bold"))
            page.add(ft.Text(f"Justificação legal: {artigo}", text_align="center"))
        else:
            page.add(ft.Icon("cancel", color="red", size=60))
            page.add(ft.Text("RESPOSTA ERRADA!", color="red", size=20, weight="bold"))
            page.add(ft.Text(f"A resposta certa era a alínea: {resposta_correta}"))
            page.add(ft.Text(f"Justificação legal: {artigo}", text_align="center"))
            
        estado_exame["indice"] += 1
        page.add(ft.Divider(height=30, color="transparent"))
        
        if estado_exame["indice"] < len(estado_exame["perguntas_atuais"]):
            page.add(ft.ElevatedButton("Próxima Pergunta", on_click=mostrar_pergunta, icon="arrow_forward"))
        else:
            page.add(ft.ElevatedButton("Ver Resultado Final", on_click=finalizar_exame, icon="assessment"))
            
        page.update()

    def mostrar_pergunta(e=None):
        page.clean()
        indice = estado_exame["indice"]
        pergunta_atual = estado_exame["perguntas_atuais"][indice]
        total = len(estado_exame["perguntas_atuais"])
        
        page.add(ft.Text(f"Pergunta {indice + 1} de {total}", size=14, color="grey"))
        page.add(ft.Text(pergunta_atual['pergunta'], size=18, weight="bold", text_align="center"))
        
        # CORREÇÃO AQUI: fit="contain" em vez de ft.ImageFit.CONTAIN
        if pergunta_atual.get("imagem"):
            imagem_sinal = ft.Image(
                src=pergunta_atual['imagem'], 
                width=150, 
                height=150, 
                fit="contain"
            )
            page.add(imagem_sinal)
            
        page.add(ft.Divider(height=20, color="transparent"))
        
        for opcao in pergunta_atual['opcoes']:
            botao = ft.ElevatedButton(
                opcao,
                width=320,
                height=60,
                on_click=lambda e, opt=opcao: verificar_resposta(opt, pergunta_atual['resposta_correta'], pergunta_atual.get('artigo', ''))
            )
            page.add(botao)
            page.add(ft.Divider(height=10, color="transparent"))
            
        page.update()

    def iniciar_exame(categoria):
        sorteio = dados.copy()
        
        if categoria:
            sorteio = [p for p in sorteio if p.get("categoria") == categoria]
            estado_exame["tipo_exame"] = f"Módulo: {categoria}"
        else:
            estado_exame["tipo_exame"] = "Exame Completo"
            
        if not sorteio:
            page.clean()
            page.add(ft.Text("Sem perguntas para este módulo!", color="red"))
            page.add(ft.ElevatedButton("Voltar", on_click=menu_categorias))
            page.update()
            return
            
        random.shuffle(sorteio)
        estado_exame["perguntas_atuais"] = sorteio[:21]
        estado_exame["indice"] = 0
        estado_exame["pontuacao"] = 0
        
        mostrar_pergunta()

    def menu_categorias(e):
        page.clean()
        page.add(ft.Text("ESCOLHA O MÓDULO", size=24, weight="bold", color="blue"))
        page.add(ft.Divider(height=20, color="transparent"))
        
        page.add(ft.ElevatedButton("Exame Completo (Todas as Matérias)", width=320, height=50, on_click=lambda e: iniciar_exame(None)))
        page.add(ft.Divider(height=10, color="transparent"))
        
        categorias_existentes = []
        for p in dados:
            cat = p.get("categoria")
            if cat and cat not in categorias_existentes:
                categorias_existentes.append(cat)
                
        for cat in categorias_existentes:
            page.add(ft.ElevatedButton(f"Módulo: {cat}", width=320, height=50, on_click=lambda e, c=cat: iniciar_exame(c)))
            page.add(ft.Divider(height=10, color="transparent"))
            
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(ft.ElevatedButton("Voltar ao Menu", on_click=desenhar_menu, icon="arrow_back"))
        page.update()

    def desenhar_menu(e=None):
        page.clean() 
        icone_app = ft.Icon("directions_car", size=100, color="blue")
        titulo = ft.Text("ESCOLA DE CONDUÇÃO", size=24, weight="bold", color="blue")
        subtitulo = ft.Text("Treino para Exame Teórico")
        
        botao_iniciar = ft.ElevatedButton("INICIAR EXAME", icon="play_arrow", on_click=menu_categorias, width=250, height=50)
        botao_progresso = ft.OutlinedButton("MEU PROGRESSO", icon="bar_chart", on_click=ver_progresso, width=250, height=50)
        
        page.add(icone_app, titulo, subtitulo, ft.Divider(height=40, color="transparent"), botao_iniciar, ft.Divider(height=10, color="transparent"), botao_progresso)
        page.update()

    desenhar_menu()

ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir=pasta_do_script)