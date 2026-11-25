import os
import random
from PIL import Image
import streamlit as st

CARPETA_CARTAS = "cartas"
ARCHIVO_CASOS = "casos.txt"
PROBABILIDAD_INVERSA = 0.35  # 35% de probabilidad de salir al revés

# Configuración de la página web
st.set_page_config(page_title="Tarot Web", page_icon="🔮", layout="wide")

st.title("🔮 Tirada de Tarot en Línea")

# Verifica que exista la carpeta de cartas
if not os.path.exists(CARPETA_CARTAS):
  st.error(
      f"No se encontró la carpeta '{CARPETA_CARTAS}'. Créala junto a este"
      " archivo."
  )
  st.stop()

archivos = [
    f
    for f in os.listdir(CARPETA_CARTAS)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

if not archivos:
  st.warning(f"La carpeta '{CARPETA_CARTAS}' está vacía. Agrega imágenes.")
  st.stop()

# Opción de Casos Hipotéticos
usar_casos = st.checkbox("📖 Practicar con un caso hipotético al azar")

# Controles principales
col_input, col_boton = st.columns(2)

with col_input:
  cantidad = st.number_input(
      "¿Cuántas cartas quieres lanzar?",
      min_value=1,
      max_value=len(archivos),
      value=min(3, len(archivos)),
      step=1,
  )

with col_boton:
  st.write("")
  st.write("")
  lanzar = st.button(
      "✨ Lanzar Cartas", type="primary", use_container_width=True
  )

# Lógica al presionar el botón
if lanzar:
  st.divider()

  # Si el usuario activó los casos de práctica, lee casos.txt soportando tildes y ñ
  if usar_casos:
    if os.path.exists(ARCHIVO_CASOS):
      try:
        with open(ARCHIVO_CASOS, "r", encoding="utf-8") as f:
          lista_casos = [linea.strip() for linea in f if linea.strip()]
      except UnicodeDecodeError:
        with open(ARCHIVO_CASOS, "r", encoding="latin-1") as f:
          lista_casos = [linea.strip() for linea in f if linea.strip()]

      if lista_casos:
        caso_elegido = random.choice(lista_casos)
        st.info(f"**Caso para practicar:**\n\n{caso_elegido}")
      else:
        st.warning(f"El archivo '{ARCHIVO_CASOS}' está vacío.")
    else:
      st.warning(
          f"No se encontró el archivo '{ARCHIVO_CASOS}' en el repositorio."
      )

  # 1. Sin repeticiones
  cartas_elegidas = random.sample(archivos, cantidad)

  # Muestra las cartas en filas de 5 columnas
  columnas_por_fila = 5

  for i in range(0, cantidad, columnas_por_fila):
    cols = st.columns(columnas_por_fila)
    bloque_cartas = cartas_elegidas[i : i + columnas_por_fila]

    for idx, archivo in enumerate(bloque_cartas):
      # 2. 35% de probabilidad de salir inversa
      es_inversa = random.random() < PROBABILIDAD_INVERSA

      ruta = os.path.join(CARPETA_CARTAS, archivo)
      img = Image.open(ruta)

      if es_inversa:
        img = img.rotate(180)
        estado = "🔄 Inversa"
      else:
        estado = "⬆️ Derecha"

      nombre = os.path.splitext(archivo)[0].replace("_", " ").title()
      numero_carta = i + idx + 1

      with cols[idx]:
        st.image(img, use_container_width=True)
        st.markdown(f"**{numero_carta}. {nombre}**")
        st.caption(estado)
