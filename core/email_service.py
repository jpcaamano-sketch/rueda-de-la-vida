import smtplib
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from email.mime.application import MIMEApplication
from core.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


def _send(to: str, subject: str, html: str, pdf_bytes: bytes = None):
    if pdf_bytes:
        msg = MIMEMultipart("mixed")
        msg.attach(MIMEText(html, "html", "utf-8"))
        pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
        pdf_part.add_header(
            "Content-Disposition", "attachment",
            filename="Rueda_de_la_Vida.pdf",
        )
        msg.attach(pdf_part)
    else:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(html, "html", "utf-8"))

    msg["Subject"] = subject
    msg["From"]    = f"YoCreo Coaching <{SMTP_USER}>"
    msg["To"]      = to

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.ehlo()
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.sendmail(SMTP_USER, to, msg.as_string())


def enviar_invitacion(nombre: str, email: str, link: str):
    """Email de invitación con el link al formulario."""
    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 0;">
<tr><td align="center">
<table width="560" cellpadding="0" cellspacing="0"
       style="background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);">
  <tr>
    <td style="background:linear-gradient(135deg,#1a3a5c,#2980b9);padding:32px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">🧭</div>
      <h1 style="margin:0;color:#fff;font-size:22px;">Rueda de la Vida</h1>
      <p style="margin:8px 0 0;color:rgba(255,255,255,0.8);font-size:14px;">Diagnóstico personal</p>
    </td>
  </tr>
  <tr>
    <td style="padding:32px 36px;">
      <p style="margin:0 0 14px;color:#333;font-size:15px;">Hola <strong>{nombre}</strong>,</p>
      <p style="margin:0 0 14px;color:#555;font-size:14px;line-height:1.6;">
        Te invitamos a completar tu <strong>Rueda de la Vida</strong>, un diagnóstico personal
        que evaluará 8 dimensiones clave de tu bienestar: trabajo, salud, finanzas,
        familia, amistades, desarrollo personal, ocio y propósito.
      </p>
      <p style="margin:0 0 24px;color:#555;font-size:14px;line-height:1.6;">
        El proceso toma aproximadamente <strong>10 minutos</strong>. Al finalizar recibirás
        un informe personalizado con gráfico, análisis de IA y prácticas concretas de mejora.
      </p>
      <div style="text-align:center;margin-bottom:24px;">
        <a href="{link}"
           style="display:inline-block;background:linear-gradient(135deg,#1a3a5c,#2980b9);
                  color:#fff;text-decoration:none;padding:14px 36px;border-radius:8px;
                  font-weight:700;font-size:15px;letter-spacing:0.3px;">
          Comenzar mi evaluación →
        </a>
      </div>
      <p style="margin:0;color:#aaa;font-size:12px;text-align:center;">
        O copia este enlace en tu navegador:<br/>
        <span style="color:#2980b9;">{link}</span>
      </p>
    </td>
  </tr>
  <tr>
    <td style="background:#1a3a5c;padding:16px;text-align:center;">
      <p style="margin:0;color:rgba(255,255,255,0.5);font-size:11px;">YoCreo Coaching</p>
    </td>
  </tr>
</table>
</td></tr>
</table>
</body>
</html>"""
    _send(email, "Tu diagnóstico personal — Rueda de la Vida 🧭", html)


def enviar_informe(nombre: str, email: str, html_informe: str, pdf_bytes: bytes = None):
    """Envía el informe completo al participante, con PDF adjunto si se provee."""
    _send(
        email,
        f"Tu Rueda de la Vida — Informe personal, {nombre}",
        html_informe,
        pdf_bytes,
    )
