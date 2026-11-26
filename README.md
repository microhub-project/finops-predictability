<img src="https://drive.google.com/thumbnail?id=1F9ZayTh5WS-dyqXuZ1eFlD7_pl5naQwv&sz=w1000" alt="Logo MicroHub" width="500">

# FinOps Predictability

## Sobre o projeto

O FinOps Predictability é uma API que faz parte do projeto [MicroHub](https://github.com/microhub-project), funcionando como microsserviço de predição. Seus dois principais componentes são:

- AWS cost fetch
- API de predição

### AWS cost fetch

O AWS Cost fetch é responsável pela atualização dos **tipos de instâncias** no **banco de dados**.

Para que isso funcione de forma adequada, realizamos uma requisição para a API externa da [ec2.shop](https://github.com/yeo/ec2.shop), tratamos os dados recebidos e analisamos cada um dos tipos de instância disponíveis no serviço da AWS EC2 realizando as seguintes ações:
- Caso o tipo de instância não exista no banco de dados, ele é adicionado;
- Caso o tipo de instância já exista, seu custo, quantidade de CPUs e de RAM são comparados com o resultado da API e, caso haja diferença, os registro é atualizado no banco de dados.

### API de predição

Essa API tem como sua finalidade servir o [sistema web](https://github.com/microhub-project/web-application) com predições baseadas em dados e na necessidade de escalar sua infraestrutura (ou instância, dependendo do endpoint chamado), analisando as possibilidades de escalar vertical ou horizontalmente, bem como seu aumento em custo, quantidade de CPUs e RAM.

A API de predição roda na porta `:8000`, que é a porta padrão do **framework web `FastAPI`**, para acessar a documentação da API, contendo todas suas rotas, corpo das requisições e objetos mapeados, acesse a URL [http://localhost:8000/docs#](http://localhost:8000/docs#) no navegador.

## Como utilizar

Após clonar o repositório, siga os passos abaixo para utilizar o sistema:

**Pré-requisito:** é necessário possuir o `Redis` instalado em sua máquina. Caso não possua, siga o guia de instalação para o seu sistema operacional na [documentação oficial do Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/).

1. Crie um **virtual environment** (`.venv`) Python na sua IDE utilizando a versão `3.14`;
2. Execute o comando abaixo para instalar todas as dependências do projeto;
    ```
    pip install -r requirements.txt
    ```
3. Utilize o arquivo `.env.example` como base para criar **um novo arquivo** `.env` e preencher as variáveis de ambiente;
4. Caso não possua o banco de dados populado, acesse o [diretório database](https://github.com/microhub-project/web-application/tree/main/src/database) do sistema web e execute os arquivos `db.sql` e `data.sql`;
5. Ative o ambiente Python executando o comando abaixo;
    ```
    source /{CAMINHO_DO_PROJETO}/.venv/bin/activate
    ```
6. Execute o script que desejar executando o comando abaixo.
    ```
    /{CAMINHO_DO_PROJETO}/.venv/bin/python /{CAMINHO_DO_PROJETO}/{ARQUIVO}.py
    ```

## Equipe MicroHub

- [Amanda Cardoso Reys](https://github.com/amandareys)
- [Andy Lin Araujo](https://github.com/Andylinaraujo)
- [Gabriel Matias da Palma](https://github.com/GabrielMatiasDaPalma)
- [Juan Oliveira Rodrigues](https://github.com/Juan-Oliveira-Rodrigues)
- [Lucas Raphael Garcia Quinália](https://github.com/lucasquinalia)
- [Yuri Aguilera Proença](https://github.com/aguilera-yuri)