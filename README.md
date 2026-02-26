# 🎥 Hack Video Worker Service

Microsserviço responsável por consumir mensagens de uma fila SQS, orquestrar o processamento de vídeos (fazendo chamadas HTTP para a API de processamento) e gerenciar os arquivos no S3.
Desenvolvido em **Python (Async)** com arquitetura limpa, e deploy automatizado via **Kubernetes (EKS)**.

![Python Version](https://img.shields.io/badge/python-3.13-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

## 🚀 Tecnologias

- **Linguagem:** Python 3.13
- **Processamento Assíncrono:** `asyncio`, `aiohttp`, `aioboto3`
- **Validação e Configurações:** `pydantic`, `pydantic-settings`
- **Infraestrutura AWS:** SQS, S3
- **Infraestrutura/Deploy:** Docker, Kubernetes (EKS), Kustomize, Terraform
- **CI/CD:** GitHub Actions
- **Testes:** Pytest

## ⚙️ Configuração Local

### Pré-requisitos
- Python 3.13
- Pipenv (para gerenciamento de pacotes)
- Docker (opcional, para rodar tudo no contêiner)
- Acesso à AWS (para S3 e SQS)

### Variáveis de Ambiente
As variáveis principais necessárias para rodar o projeto localmente são:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=sua_key
AWS_SECRET_ACCESS_KEY=sua_secret
AWS_SESSION_TOKEN=seu_token

QUEUE_URL=https://sqs.us-east-1.amazonaws.com/sua_conta/sua_fila
BUCKET=nome_do_seu_bucket

PROCESSING_API_URL=http://localhost:8080/process
INGEST_API_URL=http://localhost:8081
RESULT_API_URL=http://localhost:8080/resultado
SEMAPHORE_LIMIT=5
```
*Nota: Se estiver usando AWS Academy, lembre-se de atualizar `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `AWS_SESSION_TOKEN` a cada 4 horas.*

### Rodando o Projeto

Você pode rodar localmente com Pipenv e Make:

```bash
# Instala as dependências
make install

# Inicia o worker
make start
```

## 🧪 Testes e Qualidade

O projeto utiliza o **Pytest** para os testes automatizados, e possui regras de cobertura de código (`pytest-cov`).

Para rodar os testes localmente e verificar a cobertura:
```bash
# Roda todos os testes exibindo os pacotes sem cobertura no terminal
make test

# Roda os testes gerando relatório HTML
make test-coverage
```

Também há comandos para garantir a qualidade do código com `black`, `flake8` e `isort`:
```bash
make black
make flake8
make isort
```

## 📦 Deploy e Infraestrutura

O deploy é automatizado via **GitHub Actions** para o cluster EKS na AWS.

### 🔄 Pipeline de CI/CD (DevSecOps)

A nossa pipeline roda sempre que há um push ou pull request na branch `main`:

1. **Docker Build**
   - Construção inicial da imagem utilizando `docker buildx` e armazenamento provisório no GitHub Container Registry (GHCR).
2. **Testes Unitários (CI)**
   - Roda os testes unitários (`make test`) em um ambiente docker isolado utilizando a imagem gerada no passo anterior.
3. **Build e Deploy (CD)**
   - Caso os testes passem, envia a imagem de forma definitiva para o **Amazon ECR** com tag versionada.
   - Atualiza o kubeconfig do EKS.
   - Injeta as credenciais seguras e variáveis de ambiente dinamicamente nos manifestos YAML do Kubernetes utilizando `envsubst`.
   - Aplica os manifestos via **Kustomize** e valida o rollout da aplicação no EKS (`kubectl rollout status`).

### 🛡️ Boas Práticas Implementadas

- **Processamento Concorrente Seguro:** Uso de SQS com pooling assíncrono e `asyncio.Semaphore` para limitar e controlar as requisições em paralelo (evitando indisponibilidade sistêmica e consumo exacerbado de memória/CPU).
- **Injeção de Variáveis em Tempo de Runtime:** As credenciais sensíveis nunca ficam estáticas. Ficam configuradas diretamente nas Secrets do GitHub e provisionadas em recursos como Secret e ConfigMap no Kubernetes no momento do Deploy.
- **Isolamento de Testes:** Os testes na branch main pelo CI são acionados diretamente utilizando a imagem de contêiner com `docker run`. Isso garante maior fidelidade com o ambiente de produção.
- **Arquitetura Limpa:** O código é fragmentado e modularizado utilizando _interfaces_, _use cases_ e _infrastructure_, permitindo uma manutenção fluida.

---

### Exemplo de Mensagem no SQS (Payload esperado)

```json
{
  "s3_path": "uploads",
  "filename": "video_teste.mp4"
}
```
