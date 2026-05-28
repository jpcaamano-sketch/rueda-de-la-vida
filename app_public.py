"""
app_public.py — Formulario público de la Rueda de la Vida
Puerto: 8532

Sin token  → Landing page (nombre + email)
Con ?token → Formulario de evaluación (24 comportamientos)
"""

import streamlit as st
from core.styles     import CSS
from core.config     import BASE_URL
from core.database   import (
    crear_participante, get_participante_por_token,
    guardar_respuestas, marcar_completado,
)
from core.dimensions import DIMENSIONES, get_comportamientos_informe, calcular_puntajes
from core.email_service import enviar_invitacion, enviar_informe
from core.report     import generar_informe_completo

st.set_page_config(
    page_title="Rueda de la Vida",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
.stApp { background: #4E32AD !important; }
.block-container { font-family: 'Inter', sans-serif !important; }
.stButton > button {
  background: #FF6B4E !important;
  color: #fff !important;
  border: none !important;
  border-radius: 28px !important;
  font-weight: 500 !important;
  box-shadow: none !important;
  transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.9 !important; transform: none !important; box-shadow: none !important; }
div[data-testid="stTextInput"] input {
  background: rgba(255,255,255,0.92) !important;
  color: #1a1a2e !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 8px !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #999 !important; }
div[data-testid="stTextInput"] label p { color: rgba(255,255,255,0.75) !important; }
div[data-testid="stFormSubmitButton"] button {
  background: #FF6B4E !important; border-radius: 28px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Router por token ─────────────────────────────────────────────────────
token = st.query_params.get("token", None)

# ═════════════════════════════════════════════════════════════════════════
# LANDING — sin token
# ═════════════════════════════════════════════════════════════════════════
if not token:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
      <div style="font-size:48px;margin-bottom:10px;">🧭</div>
      <h1 style="color:#DCFE77;font-size:26px;margin:0;">Rueda de la Vida</h1>
      <p style="color:rgba(255,255,255,0.65);font-size:15px;margin-top:8px;">
        Diagnóstico personal en 8 dimensiones clave
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:16px 20px;margin-bottom:20px;font-size:14px;color:rgba(255,255,255,0.75);line-height:1.6;border:1px solid rgba(255,255,255,0.12);">
      Evaluarás <strong style="color:#fff;">24 comportamientos</strong> distribuidos en 8 áreas de tu vida:
      trabajo, salud, finanzas, familia, amistades, desarrollo personal, ocio y propósito.<br/><br/>
      Al finalizar recibirás por correo un <strong style="color:#fff;">informe personalizado</strong> con gráfico radar,
      análisis de IA y prácticas concretas para las áreas de menor puntaje.<br/>
      <em>El proceso toma aproximadamente 10 minutos.</em>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_landing"):
        nombre = st.text_input("Tu nombre completo", placeholder="Juan Pérez")
        email  = st.text_input("Tu correo electrónico", placeholder="juan@email.com")
        submit = st.form_submit_button("Comenzar mi evaluación →")

    if submit:
        nombre = nombre.strip()
        email  = email.strip().lower()

        if not nombre or not email:
            st.error("Por favor ingresa tu nombre y correo.")
            st.stop()
        if "@" not in email or "." not in email:
            st.error("Ingresa un correo válido.")
            st.stop()

        # Crear nuevo participante y enviar invitación
        with st.spinner("Enviando tu enlace de acceso..."):
            p    = crear_participante(nombre, email)
            link = f"{BASE_URL}/?token={p['token']}"
            try:
                enviar_invitacion(nombre, email, link)
                st.success(f"¡Listo, {nombre}! Revisa tu correo y sigue el enlace para comenzar.")
            except Exception as e:
                st.error(f"Hubo un error al enviar el correo: {e}")
                st.info(f"Usa este enlace directo: {link}")

    st.stop()


# ═════════════════════════════════════════════════════════════════════════
# EVALUACIÓN — con token
# ═════════════════════════════════════════════════════════════════════════
participante = get_participante_por_token(token)

if not participante:
    st.error("El enlace no es válido o ha expirado.")
    st.stop()

nombre = participante["nombre"]

# ── CSS adicional para la tabla ───────────────────────────────────────────
st.markdown("""
<style>
  .block-container { max-width: 1100px !important; padding-top: 1.2rem !important; }
  /* Texto general sobre fondo púrpura */
  .stApp p, .stApp label, .stApp span,
  .stApp [data-testid="stMarkdownContainer"] p { color: rgba(255,255,255,0.88) !important; }

  /* Spinner */
  .stSpinner p { color: rgba(255,255,255,0.75) !important; }

  /* Mensajes de error / éxito / info */
  .stAlert p { color: #1a1a2e !important; }

  /* Encabezado de tabla */
  .th-cell {
    background: #FF6B4E; color: #fff !important; font-weight: 700; font-size: 13px;
    padding: 10px 12px; border-radius: 0;
  }
  .dim-sep {
    padding: 8px 12px; font-weight: 700; font-size: 13px;
    color: #fff !important; border-radius: 4px; margin: 6px 0 2px;
  }

  /* Filas de descripción */
  .fila-desc {
    padding: 10px 10px; font-size: 15px;
    color: rgba(255,255,255,0.88) !important;
    border-bottom: 1px solid rgba(255,255,255,0.08); line-height: 1.6;
  }

  /* Inputs numéricos */
  div[data-testid="stNumberInput"] input {
    text-align: center !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    background: rgba(255,255,255,0.92) !important;
    color: #1a1a2e !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
  }

  /* Alineación vertical descripción ↔ input */
  [data-testid="stForm"] [data-testid="stColumn"] > div {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    height: 100% !important;
  }

  /* Título resumen */
  .stApp h3 { color: #DCFE77 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0 14px;border-bottom:1px solid rgba(255,255,255,0.12);margin-bottom:20px;">
  <span style="font-size:15px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:#fff;">Juan Pablo Caamaño</span>
  <a href="https://instagram.com/jpe.coachdevida" style="font-size:13px;color:#DCFE77;text-decoration:none;">@jpe.coachdevida</a>
</div>
<div style="text-align:center;padding:4px 0 14px;">
  <span style="font-size:28px;">🧭</span>
  <h1 style="color:#DCFE77;font-size:21px;margin:4px 0 2px;">Rueda de la Vida</h1>
  <p style="color:rgba(255,255,255,0.65);font-size:14px;margin:0;">
    Hola <strong style="color:#fff;">{nombre}</strong> · Asigna una nota del <strong style="color:#fff;">1 al 10</strong> a cada comportamiento
  </p>
</div>
<div style="background:rgba(255,107,78,0.15);border-radius:8px;padding:10px 16px;margin-bottom:14px;font-size:13px;color:rgba(255,255,255,0.85);border:1px solid rgba(255,107,78,0.3);">
  <strong style="color:#FF6B4E;">Instrucción:</strong> Evalúa qué tan presente está cada comportamiento en tu vida real hoy
  (no cómo te gustaría que estuviera). &nbsp;1 = casi nunca &nbsp;·&nbsp; 10 = de manera consistente.
</div>
""", unsafe_allow_html=True)

# ── Formulario de evaluación ──────────────────────────────────────────────
comportamientos = get_comportamientos_informe()
respuestas      = {}

with st.form("form_evaluacion"):
    # Header dentro del form para que las columnas cuadren
    h1, h2 = st.columns([7, 1])
    h1.markdown('<div class="th-cell">Descripción</div>', unsafe_allow_html=True)
    h2.markdown('<div class="th-cell" style="text-align:center;">Nota</div>', unsafe_allow_html=True)

    for num, comp in enumerate(comportamientos, start=1):
        c1, c2 = st.columns([7, 1])

        with c1:
            st.markdown(
                f'<div class="fila-desc">'
                f'{num}. {comp["descripcion"]}</div>',
                unsafe_allow_html=True,
            )

        with c2:
            val = st.number_input(
                label="nota",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key=f"n_{comp['id']}",
                label_visibility="collapsed",
            )
        respuestas[comp["id"]] = int(val)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    enviar = st.form_submit_button(
        "Enviar mi evaluación y recibir informe →",
        use_container_width=True,
    )

# ── JS: select-all al foco + auto-avance entre casillas ──────────────────
import streamlit.components.v1 as components
components.html("""
<script>
function getInputs() {
    return Array.from(
        window.parent.document.querySelectorAll(
            '[data-testid="stForm"] [data-testid="stNumberInput"] input'
        )
    );
}

function setupInputs() {
    var inputs = getInputs();
    inputs.forEach(function(inp, i) {
        if (inp._jpeReady) return;
        inp._jpeReady = true;

        // Seleccionar todo al entrar al campo
        inp.addEventListener('focus', function() { this.select(); });

        var timer = null;
        inp.addEventListener('keyup', function(e) {
            var v = parseInt(this.value);
            if (isNaN(v) || v < 1 || v > 10) return;
            clearTimeout(timer);

            if (v === 10 || (v >= 2 && v <= 9)) {
                // Avanzar de inmediato
                var next = getInputs()[i + 1];
                if (next) { next.focus(); next.select(); }
            } else if (v === 1) {
                // Esperar 500 ms por si viene el "0" (para hacer 10)
                timer = setTimeout(function() {
                    var next = getInputs()[i + 1];
                    if (next) { next.focus(); next.select(); }
                }, 500);
            }
        });
    });
}

// Ejecutar ahora y re-ejecutar cuando Streamlit re-renderice
setupInputs();
setTimeout(setupInputs, 600);
setTimeout(setupInputs, 1500);
new MutationObserver(setupInputs).observe(
    window.parent.document.body, { childList: true, subtree: true }
);
</script>
""", height=0)

# ── Procesar envío ────────────────────────────────────────────────────────
if enviar:
    sin_responder = [c["nombre"] for c in comportamientos if respuestas.get(c["id"], 0) == 0]
    if sin_responder:
        st.error(f"Faltan {len(sin_responder)} comportamiento(s) por evaluar. Ingresa un valor entre 1 y 10 en cada fila.")
        st.stop()

    with st.spinner("Calculando resultados y generando tu informe con IA... (puede tomar 30 segundos)"):
        try:
            # 1. Guardar respuestas
            guardar_respuestas(participante["id"], respuestas)

            # 2. Calcular puntajes por dimensión
            puntajes = calcular_puntajes(respuestas)

            # 3. Generar informe completo (gráfico + IA + HTML + PDF)
            html_informe, barra_b64, pdf_bytes = generar_informe_completo(nombre, puntajes)

            # 4. Enviar informe por email con PDF adjunto
            enviar_informe(nombre, participante["email"], html_informe, pdf_bytes)

            # 5. Marcar como completado
            marcar_completado(participante["id"])

            st.success(f"¡Listo! Tu informe fue enviado a {participante['email']}.")
            st.balloons()

            # Mostrar resumen como gráfico de barras
            st.markdown("### Resumen de tus puntajes")
            st.image(f"data:image/png;base64,{barra_b64}", use_container_width=False, width=600)

            st.markdown("""
            <div style="text-align:center;margin-top:16px;color:rgba(255,255,255,0.55);font-size:13px;">
              Revisa tu bandeja de entrada · el informe detallado llega en minutos.
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al procesar: {e}")
            raise
