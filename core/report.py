"""
Generación del informe:
  1. Gráfico de barras horizontales (matplotlib)
  2. Análisis IA con Gemini
  3. HTML del email
"""

import io
import base64
import json
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from google import genai

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable, PageBreak,
)

from core.config import GOOGLE_API_KEY
from core.dimensions import DIMENSIONES, get_comportamientos_formulario

_gemini = genai.Client(api_key=GOOGLE_API_KEY)


# ─── Gráfico de barras horizontales ──────────────────────────────────────

def generar_barra(puntajes: dict) -> str:
    """
    puntajes: {dim_id: {"nombre": ..., "promedio": ..., "color": ..., "icono": ...}}
    Retorna imagen PNG en base64.
    """
    dims    = [puntajes[d["id"]] for d in DIMENSIONES]
    nombres = [f"{d['icono']}  {d['nombre']}" for d in dims]
    valores = [d["promedio"] for d in dims]
    colores = [d["color"]    for d in dims]

    fig, ax = plt.subplots(figsize=(8, 5.5))
    fig.patch.set_facecolor("#f8f9fa")
    ax.set_facecolor("#f8f9fa")

    y = list(range(len(nombres)))

    # Barra de fondo (hasta 10)
    ax.barh(y, [10] * len(nombres), color="#e9ecef", height=0.62, zorder=2)
    # Barras de datos
    bars = ax.barh(y, valores, color=colores, height=0.62, zorder=3)

    # Valor al final de cada barra
    for i, val in enumerate(valores):
        ax.text(val + 0.15, i, f"{val:.1f}",
                va="center", ha="left",
                fontsize=10, fontweight="bold", color=colores[i], zorder=4)

    # Líneas de referencia verticales
    for x in [2, 4, 6, 8, 10]:
        ax.axvline(x, color="#ccc", linewidth=0.6, linestyle="--", zorder=1)

    ax.set_yticks(y)
    ax.set_yticklabels(nombres, fontsize=10, color="#333")
    ax.set_xlim(0, 12)
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xticklabels(["0", "2", "4", "6", "8", "10"], fontsize=9, color="#888")
    ax.set_xlabel("Puntaje (1–10)", fontsize=10, color="#888", labelpad=8)
    ax.set_title("Diagnóstico — Rueda de la Vida",
                 fontsize=13, fontweight="bold", color="#1a3a5c", pad=14)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


# ─── Análisis IA con Gemini ───────────────────────────────────────────────

