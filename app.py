
import csv
from experta import *
from flask import Flask, render_template, request

# Código em Python para um sistema especialista que faz diagnóstico baseado em sintomas usando Experta (baseado em sistemas especialistas)

# Definindo uma variável global para o caminho do dataset
CAMINHO_CSV = 'dataset_sintomas.csv'

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

# Carregar os fatos sobre doenças e seus sintomas a partir de um arquivo CSV
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

# Inicializar o Flask app
app = Flask(__name__)

# Carregar fatos do dataset
fatos, sintomas_criticos = carregar_fatos(CAMINHO_CSV)

# Criar uma lista de sintomas para o formulário
todos_sintomas = sorted({sintoma for sintomas in fatos.values() for sintoma in sintomas})

@app.route('/')
def index():
    return render_template('index.html', todos_sintomas=todos_sintomas)

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
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
    
    # Ordenar os diagnósticos pela porcentagem de forma decrescente
    diagnosticos = sorted(diagnosticos, key=lambda x: x[1], reverse=True)
    
    if not diagnosticos:
        resultado = "Nenhum diagnóstico encontrado com os sintomas fornecidos."
    else:
        resultado = [f"{doenca}: {int(porcentagem)}%" for doenca, porcentagem in diagnosticos]
    
    return render_template('resultado.html', resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)