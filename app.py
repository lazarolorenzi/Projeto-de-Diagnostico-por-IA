import csv
from experta import *
from flask import Flask, render_template, request

# Definindo o caminho do dataset, na hora que for testar mude para o seu caminho do dataset coloque o caminho desda raiz, algumas vezes ele n encontra se colocar de forma simples !! exp CAMINHO_CSV = 'dataset_sintomas.csv'
CAMINHO_CSV = 'D:\Projeto-de-Diagnostico-por-IA\dataset_sintomas.csv'

# Carregar os fatos sobre doenças e sintomas do CSV
def carregar_fatos(caminho):
    fatos = {}
    sintomas_criticos = {}
    with open(caminho, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pular o cabeçalho
        for row in reader:
            doenca, sintomas_str, sintoma_critico = row
            sintomas = [s.strip() for s in sintomas_str.split(';')]
            fatos[doenca] = sintomas
            sintomas_criticos[doenca] = [sintoma_critico.strip()]
    return fatos, sintomas_criticos

# Inicializando o Flask app
app = Flask(__name__)

# Carregar fatos do CSV
fatos, sintomas_criticos = carregar_fatos(CAMINHO_CSV)

# Criar uma lista de sintomas para o formulário
todos_sintomas = sorted({sintoma for sintomas in fatos.values() for sintoma in sintomas})
todas_doencas = sorted(fatos.keys())
print("Doenças carregadas:", todas_doencas)  # Verificação para garantir que doenças foram carregadas

# Motor de Inferência 
class Diagnostico(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action='diagnosticar')

    def __init__(self, fatos, sintomas_criticos):
        super().__init__()
        self.fatos = fatos
        self.sintomas_criticos = sintomas_criticos

    def carregar_fatos(self):
        for doenca, sintomas in self.fatos.items():
            self.declare(Fact(doenca=doenca, sintomas=sintomas))

    @Rule(Fact(action='diagnosticar'),
          Fact(doenca=MATCH.doenca, sintomas=MATCH.sintomas),
          Fact(sintomas_usuario=MATCH.sintomas_usuario),
          TEST(lambda sintomas_usuario, sintomas: len(set(sintomas_usuario) & set(sintomas)) > 0))
    def diagnosticar_doenca(self, doenca, sintomas_usuario):
        # Calcular a quantidade de sintomas coincidentes entre os sintomas do usuário e os da doença
        sintomas_comuns = set(sintomas_usuario) & set(self.fatos[doenca])
        total_sintomas = len(self.fatos[doenca])
        total_comuns = len(sintomas_comuns)

        # Definir um peso maior para sintomas críticos
        sintomas_criticos_comuns = set(sintomas_comuns) & set(self.sintomas_criticos.get(doenca, []))
        peso_critico = 3.0  # Dar um peso maior para sintomas críticos
        pontuacao = total_comuns + (len(sintomas_criticos_comuns) * (peso_critico - 1))

        # Calcular a porcentagem final levando em consideração os pesos
        porcentagem = (pontuacao / total_sintomas) * 100 if total_sintomas > 0 else 0

        # Declara o diagnóstico com a porcentagem calculada
        self.declare(Fact(diagnostico=doenca, porcentagem=round(porcentagem, 2)))

# Rotas do Flask

@app.route('/')
def index():
    # Página inicial com opções para o usuário
    return render_template('index.html')

@app.route('/diagnostico_por_sintomas')
def diagnostico_por_sintomas():
    # Página para selecionar os sintomas
    return render_template('diagnostico_por_sintomas.html', todos_sintomas=todos_sintomas)

@app.route('/resultado_diagnostico', methods=['POST'])
def resultado_diagnostico():
    sintomas_usuario = request.form.getlist('sintomas')
    
    # Criar e rodar o motor especialista
    motor = Diagnostico(fatos, sintomas_criticos)
    motor.reset()
    motor.declare(Fact(sintomas_usuario=sintomas_usuario))
    motor.carregar_fatos()
    motor.run()
    
    # Coletar diagnósticos e calcular porcentagem de ocorrência dos sintomas
    diagnosticos = []
    for fact in motor.facts.values():
        if 'diagnostico' in fact and 'porcentagem' in fact:
            doenca = fact['diagnostico']
            porcentagem = fact['porcentagem']
            diagnosticos.append((doenca, porcentagem))
    
    # Ordenar os diagnósticos pela porcentagem de forma decrescente e pegar os 3 maiores
    diagnosticos = sorted(diagnosticos, key=lambda x: x[1], reverse=True)[:3]
    
    if not diagnosticos:
        resultado = "Nenhum diagnóstico encontrado com os sintomas fornecidos."
    else:
        resultado = [f"{doenca}: {int(porcentagem)}%" for doenca, porcentagem in diagnosticos]
    
    return render_template('resultado_diagnostico.html', sintomas_usuario=sintomas_usuario, resultado=resultado)

@app.route('/engenharia_reversa')
def engenharia_reversa():
    # Página para selecionar uma doença conhecida
    return render_template('engenharia_reversa.html', todas_doencas=todas_doencas)

@app.route('/selecionar_sintomas', methods=['POST'])
def selecionar_sintomas():
    # O usuário seleciona uma possível doença
    doenca_escolhida = request.form.get('doenca')
    # Pegar os sintomas dessa doença específica
    sintomas_da_doenca = fatos.get(doenca_escolhida, [])
    return render_template('selecionar_sintomas.html', doenca=doenca_escolhida, sintomas=sintomas_da_doenca)

@app.route('/verificar_diagnostico', methods=['POST'])
def verificar_diagnostico():
    # Receber a doença escolhida e os sintomas selecionados pelo usuário
    doenca_escolhida = request.form.get('doenca')
    sintomas_usuario = request.form.getlist('sintomas')

    # Verificar se a doença escolhida corresponde aos sintomas fornecidos
    sintomas_reais = set(fatos.get(doenca_escolhida, []))
    sintomas_fornecidos = set(sintomas_usuario)

    sintomas_corretos = sintomas_fornecidos & sintomas_reais
    porcentagem = (len(sintomas_corretos) / len(sintomas_reais)) * 100 if sintomas_reais else 0
    porcentagem = round(porcentagem, 2)

    # Mensagem de verificação
    if sintomas_fornecidos == sintomas_reais:
        resultado = f"Os sintomas fornecidos correspondem totalmente aos sintomas conhecidos de {doenca_escolhida}. Probabilidade de ser esta doença: {porcentagem}%."
        # Se os sintomas correspondem exatamente, não mostrar outras doenças possíveis
        return render_template('resultado_verificacao.html', resultado=resultado)

    # Mostrar sintomas faltando ou adicionais
    sintomas_faltando = sintomas_reais - sintomas_fornecidos
    sintomas_adicionais = sintomas_fornecidos - sintomas_reais

    if sintomas_faltando:
        resultado = f"Parece que você não mencionou alguns sintomas importantes para {doenca_escolhida}: {', '.join(sintomas_faltando)}. Probabilidade de ser esta doença: {porcentagem}%."
    elif sintomas_adicionais:
        resultado = f"Os sintomas fornecidos indicam uma possibilidade de outra condição, além de {doenca_escolhida}. Sintomas adicionais: {', '.join(sintomas_adicionais)}. Probabilidade de ser esta doença: {porcentagem}%."

    # Encontrar outras possíveis doenças que correspondam aos sintomas fornecidos
    possiveis_doencas = []
    for doenca, sintomas in fatos.items():
        if doenca != doenca_escolhida:  # Ignorar a doença já escolhida pelo usuário
            sintomas_comuns = sintomas_fornecidos & set(sintomas)
            if len(sintomas_comuns) > 0:
                outra_porcentagem = (len(sintomas_comuns) / len(sintomas)) * 100
                possiveis_doencas.append((doenca, round(outra_porcentagem, 2)))

    # Ordenar por porcentagem de sintomas coincidentes e pegar até 3 doenças
    possiveis_doencas = sorted(possiveis_doencas, key=lambda x: x[1], reverse=True)[:3]

    return render_template('resultado_verificacao.html', resultado=resultado, possiveis_doencas=possiveis_doencas)

if __name__ == "__main__":
    app.run(debug=True)
    