def generar_analisis(nombre: str, puntajes: dict) -> dict:
    """
    Llama a Gemini y retorna dict con:
      - general: str
      - por_dimension: {nombre_dim: str}
      - practicas: [{dimension, score, practica_1, practica_2}]  ← 3 más bajas
    """
    # Construir resumen de resultados
    lineas_dims = []
    for dim in DIMENSIONES:
        d = puntajes[dim["id"]]
        comportamientos = "\n".join(
            f"      • {c['nombre']}: {c['puntaje']}/10"
            for c in d["detalle"]
        )
        lineas_dims.append(
            f"  {dim['icono']} {d['nombre']}: {d['promedio']}/10\n{comportamientos}"
        )
    resumen = "\n".join(lineas_dims)

    # 3 dimensiones más bajas
    bottom3 = sorted(puntajes.values(), key=lambda x: x["promedio"])[:3]
    bottom3_str = ", ".join(f"{d['nombre']} ({d['promedio']}/10)" for d in bottom3)

    prompt = f"""Eres un coach experto en desarrollo personal. Analiza los resultados de la Rueda de la Vida de {nombre}.

RESULTADOS:
{resumen}

Las 3 dimensiones más bajas son: {bottom3_str}

Responde ÚNICAMENTE con un JSON válido con esta estructura exacta (sin markdown, sin texto antes ni después):
{{
  "general": "Análisis general de 3-4 párrafos. Habla directamente a {nombre} en segunda persona. Tono empático y constructivo. Identifica patrones, fortalezas y áreas de atención.",
  "por_dimension": {{
    "Trabajo y carrera": "2-3 oraciones interpretando el puntaje y el patrón de comportamientos.",
    "Salud y energía": "...",
    "Dinero y finanzas": "...",
    "Familia y pareja": "...",
    "Amistades y vida social": "...",
    "Desarrollo personal": "...",
    "Ocio y disfrute": "...",
    "Propósito y sentido": "..."
  }},
  "practicas": [
    {{
      "dimension": "nombre exacto de la dimensión más baja",
      "score": 0.0,
      "practica_1": "Título de la práctica: descripción breve y concreta de cómo realizarla. Sin asteriscos, sin guiones, solo texto plano.",
      "practica_2": "Título de la otra práctica: descripción breve y concreta. Sin asteriscos, sin guiones, solo texto plano."
    }},
    {{
      "dimension": "nombre exacto de la segunda dimensión más baja",
      "score": 0.0,
      "practica_1": "Título: descripción. Solo texto plano.",
      "practica_2": "Título: descripción. Solo texto plano."
    }},
    {{
      "dimension": "nombre exacto de la tercera dimensión más baja",
      "score": 0.0,
      "practica_1": "Título: descripción. Solo texto plano.",
      "practica_2": "Título: descripción. Solo texto plano."
    }}
  ]
}}"""

    response = _gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    texto = response.text.strip()

    # Limpiar posible markdown
    texto = re.sub(r"^```json\s*", "", texto)
    texto = re.sub(r"\s*```$",    "", texto)

    data = json.loads(texto)

    # Limpiar markdown residual en prácticas (**, *, guiones iniciales)
    def _limpiar(s: str) -> str:
        s = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", s)   # **bold** y *italic*
        s = re.sub(r"^[\-\*]\s+", "", s, flags=re.MULTILINE)  # viñetas
        s = re.sub(r"#{1,6}\s+", "", s)                 # encabezados
        return s.strip()

    for item in data.get("practicas", []):
        item["practica_1"] = _limpiar(item.get("practica_1", ""))
        item["practica_2"] = _limpiar(item.get("practica_2", ""))

    return data


# ─── HTML del email ───────────────────────────────────────────────────────

