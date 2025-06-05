import streamlit as st
import json
import os

# Importar funções
from functions.blob import upload_image_to_blob
from functions.sql import insert_product_into_sql, display_product_list

# --- Layout Principal da Aplicação Streamlit ---

st.title("Cadastro de Produto - E-Commerce na Cloud")

# Formulário para entrada de dados do produto
st.header("Novo Produto")
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

# Botão para iniciar o processo de cadastro
if st.button("Cadastrar Produto"):
    # Validação inicial dos campos obrigatórios
    if not product_name or not description or price is None:
        st.warning("Por favor, preencha todos os campos obrigatórios (Nome, Descrição, Preço).")
    else:
        image_url = ""
        # Processa o upload da imagem se um arquivo foi fornecido
        if uploaded_file is not None:
            image_url = upload_image_to_blob(uploaded_file)
            if not image_url: # Se o upload da imagem falhou, interrompe o processo
                st.error("Falha ao carregar a imagem. O produto não será cadastrado.")
                st.stop() # Interrompe a execução do script Streamlit

        # Monta os dados do produto para inserção
        product_data = {
            "nome": product_name,
            "descricao": description,
            "preco": price,
            "imagem_url": image_url
        }

        # Tenta inserir os dados no Azure SQL Server
        if insert_product_into_sql(product_data):
            st.success("Produto cadastrado com sucesso no Azure SQL!")
            # Atualiza a lista de produtos na tela após o cadastro
            display_product_list()
        else:
            st.error("Houve um problema ao cadastrar o produto no Azure SQL.")

        # --- Bloco Opcional: Salvamento Local em JSON (para referência/depuração) ---
        # Este bloco é um exemplo de como os dados poderiam ser salvos localmente.
        # Em uma aplicação real, a persistência primária seria o banco de dados.
        file_path = "produtos.json"
        produtos = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    produtos = json.load(f)
                except json.JSONDecodeError:
                    # Caso o arquivo esteja corrompido ou vazio, inicia com uma lista vazia
                    produtos = []
        
        produtos.append(product_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=4)
        
        st.json(product_data) # Exibe os dados do produto em formato JSON no Streamlit

# --- Seção para Listagem de Produtos ---
st.markdown("---") # Separador visual

# Botão para carregar e exibir a lista de produtos a qualquer momento
if st.button("Atualizar Lista de Produtos"):
    display_product_list()

# Exibe a lista de produtos ao iniciar a aplicação ou após um cadastro bem-sucedido
# Isso garante que a lista esteja visível por padrão
display_product_list()