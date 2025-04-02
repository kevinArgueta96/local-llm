#!/usr/bin/env python3
"""
Módulo para la ingesta de archivos de texto en una base de datos vectorial FAISS
para realizar búsquedas semánticas utilizando embeddings de Ollama.
"""
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
import os

class TextIngestion:
    """
    Clase para manejar la ingesta de archivos de texto en una base de datos vectorial.
    """
    def __init__(self, embedding_model="deepseek-r1:8b"):
        """
        Inicializa el sistema de ingesta con un modelo de embeddings específico.
        
        Args:
            embedding_model (str): Nombre del modelo de Ollama a utilizar para embeddings
        """
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    def ingest_file(self, file_path, db_save_path="vectorstore"):
        """
        Ingiere un archivo de texto y lo almacena en una base de datos vectorial.
        
        Args:
            file_path (str): Ruta al archivo de texto a ingerir
            db_save_path (str): Ruta donde guardar la base de datos vectorial
            
        Returns:
            FAISS: Instancia de la base de datos vectorial
        """
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
            
        # Cargar el documento
        loader = TextLoader(file_path)
        documents = loader.load()
        
        # Dividir el texto en fragmentos
        splits = self.text_splitter.split_documents(documents)
        
        # Crear la base de datos vectorial
        vectorstore = FAISS.from_documents(splits, self.embeddings)
        
        # Guardar la base de datos para uso futuro
        vectorstore.save_local(db_save_path)
        
        return vectorstore
    
    def load_vectorstore(self, db_path="vectorstore"):
        """
        Carga una base de datos vectorial existente.
        
        Args:
            db_path (str): Ruta a la base de datos vectorial
            
        Returns:
            FAISS: Instancia de la base de datos vectorial
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"La base de datos {db_path} no existe")
            
        return FAISS.load_local(db_path, self.embeddings, allow_dangerous_deserialization=True)
    
    def semantic_search(self, query, vectorstore=None, db_path="vectorstore", k=3):
        """
        Realiza una búsqueda semántica en la base de datos vectorial.
        
        Args:
            query (str): Consulta para la búsqueda
            vectorstore (FAISS, optional): Base de datos vectorial
            db_path (str): Ruta a la base de datos vectorial si vectorstore es None
            k (int): Número de resultados a devolver
            
        Returns:
            list: Lista de documentos relevantes
        """
        if vectorstore is None:
            vectorstore = self.load_vectorstore(db_path)
            
        try:
            return vectorstore.similarity_search(query, k=k)
        except Exception as e:
            print(f"Error en búsqueda semántica: {str(e)}")
            return []

def main():
    """
    Función principal para demostrar el uso de la clase TextIngestion.
    """
    # Ejemplo de uso
    ingestion = TextIngestion()
    
    # Ruta al archivo de texto a ingerir
    file_path = "ingestion_information.txt"
    
    # Ingerir el archivo
    print(f"Ingiriendo archivo: {file_path}")
    vectorstore = ingestion.ingest_file(file_path)
    
    # Realizar una búsqueda semántica
    query = "¿Quién es Esme La Chapina?"
    print(f"\nRealizando búsqueda semántica para: '{query}'")
    results = ingestion.semantic_search(query, vectorstore)
    
    # Mostrar resultados
    print("\nResultados:")
    for i, doc in enumerate(results):
        print(f"\n--- Resultado {i+1} ---")
        print(doc.page_content)

if __name__ == "__main__":
    main()
