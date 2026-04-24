Markdown
# 🌦️ ETL Weather Pipeline: OpenWeatherMap para PostgreSQL

Um pipeline de dados automatizado construído em **Python** que extrai dados meteorológicos em tempo real da API do OpenWeatherMap, realiza a limpeza e transformação dos dados utilizando **Pandas**, e carrega os resultados em um banco de dados **PostgreSQL** hospedado em um container **Docker**.

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+** (Linguagem principal)
* **Pandas** (Transformação e manipulação de dados)
* **SQLAlchemy & Psycopg2** (Conexão e modelagem de banco de dados)
* **Requests** (Extração via API)
* **Docker** (Hospedagem do banco de dados)
* **python-dotenv** (Gerenciamento seguro de credenciais)

---

## 🏗️ Arquitetura do Pipeline

O projeto segue a arquitetura clássica de **ETL (Extract, Transform, Load)**:

1. **Extract (`src/extract_data.py`):** Conecta-se à API do OpenWeatherMap para buscar os dados climáticos atuais de São Paulo. Possui tratamento de erros e salva um backup bruto do JSON extraído localmente (`data/weather_data.json`).
2. **Transform (`src/transform_data.py`):** Lê o arquivo JSON bruto, nivela estruturas aninhadas (`json_normalize`), remove colunas não utilizadas (como `sys.id` e ícones), renomeia as colunas para um padrão limpo (snake_case) e converte timestamps UNIX para o fuso horário de São Paulo (`America/Sao_Paulo`).
3. **Load (`src/load_data.py`):** Estabelece uma conexão segura com o banco de dados PostgreSQL usando SQLAlchemy. Carrega os dados transformados na tabela `sp_weather` e valida a inserção contando as linhas cadastradas.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* Python instalado na máquina (ou rodando via WSL).
* Docker Desktop (para rodar o banco de dados PostgreSQL).
* Uma chave de API gratuita do [OpenWeatherMap](https://openweathermap.org/api).

### 2. Configuração do Banco de Dados
Suba o container do PostgreSQL usando o Docker (você pode usar um `docker-compose.yml` ou o comando direto):
```bash
docker run --name postgres -e POSTGRES_USER=seu_usuario -e POSTGRES_PASSWORD=sua_senha -e POSTGRES_DB=youtube_weather_data -p 5432:5432 -d postgres
3. Configurando as Variáveis de Ambiente
Crie um arquivo chamado .env na pasta config/ (ou na raiz do projeto, dependendo da sua estrutura).

⚠️ Atenção: Não utilize aspas ou espaços ao redor dos valores no arquivo .env.

Snippet de código
API_KEY=sua_chave_da_api_aqui
DB_DATABASE=youtube_weather_data
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
4. Instalando as Dependências
Instale os pacotes necessários listados no arquivo de requisitos. Se você estiver usando o uv (como ambiente virtual e gerenciador de pacotes), rode:

Bash
uv pip install -r requirements.txt
(Ou utilize pip install -r requirements.txt)

5. Rodando o Pipeline
Com o banco de dados rodando e as dependências instaladas, execute o script principal:

Bash
uv run main.py
Exemplo de Log de Sucesso:
Plaintext
2026-04-23 19:40:59 - INFO - -> Conectando ao 192.168.100.8:5432/youtube_weather_data
2026-04-23 19:40:59 - INFO - ETAPA 1: EXTRACT
2026-04-23 19:41:00 - INFO - ETAPA 2: TRANSFORM
2026-04-23 19:41:03 - INFO - ETAPA 3: LOAD
2026-04-23 19:41:03 - INFO - Total de registro na tabela: 1
✅ Pipeline concluído com sucesso!
📂 Estrutura do Projeto
Plaintext
📁 tutorial_pipeline_open/
│
├── 📁 config/
│   └── .env                   # Credenciais e tokens (NÃO comitar este arquivo)
├── 📁 data/
│   └── weather_data.json      # Dados brutos extraídos (cache)
├── 📁 src/
│   ├── extract_data.py        # Módulo de extração
│   ├── transform_data.py      # Módulo de transformação (Pandas)
│   └── load_data.py           # Módulo de carga (SQLAlchemy)
│
├── main.py                    # Orquestrador do pipeline
└── requirements.txt           # Bibliotecas do projeto
📝 Notas de Desenvolvimento
WSL vs Docker: O projeto está configurado para permitir que o script Python rodando dentro do WSL alcance o PostgreSQL rodando no Docker host. Isso é feito injetando o IP local da máquina Windows no arquivo principal (substituindo o localhost).

Tratamento da API: A API OpenWeatherMap altera o schema de colunas (como a presença de sys.type). O pipeline lida com essas variações dinamicamente no processo de deleção de colunas antes da carga.