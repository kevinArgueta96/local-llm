# Asistente con búsqueda semántica usando LangChain y Ollama

Un proyecto de Python que utiliza LangChain y Ollama para crear un asistente conversacional con capacidad de búsqueda semántica. El sistema usa el modelo deepseek-r1:8b para generar respuestas y gemma3:1b para filtrar y formatear el contenido.

## Requisitos Previos

- Python 3.10 o superior
- [Ollama](https://ollama.ai/) instalado en tu sistema

## Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Descarga los modelos necesarios usando Ollama:
   ```
   ollama pull deepseek-r1:8b
   ollama pull gemma3:1b
   ```
   Nota: Este paso puede tardar varios minutos dependiendo de tu conexión a internet.

## Uso

### Modo Interactivo con Menú

1. Ejecuta el script principal:
   ```
   python main.py
   ```

2. Selecciona una de las siguientes opciones:
   - **Opción 1**: Realizar una pregunta al modelo (utiliza búsqueda semántica para encontrar contexto relevante)
   - **Opción 2**: Ingerir un archivo de texto en la base de datos vectorial
   - **Opción 3**: Realizar una búsqueda semántica directa
   - **Opción 4**: Salir

### Búsqueda Semántica

La aplicación permite cargar archivos de texto en una base de datos vectorial FAISS para realizar búsquedas semánticas:

1. Selecciona la opción 2 para ingerir un archivo de texto
2. Proporciona la ruta del archivo cuando se te solicite
3. El archivo se procesará y se almacenará en la base de datos vectorial

Una vez que hayas ingresado archivos, puedes:
- Usar la opción 1 para hacer preguntas al modelo, que automáticamente buscará información relevante en los documentos ingresados
- Usar la opción 3 para realizar búsquedas semánticas directas sin utilizar el modelo de lenguaje

## Modelos utilizados

### DeepSeek (deepseek-r1:8b)
- Usado como modelo principal para generar respuestas
- También se utiliza para generar embeddings para la búsqueda semántica
- Proporciona respuestas de alta calidad basadas en el contexto proporcionado

### Gemma (gemma3:1b)
- Modelo más ligero utilizado para filtrar y formatear las respuestas
- Extrae el contenido relevante de las respuestas de DeepSeek
- Asegura que las respuestas tengan el formato adecuado en español

## Archivos principales

- **main.py**: Script principal con menú interactivo y funcionalidad del asistente
- **ingestion.py**: Módulo para gestionar la ingesta de archivos y búsqueda semántica

## Ejemplo de uso

```
$ python main.py
Initializing Ollama models...
Base de datos vectorial cargada correctamente.

==================================================
MENÚ PRINCIPAL
==================================================
1. Realizar una pregunta al modelo
2. Ingerir un archivo de texto
3. Realizar una búsqueda semántica
4. Salir

Selecciona una opción (1-4): 1
Ingresa su pregunta: ¿Quién es Esme La Chapina?
Realizando búsqueda semántica en documentos ingresados...
Se encontró información relevante en los documentos ingresados.
Enviando consulta al modelo con el contexto relevante...
Respuesta completa del primer modelo:

Filtrando respuesta...

Respuesta filtrada:
<ANSWER>Esme La Chapina es un personaje creado por Esmeralda Sabrina, una joven de 23 años originaria de Chiquimulilla, Santa Rosa. Según la información proporcionada, Esmeralda salió de su lugar de origen a los 14 años para iniciar su vida como emprendedora. Ha tenido diferentes ocupaciones y viajaba desde Santa Rosa a la capital en busca de mercadería. Es una mujer independiente que ha luchado por salir adelante y ha superado grandes pruebas en su vida.</ANSWER>
```

## Personalización

Puedes modificar los siguientes aspectos:

1. **Parámetros de Ingesta**: En `ingestion.py` puedes ajustar el tamaño de los fragmentos y la superposición
2. **Prompts**: En `main.py` puedes modificar las plantillas de prompts para adaptarlas a tus necesidades
3. **Modelos**: Puedes cambiar los modelos de Ollama utilizados (requiere modificar el código y tener los modelos instalados)

## Uso en Raspberry Pi

Este sistema está diseñado para funcionar en dispositivos con recursos limitados como una Raspberry Pi:
- Utiliza FAISS como base de datos vectorial local, eficiente en memoria
- Los embeddings se generan localmente usando Ollama
- Todo el procesamiento es local, sin dependencias de servicios en la nube
