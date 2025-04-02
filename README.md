# Generador de Chistes con LangChain y Ollama

Un simple proyecto de Python que utiliza LangChain y Ollama para generar chistes sobre temas específicos utilizando el modelo deepseek-r1:8b.

## Requisitos Previos

- Python 3.10 o superior
- [Ollama](https://ollama.ai/) instalado en tu sistema

## Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Descarga el modelo deepseek-r1:8b usando Ollama:
   ```
   ollama pull deepseek-r1:8b
   ```
   Nota: Este paso puede tardar varios minutos dependiendo de tu conexión a internet.

## Uso

### Modo Interactivo

1. Ejecuta el script principal:
   ```
   python main.py
   ```

2. Cuando se te solicite, ingresa un tema para el chiste.

3. El programa generará un chiste sobre el tema proporcionado utilizando el modelo deepseek-r1:8b.

### Modo Directo

También puedes usar el script de ejemplo que genera chistes sobre temas predefinidos:

```
python ejemplo_directo.py
```

Este script muestra cómo usar el prompt template programáticamente con temas predefinidos, lo que es útil si quieres integrar esta funcionalidad en otras aplicaciones.

### Uso Avanzado con Chains

Para ver un ejemplo más avanzado que utiliza LangChain chains:

```
python ejemplo_chain.py
```

Este ejemplo demuestra cómo integrar el prompt template en una cadena de LangChain, lo que permite construir aplicaciones más complejas y flujos de trabajo más sofisticados.

## Ejemplo

```
$ python main.py
Initializing Ollama with deepseek-r1:8b model...
Ingresa un tema para el chiste: programación

Generando chiste sobre programación ...

¿Por qué los programadores prefieren el invierno? 
Porque pueden usar buffers sin que nadie les diga nada.
```

## Personalización

Puedes modificar el prompt template en `main.py` para cambiar el tipo de chistes que se generan o para solicitar otro tipo de contenido al modelo.
