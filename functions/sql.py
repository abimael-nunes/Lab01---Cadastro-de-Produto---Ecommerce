import pymssql
import streamlit as st
from settings import SQL_SERVER, SQL_USER_AAD, SQL_PASSWORD_AAD, SQL_DATABASE

def insert_product_into_sql(product_data):
    """
    Insere os dados de um produto na tabela 'Produtos' do Azure SQL Server.

    Args:
        product_data (dict): Um dicionário contendo 'nome', 'descricao', 'preco' e 'imagem_url'.

    Returns:
        bool: True se a inserção for bem-sucedida, False caso contrário.
    """
    try:
        # Conecta-se ao Azure SQL Server
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER_AAD, password=SQL_PASSWORD_AAD, database=SQL_DATABASE)
        cursor = conn.cursor()

        # Query SQL para inserção de dados
        insert_query = """
        INSERT INTO dbo.Produtos (nome, descricao, preco, imagem_url)
        VALUES (%s, %s, %s, %s)
        """
        # Executa a query com os dados do produto
        cursor.execute(insert_query, (product_data["nome"], product_data["descricao"], product_data["preco"], product_data["imagem_url"]))
        conn.commit() # Confirma a transação

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir produto no Azure SQL Server: {e}")
        return False

def get_products_from_sql():
    """
    Recupera todos os produtos da tabela 'Produtos' do Azure SQL Server.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um produto.
              Retorna uma lista vazia em caso de erro.
    """
    try:
        # Conecta-se ao Azure SQL Server
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER_AAD, password=SQL_PASSWORD_AAD, database=SQL_DATABASE)
        # Cursor com as_dict=True retorna os resultados como dicionários, facilitando o acesso
        cursor = conn.cursor(as_dict=True)
        query = "SELECT id, nome, descricao, preco, imagem_url FROM dbo.Produtos"
        cursor.execute(query)
        rows = cursor.fetchall() # Recupera todas as linhas
        
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos do Azure SQL Server: {e}")
        return []

# --- Funções de UI (Streamlit) ---

def display_product_list():
    """
    Exibe a lista de produtos cadastrados no Azure SQL Server na interface do Streamlit
    em um formato de grade (cards).
    """
    st.header("Produtos Cadastrados")
    products = get_products_from_sql() # Obtém os produtos do banco de dados

    if products:
        cards_per_row = 3 # Define o número de cards por linha para a exibição em grade
        
        # Itera sobre os produtos e os organiza em colunas (cards)
        for i, product in enumerate(products):
            # Cria novas colunas para cada linha de cards
            if i % cards_per_row == 0:
                cols = st.columns(cards_per_row)
            
            # Seleciona a coluna atual para exibir o card do produto
            with cols[i % cards_per_row]:
                st.markdown(f"### {product['nome']}") # Nome do produto como título
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                
                # Exibe a imagem se a URL estiver disponível
                if product["imagem_url"]:
                    # Usa markdown com HTML para controlar o tamanho da imagem
                    html_img = f'<img src="{product["imagem_url"]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                
                st.markdown("---") # Linha separadora entre os cards
    else:
        st.info("Nenhum produto encontrado. Cadastre um novo produto!")