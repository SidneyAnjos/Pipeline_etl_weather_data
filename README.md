# 🌤️ Pipeline ETL - Dados Climáticos de São Paulo

> Pipeline ETL automatizado para coleta, transformação e armazenamento de dados meteorológicos em tempo real da cidade de São Paulo, orquestrado com Apache Airflow e Docker.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura do Pipeline](#-arquitetura-do-pipeline)
- [Stack Tecnológica](#-stack-tecnológica)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
- [Detalhamento das Etapas (ETL)](#-detalhamento-das-etapas)
- [Troubleshooting Comum](#-troubleshooting)

---

## 🎯 Sobre o Projeto

Este projeto demonstra a construção de um **pipeline ETL completo** utilizando as melhores práticas de Engenharia de Dados. 

O pipeline coleta dados meteorológicos da API do OpenWeatherMap a cada hora, transforma os dados de um JSON aninhado para um formato tabular estruturado (salvando temporariamente em `.parquet` para performance), e os carrega em um banco de dados PostgreSQL para análises futuras.

---

## 🏗️ Arquitetura do Pipeline

<div align="center">
  <img src="arquitetura_de_dados_draw.png" alt="Arquitetura do Pipeline ETL" width="800">
</div>

---

## 🛠️ Stack Tecnológica

### Core e Infraestrutura
* **Python 3.10+** - Linguagem principal
* **Apache Airflow (CeleryExecutor)** - Orquestração do pipeline
* **PostgreSQL 16** - Banco de dados relacional (Data Warehouse)
* **Docker & Docker Compose** - Containerização e isolamento de ambiente
* **Redis** - Message broker para as tarefas do Celery

### Bibliotecas Python (`uv.lock`)
* **pandas** - Transformação, limpeza e manipulação de dados
* **requests** - Extração de dados via requisições HTTP
* **SQLAlchemy & psycopg2-binary** - Conexão e modelagem do banco de dados
* **python-dotenv** - Gerenciamento seguro de credenciais

---

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
* Git instalado
* Docker e Docker Compose instalados na máquina (ou WSL)
* Gerenciador de pacotes `uv` (opcional, mas recomendado para testes locais)

### 2. Configuração do Ambiente e Credenciais
Crie um arquivo `.env` dentro da pasta `config/`:

```env
# config/.env
```
# Chave da API do OpenWeatherMap
API_KEY=sua_chave_api_aqui

# Credenciais do PostgreSQL (Airflow)
user=airflow
password=airflow
database=airflow
⚠️ Atenção: O arquivo .env está no .gitignore e nunca deve ser "commitado".

3. Configuração de Permissões do Docker (Linux/WSL)
Para evitar problemas de permissão de pastas com o Airflow, crie um arquivo .env na raiz do projeto contendo o seu User ID:

Bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
4. Inicializando os Containers
No terminal, execute o comando para baixar as imagens e subir a infraestrutura:

Bash
docker-compose up -d
Aguarde alguns minutos. Você pode verificar se tudo está rodando com docker-compose ps.

🎮 Como Executar
1. Acesso ao Apache Airflow
Abra o seu navegador e acesse: http://localhost:8080

Usuário: airflow | Senha: airflow

2. Ativação da DAG
Localize a DAG youtube_weather_pipeline.

Clique no botão de Unpause (toggle) e depois em Trigger DAG (▶️).

O pipeline extrairá o clima de São Paulo, fará o tratamento e salvará no banco a cada 1 hora (0 */1 * * *).

🔍 Detalhamento das Etapas (ETL)
📥 1. Extract (src/extract_data.py)
Faz a requisição HTTP GET para a API do OpenWeatherMap. Possui validação de status code e salva um snapshot bruto (RAW) dos dados em data/weather_data.json como garantia de linhagem de dados.

🔄 2. Transform (src/transform_data.py)
Utiliza pandas para ler o JSON, aplicar json_normalize nas colunas aninhadas e limpar a estrutura.

Converte temperaturas de Kelvin/Fahrenheit para Celsius (via API parameters).

Converte os campos Unix Timestamp (dt, sunrise, sunset) para o timezone correto (America/Sao_Paulo).

Salva os dados transformados em data/temp_data.parquet para otimizar o transporte de dados no Airflow (substituindo o uso pesado de XComs).

💾 3. Load (src/load_data.py)
Lê o arquivo Parquet gerado na etapa anterior e estabelece conexão com o PostgreSQL via SQLAlchemy. Carrega os dados na tabela sp_weather e retorna um log de validação com o total de registros inseridos.

🐛 Troubleshooting Comum
1. Erro ModuleNotFoundError: No module named 'src' no Airflow

Causa: O container do Airflow não sabe onde os módulos estão.

Solução: O docker-compose.yaml deste projeto já mapeia o volume da pasta src. Certifique-se de que a variável de ambiente PYTHONPATH: /opt/airflow está declarada na secção x-airflow-common do Docker Compose.

2. Erro de conexão com o Banco de Dados (Connection Refused)

Causa: Conflito de rede entre o container e o host.

Solução: No arquivo src/load_data.py, se o código estiver a rodar dentro do Airflow via Docker, a variável host deve ser 'postgres' (o nome do serviço no docker-compose), e não 'localhost'.

3. Como consultar os dados no banco?
Você pode acessar o banco do Airflow rodando o comando interativo do Docker:

Bash
docker-compose exec postgres psql -U airflow -d airflow
Dentro do terminal SQL, execute: SELECT * FROM sp_weather;
