# 📝 Relatório Final - Sistema Especialista para Diagnóstico de Doenças

## 🎯 Objetivo
Este relatório detalha o desenvolvimento de um sistema especialista para diagnóstico médico baseado em sintomas. O projeto utiliza a abordagem de IA lógica, e a biblioteca **Experta** foi utilizada para implementar o motor lógico.

---

## 1. 📌 Justificativa da Abordagem de IA Escolhida

A abordagem escolhida para este trabalho foi a de um **Sistema Especialista**, um tipo de IA lógica baseada em sistemas de regras. Optamos por essa abordagem por algumas razões principais:

### ✔️ **Natureza do Problema**:
O diagnóstico médico é um processo sistemático, e os médicos geralmente seguem protocolos lógicos para relacionar sintomas a doenças. Um sistema especialista é capaz de formalizar esse processo usando regras específicas.

### ✔️ **Transparência e Explicabilidade**:
Sistemas especialistas são altamente **explicáveis**. Cada inferência é baseada em regras explícitas, e isso permite que o usuário compreenda como um diagnóstico foi alcançado. Isso é fundamental na área médica, onde a confiança no diagnóstico e a rastreabilidade das decisões são importantes.

### ✔️ **Simplicidade e Controle**:
Utilizando a biblioteca **Experta**, pudemos definir um conjunto de regras determinísticas para inferir possíveis doenças, proporcionando **alto controle** sobre o comportamento do sistema.

Portanto, a abordagem escolhida foi motivada pela **simplicidade**, **explicabilidade** e capacidade de formalizar o conhecimento em regras lógicas para resolver problemas específicos.

---

## 2. 📂 Descrição e Origem do Dataset

### 📋 **Origem e Criação**:
- O dataset utilizado foi **criado manualmente** para incluir as **100 doenças mais comuns**, juntamente com seus respectivos sintomas. Este conjunto de dados foi expandido posteriormente para incluir **sintomas críticos** para cada doença, com base em pesquisas sobre sintomas característicos.
  
### 🧩 **Estrutura do Dataset**:
- Cada linha do dataset contém:
  - 📌 O nome da **doença**.
  - 🩺 Uma lista de **sintomas** associados, separados por ponto e vírgula.
  - ⚠️ Um **sintoma crítico**, que tem um peso maior durante a inferência.

### 🔍 **Adaptação**:
Algumas doenças apresentavam sintomas muito semelhantes, levando à redundância. Para garantir a **qualidade do diagnóstico**, o dataset passou por um processo de **limpeza e refinamento**, onde doenças redundantes foram removidas, e sintomas foram ajustados.

---

## 3. ⚙️ Processos de Treinamento, Ajuste e Teste

### 🔨 **Construção do Sistema Especialista**:
- **Base de Conhecimento**: Utilizamos o dataset criado como a **base de conhecimento** do sistema. Cada doença foi mapeada para seus sintomas e sintomas críticos.
- **Regras de Inferência**: O motor de inferência foi implementado utilizando a biblioteca **Experta**, que suporta regras do tipo "se-então". Essas regras verificam quais sintomas fornecidos pelo usuário se cruzam com os sintomas listados para cada doença.

### 🔧 **Ajustes do Sistema**:
- **Peso para Sintomas Críticos**: Foi dado um peso maior para sintomas críticos, de modo que, se um sintoma crítico específico estivesse presente, a pontuação da doença aumentaria.
- **Seleção dos Três Principais Diagnósticos**: Após as inferências, os diagnósticos foram ordenados pela porcentagem de correspondência, e os **três mais prováveis** foram apresentados ao usuário, para fornecer resultados mais concisos.

### 🧪 **Testes e Validação**:
- **Simulação de Casos**: O sistema foi testado usando combinações de sintomas fictícias para simular diferentes casos de diagnóstico. 
- **Métricas**:
  - A precisão e métricas tradicionais de modelos de machine learning (como **recall** e **F1-score**) não se aplicam facilmente devido à natureza determinística do sistema especialista.
  - As inferências foram verificadas qualitativamente para garantir **coerência e consistência** em comparação com a literatura médica.

---

## 4. 🔍 Análise Crítica dos Resultados

