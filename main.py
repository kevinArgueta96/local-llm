#!/usr/bin/env python3
"""
Simple LangChain application that uses Ollama for chat interactions
and vector database for semantic search.
"""
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from ingestion import TextIngestion
import os

def ask_question(llm, filter_llm, ingestion, vectorstore=None):
    """
    Función para realizar preguntas al modelo con búsqueda semántica previa.
    """
    # Obtener la pregunta del usuario
    question = input("Ingresa su pregunta: ")
    
    # Verificar si existe una base de datos vectorial para búsqueda semántica
    context = ""
    if vectorstore is not None or os.path.exists("vectorstore"):
        try:
            print("Realizando búsqueda semántica en documentos ingresados...")
            results = ingestion.semantic_search(question, vectorstore)
            print(results)
            
            if results:
                context = "Información relevante encontrada en los documentos:\n\n"
                for i, doc in enumerate(results):
                    context += f"Documento {i+1}: {doc.page_content}\n\n"
                
                print("Se encontró información relevante en los documentos ingresados.")
            else:
                print("No se encontró información relevante en los documentos ingresados.")
        except Exception as e:
            print(f"Error al realizar la búsqueda semántica: {str(e)}")
    
    # Crear un ChatPromptTemplate con roles de sistema y usuario
    system_template = """You are a helpful assistant. Answer the user's questions based on your knowledge and the provided context.
     Think to understand and provide a complete answer.
     
    <CONTEXT>
    {context}
    </CONTEXT>
        
    <RULES>
    -RETURN the answer into <ANSWER>[here]</ANSWER>
    -If context is provided, base your answer primarily on that information
    -If the context doesn't contain relevant information, use your own knowledge
    </RULES>"""
    
    chat_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{question}")
    ])
    
    # Formatear el template con la pregunta del usuario y el contexto
    messages = chat_template.format_messages(question=question, context=context)
    
    # Enviar los mensajes al modelo y obtener la respuesta
    print("Enviando consulta al modelo con el contexto relevante...")
    response = llm.invoke(messages)
    
    print("Respuesta completa del primer modelo:")
    print(response)
    print("\nFiltrando respuesta...")
    
    # Crear un template para extraer solo el contenido dentro de las etiquetas <ANSWER>
    filter_prompt = PromptTemplate.from_template(
        "FIND THE ANSWER IN THE NEXT TEXT:\n\n{response_text}\n\nExtract and return ONLY the text between <ANSWER> and </ANSWER> tags. RULES: ALWAYS RESPONSE IN SPANSIH"
    )
    
    # Formatear el prompt con la respuesta del primer modelo
    formatted_filter_prompt = filter_prompt.format(response_text=str(response))
    
    # Enviar al segundo modelo
    response_filtered = filter_llm.invoke(formatted_filter_prompt)
    
    print("\nRespuesta filtrada:")
    print(response_filtered)

def ingest_text_file(ingestion):
    """
    Función para ingerir un archivo de texto en la base de datos vectorial.
    """
    # Solicitar la ruta del archivo
    file_path = input("Ingresa la ruta del archivo de texto a ingerir: ")
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe.")
        return None
    
    try:
        # Ingerir el archivo
        print(f"Ingiriendo archivo: {file_path}")
        vectorstore = ingestion.ingest_file(file_path)
        print(f"Archivo ingresado correctamente y guardado en la base de datos vectorial.")
        return vectorstore
    except Exception as e:
        print(f"Error al ingerir el archivo: {str(e)}")
        return None

def semantic_search(ingestion, vectorstore=None):
    """
    Función para realizar una búsqueda semántica en la base de datos vectorial.
    """
    # Verificar si existe una base de datos vectorial
    if vectorstore is None and not os.path.exists("vectorstore"):
        print("Error: No hay una base de datos vectorial disponible.")
        print("Primero debes ingerir un archivo de texto.")
        return
    
    # Solicitar la consulta
    query = input("Ingresa tu consulta para la búsqueda semántica: ")
    
    try:
        # Realizar la búsqueda
        print(f"Realizando búsqueda semántica para: '{query}'")
        results = ingestion.semantic_search(query, vectorstore)
        
        # Mostrar resultados
        print("\nResultados:")
        for i, doc in enumerate(results):
            print(f"\n--- Resultado {i+1} ---")
            print(doc.page_content)
    except Exception as e:
        print(f"Error al realizar la búsqueda: {str(e)}")

def main():
    """
    Main function to run the application.
    """
    # Initialize the Ollama models
    print("Initializing Ollama models...")
    llm = OllamaLLM(model="deepseek-r1:8b")
    filter_llm = OllamaLLM(model="gemma3:1b")
    
    # Initialize the TextIngestion class
    ingestion = TextIngestion(embedding_model="deepseek-r1:8b")
    
    # Variable para almacenar la base de datos vectorial
    vectorstore = None
    
    # Cargar la base de datos vectorial si existe
    if os.path.exists("vectorstore"):
        try:
            vectorstore = ingestion.load_vectorstore()
            print("Base de datos vectorial cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la base de datos vectorial: {str(e)}")
    
    # Bucle principal
    while True:
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL")
        print("="*50)
        print("1. Realizar una pregunta al modelo")
        print("2. Ingerir un archivo de texto")
        print("3. Realizar una búsqueda semántica")
        print("4. Salir")
        
        # Obtener la opción del usuario
        option = input("\nSelecciona una opción (1-4): ").strip()
        
        if option == "1":
            ask_question(llm, filter_llm, ingestion, vectorstore)
        elif option == "2":
            vectorstore = ingest_text_file(ingestion)
        elif option == "3":
            semantic_search(ingestion, vectorstore)
        elif option == "4" or option.lower() == "salir":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 4.")

if __name__ == "__main__":
    main()
