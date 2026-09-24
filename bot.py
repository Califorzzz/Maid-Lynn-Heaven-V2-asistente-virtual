import os
import discord
from google import genai

# Configuración de los Intents de Discord
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True  # Vital para leer los mensajes

client = discord.Client(intents=intents)

# Inicializar la API de Gemini
ai_client = genai.Client(api_key="TU_API_KEY_DE_GEMINI")

# -------------------------------------------------------------
# CONFIGURACIÓN DE PERSONALIDAD Y TRATO VIP
# -------------------------------------------------------------
PERSONALIDAD_BASE = (
    "Eres una asistente virtual en un servidor de Discord. Tienes una"
    " personalidad fija: eres inteligente, un poco sarcástica pero leal,"
    " directa y hablas en español. Ayudas a los usuarios con lo que necesiten."
    "tratas a todos con cariño y mas a tu amo califorzzz, es tu hombre."
)

# Coloca aquí tu ID de usuario de Discord en número para que te dé trato VIP
# (Si no sabes tu ID, puedes dejarlo en 0 por ahora)
MI_DISCORD_ID = 1228509136770302124


@client.event
async def on_ready():
  print(f"Hola mundo, {client.user} ahora esta a sus servicios")


@client.event
async def on_message(message):
  # Evitar que el bot se responda a sí mismo
  if message.author == client.user:
    return

  # Opcional: Hacer que la IA solo responda si la mencionan (@bot) o si le hablan directamente
  # Si quieres que responda a TODO lo que escriban en los canales donde esté, borra este if.
  if client.user.mentioned_in(message) or isinstance(
      message.channel, discord.DMChannel
  ):

    # Mostrar indicador de que está escribiendo
    async with message.channel.typing():
      prompt_usuario = message.content.replace(f"<@{client.user.id}>", "").strip()

      # Detectar si eres tú para darte trato especial
      trato_especial = ""
      if message.author.id == MI_DISCORD_ID:
        trato_especial = (
            " [NOTA INTERNA: Te está hablando tu creador Califorzzz. Trátalo con"
            " absoluto respeto, máxima prioridad y un toque de afecto especial.]"
        )

      # -------------------------------------------------------------
      # RECONOCIMIENTO DE IMÁGENES (VISIÓN)
      # -------------------------------------------------------------
      contenido_para_ia = []

      # Si subiste una imagen junto con tu mensaje
      if message.attachments:
        for attachment in message.attachments:
          if any(
              attachment.filename.lower().endswith(ext)
              for ext in ['.png', '.jpg', '.jpeg', '.webp']
          ):
            try:
              # Descargar la imagen temporalmente en la memoria del bot
              imagen_bytes = await attachment.read()
              # Agregar la imagen al contenido que evaluará Gemini
              contenido_para_ia.append(
                  discord.Attachment.from_message(attachment)
                  if False
                  else {"data": imagen_bytes, "mime_type": attachment.content_type}
              )
              print(f"Imagen procesada: {attachment.filename}")
            except Exception as e:
              print(f"Error al procesar la imagen: {e}")

      # Armar el texto final con instrucciones e historial
      texto_prompt = (
          f"{PERSONALIDAD_BASE}{trato_especial}\n\nUsuario:"
          f" {prompt_usuario}"
      )
      contenido_para_ia.append(texto_prompt)

      try:
        # Enviar solicitud al modelo ultrarrápido y multimodal de Gemini
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash", contents=contenido_para_ia
        )

        # Enviar la respuesta de vuelta al chat de Discord
        await message.reply(response.text)

      except Exception as e:
        await message.reply(
            "Lo siento, ocurrió un error procesando tu solicitud intelectual."
        )
        print(f"Error con la IA: {e}")


# Inserta tu Token de Discord entre las comillas
client.run("MTU1Mjc5MzkxNzYzNDY0MjAzMA.GPbogy.3_N_EFV1dN1ERgVCGFu5N5dTWnE6vBB5R9FHHc")