### 📊 **Resultados**:
- O sistema especialista mostrou-se capaz de **diagnosticar doenças** de forma razoável, especialmente quando todos os sintomas relevantes eram fornecidos pelo usuário.
- A introdução de **sintomas críticos** ajudou a aumentar a precisão, destacando doenças que eram mais prováveis.

### 🛑 **Dificuldades Encontradas**:
- **Sintomas Redundantes**: Havia muitos sintomas semelhantes entre diferentes doenças, o que exigiu um trabalho significativo de **refinamento do dataset**.
- **Peso dos Sintomas Críticos**: Ajustar o peso dos sintomas críticos foi um desafio, pois precisávamos encontrar um equilíbrio que fosse significativo, mas não distorcesse demais o diagnóstico.
- **Falta de Aprendizado**: O sistema especialista **não é treinável**, ou seja, ele não aprende com novos dados. Isso significa que qualquer modificação nas inferências deve ser feita através de ajustes manuais nas regras e no dataset.

### 🔄 **Fine-Tuning**:
- O ajuste fino foi feito principalmente através da **modificação das regras de inferência** e do **refinamento do dataset**.
- Regras foram ajustadas para melhorar o manuseio de sintomas comuns entre doenças e priorizar **sintomas críticos**.

---

## 🛠️ 5. Bibliotecas e Ferramentas Utilizadas

Para a construção do sistema especialista, utilizamos as seguintes bibliotecas e ferramentas:

- **Python 3.9**: Linguagem principal para implementação do sistema.
- **Experta**: Biblioteca Python para criar sistemas especialistas baseados em regras. Utilizamos Experta para definir o motor lógico do sistema e as regras de inferência.
- **Flask**: Utilizado para criar a interface web do sistema, permitindo a interação do usuário através do navegador.
- **Bootstrap 4.5**: Framework CSS utilizado para estilizar as páginas web, proporcionando uma interface amigável e responsiva.
- **CSV**: O dataset foi armazenado em formato CSV, e a biblioteca **csv** do Python foi utilizada para manipular esses dados.

---

## 🛠️ 6. Tutorial de Execução do Projeto

### 6.1. Pré-requisitos

- **Python 3.9**: Certifique-se de que o Python 3.9 está instalado. Para verificar a versão do Python, execute:
  ```sh
  python --version
Se precisar instalá-lo, acesse o site oficial do Python.

Pip: Certifique-se de que o pip está instalado para gerenciar pacotes do Python. Para verificar:
```sh
pip --version
```
Caso não esteja instalado, siga as instruções na página do Pip.
6.2. Instalar as Dependências
Criar um Ambiente Virtual (opcional): Crie um ambiente virtual para isolar as dependências do projeto:


```sh
python -m venv env
```
Ative o ambiente virtual:

Windows:

```
.\env\Scripts\activate
```
Linux/Mac:

```sh
source env/bin/activate

```
Instalar as Bibliotecas Necessárias: Execute o comando abaixo para instalar as dependências:


```sh
pip install -r requirements.txt
```
Clonar o Repositório: Clone o repositório do projeto para sua máquina local:


```sh
git clone <link-do-repositorio>
```
Entre no diretório do projeto:
```sh
cd nome-do-projeto

```
Executar o Servidor Flask: Execute o script app.py para iniciar o servidor local:


```sh
python app.py
```
Se o servidor estiver rodando corretamente, você verá uma mensagem indicando que o Flask está ativo em http://127.0.0.1:5000/.

Acessar o Sistema: Abra o navegador e vá até http://127.0.0.1:5000/ para acessar a interface do sistema.

###🔚 Conclusão
O sistema desenvolvido é um exemplo clássico de um sistema especialista, utilizando regras de produção para inferir possíveis doenças a partir dos sintomas fornecidos pelo usuário. Embora o sistema não seja treinável, ele é altamente explicável e proporciona confiança e transparência nas inferências, uma vez que o processo lógico é explícito e rastreável.

Este sistema possui algumas limitações de adaptabilidade, mas oferece um ponto de partida sólido para problemas que requerem uma abordagem determinística e rastreável. Para futuras melhorias, recomenda-se integrar um componente de aprendizado de máquina para tornar o sistema mais adaptável a novos dados.
