from azure.storage.blob import BlobServiceClient
import uuid
import streamlit as st
from settings import BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME, BLOB_ACCOUNT_NAME


def upload_image_to_blob(file_obj):
    """
    Faz o upload de um arquivo de imagem para o Azure Blob Storage.

    Args:
        file_obj: O objeto de arquivo carregado via st.file_uploader.

    Returns:
        str: A URL pública da imagem no Blob Storage, ou None em caso de erro.
    """
    try:
        # Inicializa o cliente de serviço Blob
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

        # Gera um nome único para o blob (imagem) para evitar colisões
        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)

        # Faz o upload do conteúdo do arquivo
        blob_client.upload_blob(file_obj.read(), overwrite=True)

        # Constrói e retorna a URL pública da imagem
        image_url = f"https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_CONTAINER_NAME}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao enviar imagem para o Azure Blob Storage: {e}")
        return None