# Desafio CGR - Sistema de Monitoramento de Rede e Alocação de Recursos

## 🧩 Introdução

Este repositório apresenta a solução desenvolvida para o **Desafio de Desenvolvimento Júnior - CGR**, que propõe a criação de um sistema simplificado para **monitoramento de rede e alocação de recursos** em uma empresa de telecomunicações.

O sistema foi projetado para simular um ambiente real onde a empresa gerencia uma ampla infraestrutura de rede. A ferramenta permite:

- Monitorar o status dos equipamentos de rede;
- Alocar e desalocar recursos (como portas de switch e endereços IP);
- Identificar gargalos, falhas e possíveis pontos críticos na infraestrutura.

O foco principal está na **robustez da lógica de negócio**, **integração entre os componentes** e na utilização de **Python, SQL, APIs REST e algoritmos** para fornecer uma solução funcional e bem estruturada.

> **Nota:** A interface gráfica não foi priorizada neste desafio, de acordo com a proposta, permitindo concentrar os esforços na implementação da lógica e arquitetura do sistema.

## 🚀 Como Rodar o Projeto

Este projeto pode ser executado de duas formas:

1. Diretamente com Python (`run.py`);
2. Utilizando Docker Compose para encapsular todos os serviços.

### 🔧 Pré-requisitos

- Python
- Git instalado
- [Opcional] Docker e Docker Compose (para execução em containers)

### 🐍 Método 1: Executando com Python

#### 1. Clone o repositório

```bash
git clone https://github.com/MarcosAndreLS/Desafio_CGR.git
cd Desafio_CGR
```

#### 2. Crie e ative um ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```
**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Execute o projeto

```bash
python run.py
```

**A aplicação será iniciada localmente e estará acessível em http://localhost:5000**

### 🐳 Método 2: Executando com docker-compose

#### 1. Clone o repositório

```bash
git clone https://github.com/MarcosAndreLS/Desafio_CGR.git
cd Desafio_CGR
```

#### 2.  Execute o projeto

```bash
docker-compose up --build
```

**A aplicação será exposta na porta definida no docker-compose.yml (por padrão, 5000).**

