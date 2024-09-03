# SintomaTech

## Descrição

O **SintomaTech** é uma aplicação web desenvolvida para registrar sintomas, sugerir possíveis doenças com base nesses sintomas e gerar relatórios detalhados para auxiliar médicos. O sistema utiliza tecnologia avançada para comparar sintomas e identificar doenças, oferecendo uma ferramenta intuitiva e eficaz para diagnóstico.

## Tecnologias Utilizadas

- **Backend:**
  - **Node.js**: Ambiente de execução JavaScript no servidor.
  - **TypeScript**: Superset do JavaScript para tipagem estática.
  - **TypeORM**: ORM para manipulação do banco de dados.
  - **Express**: Framework para criação de APIs RESTful.
  - **SQLite**: Banco de dados relacional leve para desenvolvimento.

- **Frontend (opcional):**
  - **React** ou **Vue.js**: Bibliotecas para criar interfaces de usuário interativas.

- **Ferramentas de Desenvolvimento:**
  - **Postman**: Para testar e documentar as APIs.
  - **Figma**: Para criar fluxos de telas e protótipos.

## Requisitos Funcionais

1. **Cadastro e Gerenciamento de Sintomas:**
   - Permitir que os usuários registrem sintomas com descrição, gravidade e data.
   - Exibir o histórico de sintomas para cada usuário.

2. **Diagnóstico de Doenças:**
   - Receber uma lista de sintomas e sugerir possíveis doenças com base em um banco de dados de doenças e sintomas.
   - Identificar a doença que mais se assemelha aos sintomas relatados, comparando a lista de sintomas do usuário com a lista de sintomas vinculados a cada doença.

3. **Geração de Relatórios:**
   - Gerar relatórios detalhados sobre os sintomas dos usuários para facilitar a análise médica.

4. **Cadastro e Autenticação de Usuários:**
   - Permitir o cadastro e autenticação de usuários para garantir o acesso ao histórico de sintomas e relatórios.

## Requisitos Não Funcionais

1. **Desempenho:**
   - O sistema deve responder a requisições de API em menos de 500ms.
   
2. **Segurança:**
   - Implementar autenticação e autorização para proteger dados sensíveis dos usuários.
   - Garantir que os dados sejam armazenados e transmitidos de forma segura (utilizando HTTPS).

3. **Escalabilidade:**
   - O sistema deve ser escalável para suportar um número crescente de usuários e dados.

4. **Usabilidade:**
   - Interface intuitiva e fácil de usar para ambos os usuários e médicos.

## Regras de Negócio

1. **Diagnóstico:**
   - O sistema sugere possíveis doenças com base na correspondência dos sintomas fornecidos pelo usuário com o banco de dados de doenças e sintomas.
   - A doença mais semelhante é identificada usando algoritmos de comparação, calculando a similaridade entre os sintomas fornecidos e os sintomas vinculados a cada doença.

2. **Relatórios:**
   - Relatórios são gerados com base no histórico de sintomas e devem incluir uma análise resumida dos sintomas relatados.

3. **Histórico de Sintomas:**
   - O histórico de sintomas é mantido para cada usuário e pode ser acessado a qualquer momento.

4. **Dados de Usuários:**
   - Dados pessoais e históricos de sintomas são confidenciais e devem ser acessíveis apenas ao usuário e aos médicos autorizados.

## Modelagem do Banco de Dados

**Entidades e Relacionamentos:**

- **Usuário (User)**
  - `id` (Chave Primária)
  - `nome`
  - `idade`

- **Sintoma (Symptom)**
  - `id` (Chave Primária)
  - `descricao`
  - `gravidade`
  - `data`
  - `usuarioId` (Chave Estrangeira referenciando `User`)

- **Doença (Disease)**
  - `id` (Chave Primária)
  - `nome`
  - `descricao`

- **DoençaSintoma (DiseaseSymptom)**
  - `id` (Chave Primária)
  - `doencaId` (Chave Estrangeira referenciando `Disease`)
  - `sintomaId` (Chave Estrangeira referenciando `Symptom`)

- **Relatório (Report)**
  - `id` (Chave Primária)
  - `usuarioId` (Chave Estrangeira referenciando `User`)
  - `geradoEm`
  - `conteudo`

**Relacionamentos:**

- Um usuário pode ter muitos sintomas (Um-para-Muitos).
- Uma doença pode ter muitos sintomas associados (Muitos-para-Muitos com sintomas, usando a entidade intermediária `DoençaSintoma`).
- Um usuário pode ter muitos relatórios (Um-para-Muitos).

## Fluxos das Principais Telas

**Tela de Entrada de Sintomas:**

1. **Usuário** acessa o formulário de entrada de sintomas.
2. **Usuário** preenche a descrição, gravidade e data dos sintomas.
3. **Usuário** submete o formulário.
4. **Sistema** armazena os sintomas e confirma o recebimento.

**Tela de Diagnóstico:**

1. **Usuário** envia uma lista de sintomas para diagnóstico.
2. **Sistema** processa os sintomas e consulta o banco de dados.
3. **Sistema** compara a lista de sintomas fornecida com os sintomas vinculados a cada doença.
4. **Sistema** identifica a doença com a maior similaridade com os sintomas fornecidos e retorna uma lista de possíveis doenças.
5. **Usuário** visualiza as sugestões de doenças.

**Tela de Relatórios:**

1. **Médico** acessa a lista de relatórios disponíveis.
2. **Médico** seleciona um relatório para visualizar detalhes.
3. **Sistema** exibe o relatório detalhado com o histórico de sintomas.

## Documentação da API com Postman

1. **Criar Coleção no Postman:**
   - Adicione uma nova coleção para o projeto.

2. **Adicionar Requisições:**
   - **POST /sintomas**: Para registrar sintomas.
   - **GET /sintomas**: Para obter todos os sintomas.
   - **POST /diagnostico**: Para receber sugestões de doenças e identificar a mais semelhante.
   - **POST /relatorios**: Para gerar relatórios.

3. **Definir Exemplos e Testes:**
   - Adicione exemplos de payloads e respostas para cada endpoint.
   - Configure testes básicos para validar a resposta da API.

4. **Exportar e Compartilhar:**
   - Exporte a coleção e compartilhe o link com a equipe ou stakeholders.
