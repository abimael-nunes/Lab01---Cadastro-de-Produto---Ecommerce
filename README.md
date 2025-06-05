
# E-commerce na Nuvem com Streamlit, Azure SQL e Azure Blob Storage

## Introdução

Este projeto é uma aplicação web simples desenvolvida em Streamlit que simula o cadastro e a listagem de produtos para um e-commerce. Ele demonstra a integração com serviços de nuvem da Microsoft Azure: utilizando Azure SQL Database para persistência de dados de produtos e Azure Blob Storage para armazenamento de imagens.


## 🚀 Sobre o Projeto
Este repositório contém o código-fonte de um projeto prático desenvolvido durante um bootcamp da DIO (Digital Innovation One). O objetivo principal foi explorar e aplicar conhecimentos sobre:

- Desenvolvimento Web com Streamlit: Criação de interfaces de usuário interativas e de fácil implementação em Python.
- Armazenamento de Dados na Nuvem com Azure SQL Database: Gerenciamento de um banco de dados relacional hospedado na nuvem.
- Armazenamento de Objetos com Azure Blob Storage: Upload e recuperação de arquivos binários (imagens) de forma escalável e segura.
- Conectividade Python com Bancos de Dados: Utilização da biblioteca pymssql para interagir com o SQL Server.
A aplicação permite que os usuários cadastrem novos produtos, informando nome, descrição, preço e fazendo upload de uma imagem. As informações textuais são salvas no Azure SQL, enquanto as imagens são enviadas para o Azure Blob Storage, e sua URL é armazenada no banco de dados. Posteriormente, é possível listar todos os produtos cadastrados, exibindo-os com suas respectivas imagens.

## 🛠️ Tecnologias Utilizadas
As seguintes tecnologias foram empregadas neste projeto:

- Python: Linguagem de programação principal.
- Streamlit: Framework Python para construção de aplicações web de dados.
- Azure SQL Database: Serviço de banco de dados relacional gerenciado na nu nuvem (PaaS).
- Azure Blob Storage: Serviço de armazenamento de objetos escalável e de baixo custo.
- ```azure-storage-blob```: SDK Python para interagir com Azure Blob Storage.
- ```pymssql```: Adaptador Python para Microsoft SQL Server.
- ```uuid```: Módulo Python para geração de identificadores únicos universais.
- ```json``` e ```os```: Módulos Python para manipulação de arquivos e sistema operacional (usados para o salvamento local opcional).

## ⚙️ Configuração e Execução
Para rodar este projeto localmente, siga os passos abaixo:

**Pré-requisitos**
- **Python** 3.8+ instalado.
- Acesso a uma conta **Azure** com permissões para criar e configurar:
    - Um **Azure SQL Database** (com uma tabela ```Produtos``` conforme o esquema abaixo).
    - Uma conta de **Azure Storage** (com um contêiner de blobs ```fotos```).
- **Conectividade** com os serviços Azure a partir do ambiente onde você executará a aplicação.

**1. Clonar o Repositório**

```
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

**2. Instalar as Dependências**

Crie um ambiente virtual (recomendado) e instale as bibliotecas necessárias:

```
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**3. Configurar o Azure SQL Database**

Certifique-se de ter um Azure SQL Database configurado. Você precisará de uma tabela chamada ```Produtos``` (dentro do esquema ```dbo```) com as seguintes colunas:

```SQL
CREATE TABLE dbo.Produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(255) NOT NULL,
    descricao NVARCHAR(MAX),
    preco DECIMAL(10, 2),
    imagem_url NVARCHAR(MAX)
);
```
**Importante:** Configure as regras de firewall do seu Azure SQL Database para permitir conexões do seu endereço IP local ou da rede onde a aplicação será executada.

**4. Configurar o Azure Blob Storage**

Certifique-se de ter uma conta de armazenamento no Azure e um contêiner de blobs chamado ```fotos```.

**5. Atualizar as Credenciais**

```Python
# app.py (trecho)
# ...
BLOB_CONNECTION_STRING = "SUA_BLOB_CONNECTION_STRING_AQUI"
BLOB_CONTAINER_NAME = "fotos" # Ou o nome do seu contêiner
BLOB_ACCOUNT_NAME = "SEU_BLOB_ACCOUNT_NAME_AQUI"

SQL_SERVER = "SEU_SQL_SERVER_AQUI.database.windows.net"
SQL_DATABASE = "SEU_SQL_DATABASE_AQUI"
SQL_USER_AAD = "SEU_SQL_USER_AQUI"
SQL_PASSWORD_AAD = "SUA_SQL_PASSWORD_AQUI"
# ...
```

**6. Executar a Aplicação Streamlit**

Após configurar tudo, execute a aplicação Streamlit no terminal:

```
streamlit run app.py
```
Isso abrirá a aplicação no seu navegador web, geralmente em http://localhost:8501.

## 💡 Como Funciona
**1. Formulário de Cadastro:** A interface do Streamlit permite inserir nome, descrição, preço e selecionar um arquivo de imagem.

**2. Upload da Imagem:** Ao clicar em "Cadastrar Produto", se uma imagem for fornecida, a função ```upload_image_to_blob``` é chamada. Ela gera um nome único para o arquivo e o envia para o contêiner ```fotos``` no Azure Blob Storage, retornando a URL pública da imagem.

**3. Inserção no Banco de Dados:** Os detalhes do produto (nome, descrição, preço e a URL da imagem) são então enviados para a função ```insert_product_into_sql```, que os insere na tabela ```dbo.Produtos``` no Azure SQL Database.

**4. Listagem de Produtos:** A função ```display_product_list``` recupera todos os produtos do Azure SQL Database, incluindo suas URLs de imagem, e os exibe na interface do Streamlit em um formato de grade.

## 🤝 Contribuições
Este projeto foi desenvolvido como parte de um bootcamp, mas melhorias e contribuições são sempre bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 🎓 Agradecimentos
Este projeto foi realizado como parte do bootcamp de Desenvolvimento Cloud da **DIO (Digital Innovation One)**, com o apoio de diversos instrutores e da comunidade. Um agradecimento especial por proporcionar a oportunidade de aprender e aplicar tecnologias de nuvem na prática.