def generar_html_informe(nombre: str, puntajes: dict, analisis: dict, radar_b64: str) -> str:

    # ── Tabla de resultados (agrupada por dimensión, orden: 1.1,1.2,1.3, 2.1,2.2,2.3…) ──
    filas_tabla = ""
    for dim in DIMENSIONES:
        d = puntajes[dim["id"]]
        color = d["color"]
        prom  = d["promedio"]
        barra = int(prom * 10)

        # Fila encabezado de dimensión
        filas_tabla += f"""
        <tr style="background:#f8f9fa;">
          <td style="padding:10px 12px;font-weight:700;color:{color};font-size:15px;">
            {d['icono']} {d['nombre']}
          </td>
          <td style="padding:10px 12px;text-align:center;">
            <span style="font-weight:800;font-size:16px;color:{color};">{prom}</span>
            <span style="color:#aaa;font-size:12px;">/10</span>
            <div style="margin-top:4px;background:#e9ecef;border-radius:4px;height:6px;width:80px;display:inline-block;vertical-align:middle;margin-left:6px;">
              <div style="background:{color};width:{barra}%;height:6px;border-radius:4px;"></div>
            </div>
          </td>
        </tr>"""

        # Filas de comportamientos de esta dimensión (ordenadas por posición)
        for comp in get_comportamientos_formulario():
            if comp["dim_id"] != dim["id"]:
                continue
            puntaje = next(
                (c["puntaje"] for c in d["detalle"] if c["id"] == comp["id"]), 0
            )
            filas_tabla += f"""
            <tr>
              <td style="padding:5px 12px 5px 28px;font-size:13px;color:#555;border-bottom:1px solid #f0f0f0;">
                {comp['nombre']}
              </td>
              <td style="padding:5px 12px;text-align:center;font-weight:600;color:{color};font-size:13px;border-bottom:1px solid #f0f0f0;">
                {puntaje}/10
              </td>
            </tr>"""

    # ── Análisis por dimensión ──
    bloques_dims = ""
    for dim in DIMENSIONES:
        nombre_dim = dim["nombre"]
        texto_dim  = analisis.get("por_dimension", {}).get(nombre_dim, "")
        color      = dim["color"]
        prom       = puntajes[dim["id"]]["promedio"]
        bloques_dims += f"""
        <div style="margin-bottom:16px;padding:14px 16px;border-left:4px solid {color};background:#fafafa;border-radius:0 8px 8px 0;">
          <div style="font-weight:700;color:{color};font-size:14px;margin-bottom:6px;">
            {dim['icono']} {nombre_dim} — {prom}/10
          </div>
          <div style="color:#444;font-size:13px;line-height:1.6;">{texto_dim}</div>
        </div>"""

    # ── Prácticas de mejora (3 dimensiones más bajas) ──
    bloques_practicas = ""
    for item in analisis.get("practicas", []):
        # Buscar color de la dimensión
        color_dim = "#1a3a5c"
        icono_dim = "🎯"
        for dim in DIMENSIONES:
            if dim["nombre"] == item.get("dimension", ""):
                color_dim = dim["color"]
                icono_dim = dim["icono"]
                break

        bloques_practicas += f"""
        <div style="margin-bottom:20px;border:1px solid #e0e0e0;border-radius:10px;overflow:hidden;">
          <div style="background:{color_dim};padding:12px 16px;color:#fff;">
            <span style="font-weight:700;font-size:15px;">{icono_dim} {item.get('dimension','')} — {item.get('score','')}/10</span>
          </div>
          <div style="padding:14px 16px;background:#fff;">
            <div style="margin-bottom:10px;">
              <div style="font-weight:700;color:{color_dim};font-size:13px;margin-bottom:4px;">✅ Práctica 1</div>
              <div style="color:#444;font-size:13px;line-height:1.5;">{item.get('practica_1','')}</div>
            </div>
            <div>
              <div style="font-weight:700;color:{color_dim};font-size:13px;margin-bottom:4px;">✅ Práctica 2</div>
              <div style="color:#444;font-size:13px;line-height:1.5;">{item.get('practica_2','')}</div>
            </div>
          </div>
        </div>"""

    # Párrafos del análisis general
    parrafos_general = "".join(
        f'<p style="margin:0 0 12px 0;color:#333;font-size:14px;line-height:1.7;">{p.strip()}</p>'
        for p in analisis.get("general", "").split("\n\n")
        if p.strip()
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Tu Rueda de la Vida</title></head>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:30px 0;">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);">

  <!-- Header -->
  <tr>
    <td style="background:linear-gradient(135deg,#1a3a5c,#2980b9);padding:32px 36px;text-align:center;">
      <div style="font-size:28px;margin-bottom:8px;">🧭</div>
      <h1 style="margin:0;color:#fff;font-size:22px;font-weight:800;">Tu Rueda de la Vida</h1>
      <p style="margin:8px 0 0;color:rgba(255,255,255,0.8);font-size:14px;">Informe personal de {nombre}</p>
    </td>
  </tr>

  <!-- Gráfico de barras -->
  <tr>
    <td style="padding:28px 36px 10px;text-align:center;">
      <h2 style="margin:0 0 16px;color:#1a3a5c;font-size:17px;">Diagnóstico visual</h2>
      <img src="data:image/png;base64,{radar_b64}"
           alt="Rueda de la Vida" width="480"
           style="max-width:100%;border-radius:8px;"/>
    </td>
  </tr>

  <!-- Tabla resultados -->
  <tr>
    <td style="padding:20px 36px;">
      <h2 style="margin:0 0 14px;color:#1a3a5c;font-size:17px;">📊 Resultados por dimensión</h2>
      <table width="100%" cellpadding="0" cellspacing="0"
             style="border-collapse:collapse;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;">
        <tr style="background:#1a3a5c;">
          <th style="padding:10px 12px;color:#fff;text-align:left;font-size:13px;">Dimensión / Comportamiento</th>
          <th style="padding:10px 12px;color:#fff;text-align:center;font-size:13px;width:140px;">Puntaje</th>
        </tr>
        {filas_tabla}
      </table>
    </td>
  </tr>

  <!-- Análisis general -->
  <tr>
    <td style="padding:20px 36px;">
      <h2 style="margin:0 0 14px;color:#1a3a5c;font-size:17px;">🔍 Análisis general</h2>
      <div style="background:#f8f9fa;border-radius:8px;padding:18px 20px;">
        {parrafos_general}
      </div>
    </td>
  </tr>

  <!-- Análisis por dimensión -->
  <tr>
    <td style="padding:20px 36px;">
      <h2 style="margin:0 0 14px;color:#1a3a5c;font-size:17px;">📌 Análisis por dimensión</h2>
      {bloques_dims}
    </td>
  </tr>

  <!-- Prácticas de mejora -->
  <tr>
    <td style="padding:20px 36px 32px;">
      <h2 style="margin:0 0 6px;color:#1a3a5c;font-size:17px;">🚀 Prácticas de mejora</h2>
      <p style="margin:0 0 16px;color:#888;font-size:13px;">Para tus 3 dimensiones con menor puntaje</p>
      {bloques_practicas}
    </td>
  </tr>

  <!-- Footer -->
  <tr>
    <td style="background:#1a3a5c;padding:20px 36px;text-align:center;">
      <p style="margin:0;color:rgba(255,255,255,0.6);font-size:12px;">
        Este informe fue generado automáticamente · YoCreo Coaching
      </p>
    </td>
  </tr>

</table>
</td></tr>
</table>
</body>
</html>"""

    return html


def _strip_emoji(text: str) -> str:
    """Elimina emojis para uso en fuentes PDF que no los soportan."""
    return re.sub(
        r"[\U0001F000-\U0001FFFF\U00002600-\U000027BF\U0000FE00-\U0000FEFF]+",
        "",
        text,
    ).strip()


# ─── Gráfico radar (para PDF) ─────────────────────────────────────────────

def generar_radar(puntajes: dict) -> bytes:
    """
    Genera un gráfico radar polar con las 8 dimensiones.
    Retorna bytes PNG para embeber en el PDF.
    """
    dims        = [puntajes[d["id"]] for d in DIMENSIONES]
    nombres     = [d["nombre"]   for d in dims]
    valores     = [d["promedio"] for d in dims]
    colores_dim = [d["color"]    for d in dims]

    N = len(nombres)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    valores_plot = valores + [valores[0]]
    angles_plot  = angles  + [angles[0]]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection="polar"))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f4f2fb")

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=7, color="#aaaaaa")

    # Etiquetas abreviadas para los ejes
    etiquetas = []
    for n in nombres:
        if " y " in n:
            parts = n.split(" y ", 1)
            etiquetas.append(f"{parts[0]}\ny {parts[1]}")
        elif len(n) > 14:
            words = n.split()
            mid = max(1, len(words) // 2)
            etiquetas.append(" ".join(words[:mid]) + "\n" + " ".join(words[mid:]))
        else:
            etiquetas.append(n)

    ax.set_xticks(angles)
    ax.set_xticklabels(etiquetas, fontsize=8, color="#333333", linespacing=1.3)

    ax.fill(angles_plot, valores_plot, alpha=0.22, color="#4E32AD")
    ax.plot(angles_plot, valores_plot, color="#4E32AD", linewidth=2.2)

    for angle, val, col in zip(angles, valores, colores_dim):
        ax.scatter(angle, val, color=col, s=72, zorder=5)

    for angle, val in zip(angles, valores):
        offset = min(val + 1.05, 10.6)
        ax.annotate(
            str(val),
            xy=(angle, val),
            xytext=(angle, offset),
            ha="center", va="center",
            fontsize=9, fontweight="bold", color="#4E32AD",
        )

    ax.grid(color="#cccccc", linestyle="--", linewidth=0.5, alpha=0.8)
    ax.spines["polar"].set_color("#cccccc")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ─── PDF con reportlab ────────────────────────────────────────────────────

def generar_pdf(nombre: str, puntajes: dict, analisis: dict, radar_bytes: bytes) -> bytes:
    """
    Genera el informe completo en PDF.
    Retorna bytes del PDF.
    """
    from datetime import date

    PURPLE  = HexColor("#4E32AD")
    ORANGE  = HexColor("#FF6B4E")
    GREY    = HexColor("#888888")
    DARK    = HexColor("#1a1a2e")
    BGLIGHT = HexColor("#f4f2fb")

    W = 17.4 * cm  # ancho de contenido

    def _p(text: str, style) -> "Paragraph":
        return Paragraph(text, style)

    def _colored_block(text: str, bg: HexColor, txt_color=None) -> "Table":
        if txt_color is None:
            txt_color = colors.white
        st = ParagraphStyle(
            "cb", fontSize=11, fontName="Helvetica-Bold",
            textColor=txt_color, leading=15,
        )
        t = Table([[_p(text, st)]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), bg),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ]))
        return t

    def _body_block(text: str, bg=None) -> "Table":
        bg = bg or HexColor("#f9f9f9")
        st = ParagraphStyle(
            "bb", fontSize=10, fontName="Helvetica",
            textColor=DARK, leading=15,
        )
        t = Table([[_p(text, st)]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), bg),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ]))
        return t

    styles = getSampleStyleSheet()

    title_st = ParagraphStyle(
        "T", fontSize=22, fontName="Helvetica-Bold",
        textColor=PURPLE, alignment=TA_CENTER,
        spaceBefore=6, spaceAfter=10, leading=28,
    )
    sub_st = ParagraphStyle(
        "S", fontSize=13, fontName="Helvetica",
        textColor=GREY, alignment=TA_CENTER, spaceAfter=4,
    )
    date_st = ParagraphStyle(
        "D", fontSize=10, fontName="Helvetica",
        textColor=GREY, alignment=TA_CENTER, spaceAfter=6,
    )
    section_st = ParagraphStyle(
        "SEC", fontSize=13, fontName="Helvetica-Bold",
        textColor=PURPLE, spaceBefore=14, spaceAfter=6,
    )
    body_st = ParagraphStyle(
        "BD", fontSize=10, fontName="Helvetica",
        textColor=DARK, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=8,
    )
    small_st = ParagraphStyle(
        "SM", fontSize=9, fontName="Helvetica",
        textColor=GREY, spaceAfter=4,
    )
    footer_st = ParagraphStyle(
        "FT", fontSize=9, fontName="Helvetica",
        textColor=GREY, alignment=TA_CENTER,
    )

    # Fecha en español
    today = date.today().strftime("%d de %B de %Y")
    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre",
    }
    for en, es in meses.items():
        today = today.replace(en, es)

    story = []

    # ── Encabezado ──
    story.append(Spacer(1, 0.3 * cm))
    story.append(_p("Rueda de la Vida", title_st))
    story.append(_p(f"Informe personal de {nombre}", sub_st))
    story.append(_p(today, date_st))
    story.append(HRFlowable(width="100%", thickness=2, color=ORANGE, spaceAfter=12))

    # ── Gráfico radar ──
    story.append(_p("Diagnostico visual", section_st))
    radar_img = Image(io.BytesIO(radar_bytes), width=11 * cm, height=11 * cm)
    radar_img.hAlign = "CENTER"
    story.append(radar_img)
    story.append(Spacer(1, 0.4 * cm))

    # ── Tabla de resultados ──
    story.append(_p("Resultados por dimension", section_st))

    hdr_st = ParagraphStyle(
        "HDR", fontSize=11, fontName="Helvetica-Bold",
        textColor=colors.white, alignment=TA_CENTER,
    )
    td_name_st = ParagraphStyle(
        "TDN", fontSize=10, fontName="Helvetica", textColor=DARK,
    )

    tdata = [[_p("Dimension", hdr_st), _p("Promedio", hdr_st)]]
    for dim in DIMENSIONES:
        d = puntajes[dim["id"]]
        dim_color = HexColor(d["color"])
        score_st = ParagraphStyle(
            f"sc_{dim['id']}", fontSize=11, fontName="Helvetica-Bold",
            textColor=dim_color, alignment=TA_CENTER,
        )
        tdata.append([
            _p(_strip_emoji(f"{d['icono']} {d['nombre']}"), td_name_st),
            _p(f"{d['promedio']}/10", score_st),
        ])

    results_table = Table(tdata, colWidths=[13.4 * cm, 4 * cm])
    results_table.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  PURPLE),
        ("ALIGN",          (0, 0), (-1, 0),  "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#f4f2fb")]),
        ("GRID",           (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("TOPPADDING",     (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 8),
        ("LEFTPADDING",    (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 0.4 * cm))

    # ── Análisis general ──
    story.append(_p("Analisis general", section_st))
    for parrafo in analisis.get("general", "").split("\n\n"):
        parrafo = parrafo.strip()
        if parrafo:
            story.append(_p(parrafo, body_st))

    # ── Análisis por dimensión ──
    story.append(_p("Analisis por dimension", section_st))
    for dim in DIMENSIONES:
        nombre_dim = dim["nombre"]
        texto_dim  = analisis.get("por_dimension", {}).get(nombre_dim, "")
        prom       = puntajes[dim["id"]]["promedio"]
        dim_color  = HexColor(dim["color"])

        story.append(_colored_block(
            f"{_strip_emoji(dim['icono'])} {nombre_dim}  —  {prom}/10",
            dim_color,
        ))
        story.append(_body_block(texto_dim))
        story.append(Spacer(1, 0.15 * cm))

    # ── Plan de acción (3 más bajas) ──
    story.append(_p("Plan de accion — 3 dimensiones prioritarias", section_st))
    story.append(_p("Para las 3 dimensiones con menor puntaje", small_st))
    story.append(Spacer(1, 0.15 * cm))

    practica_label_st = ParagraphStyle(
        "PL", fontSize=10, fontName="Helvetica-Bold",
        textColor=DARK, leading=14, spaceAfter=2,
    )

    for item in analisis.get("practicas", []):
        dim_color = PURPLE
        for dim in DIMENSIONES:
            if dim["nombre"] == item.get("dimension", ""):
                dim_color = HexColor(dim["color"])
                break

        score_txt = item.get("score", "")
        story.append(_colored_block(
            f"{_strip_emoji(item.get('dimension', ''))}  —  {score_txt}/10",
            dim_color,
        ))
        practica_bg = HexColor("#ffffff")
        story.append(_body_block("Practica 1: " + item.get("practica_1", ""), practica_bg))
        story.append(_body_block("Practica 2: " + item.get("practica_2", ""), practica_bg))
        story.append(Spacer(1, 0.3 * cm))

    # ── Footer ──
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceBefore=8))
    story.append(_p("Juan Pablo Caamaño · @jpe.coachdevida · Rueda de la Vida", footer_st))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    doc.build(story)
    buf.seek(0)
    return buf.read()


def generar_informe_completo(nombre: str, puntajes: dict) -> tuple[str, str, bytes]:
    """
    Genera el informe completo.
    Retorna (html_str, barra_b64, pdf_bytes)
    """
    barra_b64   = generar_barra(puntajes)
    radar_bytes = generar_radar(puntajes)
    analisis    = generar_analisis(nombre, puntajes)
    html        = generar_html_informe(nombre, puntajes, analisis, barra_b64)
    pdf_bytes   = generar_pdf(nombre, puntajes, analisis, radar_bytes)
    return html, barra_b64, pdf_bytes
