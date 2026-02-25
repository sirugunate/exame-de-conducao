import time
import json
import random
import os

def carregar_perguntas():
    """Tenta carregar as perguntas do ficheiro JSON."""
    nome_ficheiro = 'perguntas.json'
    
    if not os.path.exists(nome_ficheiro):
        print(f"ERRO: Não encontrei o ficheiro '{nome_ficheiro}'!")
        print("Crie o ficheiro JSON na mesma pasta deste script.")
        return []
    
    try:
        with open(nome_ficheiro, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler o ficheiro: {e}")
        return []
    
# NOVO: Adicionámos o parâmetro 'tipo_exame'
def guardar_resultado(nome_aluno, pontuacao, total_perguntas, percentagem, tipo_exame):
    """Guarda o resultado do aluno num ficheiro de texto, com a categoria do exame."""
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    caminho_registo = os.path.join(pasta_do_script, 'registos_escola.txt')
    
    with open(caminho_registo, 'a', encoding='utf-8') as f:
        data_hora = time.strftime("%Y-%m-%d %H:%M")
        
        # NOVO: O ficheiro agora escreve o tipo de exame logo a seguir à data
        f.write(f"[{data_hora}] {tipo_exame} | Instruendo: {nome_aluno} | Resultado: {pontuacao}/{total_perguntas} ({percentagem:.1f}%)\n")

def ver_registos():
    """Lê o ficheiro de texto e mostra as notas dos alunos."""
    os.system('clear')
    print("🗂️ --- ARQUIVO DE NOTAS DA ESCOLA --- 🗂️\n")
    
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    caminho_registo = os.path.join(pasta_do_script, 'registos_escola.txt')
    
    # Verifica se o ficheiro já existe (pode não existir se ninguém fez exame ainda)
    if os.path.exists(caminho_registo):
        with open(caminho_registo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            print(conteudo)
    else:
        print("Ainda não existem exames registados no sistema.")
        
    input("\n[Pressione ENTER para voltar ao Menu Principal]")

# NOVO: Agora a função aceita um parâmetro chamado 'categoria_filtro'
def iniciar_exame(categoria_filtro=None):
    os.system('clear') 
    
    print("🚗 --- ESCOLA DE CONDUÇÃO 2.0 --- 🚗")
    
    nome = input("Por favor, insira o nome do instruendo: ").strip()
    if not nome:
        nome = "Aluno Anónimo"

    print("\nA carregar base de dados...")
    time.sleep(0.5)
    
    dados = carregar_perguntas()
    
    if not dados:
        return 

    # --- BLOCO NOVO: A LÓGICA DE FILTRAGEM ---
    # Se o professor escolheu uma categoria específica no Menu...
    if categoria_filtro is not None:
        dados_filtrados = []
        for pergunta in dados:
            # O .get() procura a etiqueta 'categoria' de forma segura
            if pergunta.get('categoria') == categoria_filtro:
                dados_filtrados.append(pergunta)
        
        dados = dados_filtrados # Substituímos todas as perguntas apenas pelas filtradas
        print(f"\n📚 MÓDULO DE ESTUDO: {categoria_filtro.upper()}")
    # ------------------------------------------

    # Se a categoria escolhida não tiver perguntas, o programa avisa
    if len(dados) == 0:
        print("Ainda não existem perguntas registadas para esta categoria.")
        input("\n[Pressione ENTER para voltar ao Menu]")
        return

    random.shuffle(dados)
    
    pontuacao = 0
    total_perguntas = len(dados)
    opcoes_validas = ['A', 'B', 'C']

    for i, item in enumerate(dados, 1):
        print(f"\nQUESTÃO {i}/{total_perguntas}: {item['pergunta']}")
        
        for opcao in item['opcoes']:
            print(f"   {opcao}")
        
        while True:
            resposta = input("\nSua resposta (A/B/C): ").strip().upper()
            if resposta in opcoes_validas:
                break
            else:
                print(f"⚠️ Erro: '{resposta}' não é uma opção válida. Tente A, B ou C.")
        
        if resposta == item['resposta_correta']:
            print("✅ CORRETO!")
            pontuacao += 1
        else:
            print(f"❌ ERRADO! A resposta certa era {item['resposta_correta']}.")
            print(f"📖 Lei: {item['artigo']}")
        
        input("[Pressione ENTER para continuar...]")
        os.system('clear') 

    print(f"\n=== RESULTADO FINAL DE {nome.upper()} ===")
    print(f"Acertou {pontuacao} de {total_perguntas} perguntas.")
    percentagem = (pontuacao / total_perguntas) * 100
    print(f"Nota: {percentagem:.1f}%")

    if percentagem >= 75:
        print("🎉 APROVADO! Pode ir marcar o exame real.")
    else:
        print("📚 REPROVADO. Estude mais o Decreto-Lei 1/2011.")

    # ... (código existente acima) ...
    
    # --- BLOCO NOVO: DEFINIR O TIPO DE EXAME PARA O REGISTO ---
    if categoria_filtro is None:
        tipo_exame = "Exame Completo"
    else:
        tipo_exame = f"Módulo: {categoria_filtro}"
    # ----------------------------------------------------------

    # --- LÓGICA DE FILTRAGEM (Já existia) ---
    if categoria_filtro is not None:
        dados_filtrados = []
# ... (resto do código do exame) ...

def menu_principal():
    while True:
        os.system('clear')
        print("🏛️ --- SISTEMA DE GESTÃO: CÓDIGO DA ESTRADA --- 🏛️")
        print("1. Exame Completo (Todas as Matérias)")
        print("2. Exame Temático (Por Módulo)")
        print("3. Consultar Notas de Alunos")
        print("4. Fechar Sistema")
        
        escolha = input("\nEscolha uma opção (1/2/3/4): ").strip()
        
        if escolha == '1':
            iniciar_exame() # Não enviamos nada, logo faz o exame todo
        
        elif escolha == '2': # NOVO: Sub-menu de categorias
            os.system('clear')
            print("Escolha o Módulo de Estudo:")
            print("A) Regras de Trânsito")
            print("B) Contra-ordenações e Multas")
            tema = input("\nOpção (A/B): ").strip().upper()
            
            if tema == 'A':
                iniciar_exame(categoria_filtro="Regras de Trânsito")
            elif tema == 'B':
                iniciar_exame(categoria_filtro="Contra-ordenações e Multas")
            else:
                print("❌ Módulo inexistente.")
                time.sleep(1.5)
                
        elif escolha == '3':
            ver_registos()
            
        elif escolha == '4':
            os.system('clear')
            print("A encerrar o sistema. Até logo!")
            break
            
        else:
            print("❌ Opção inválida. Escolha de 1 a 4.")
            time.sleep(1.5)

if __name__ == "__main__":
    menu_principal()