"""Servicio de envío de emails para Evaluación 360 v2."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, APP_AUTO_URL, APP_FEEDBACK_URL


def _enviar_email(destinatario, asunto, cuerpo_html):
    """Envía un email HTML."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    msg["From"] = f"Evaluación 360 <{SMTP_USER}>"
    msg["To"] = destinatario
    msg.attach(MIMEText(cuerpo_html, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, destinatario, msg.as_string())


def enviar_invitacion_autoevaluacion(participante):
    """Envía invitación de autoevaluación a un participante."""
    link = f"{APP_AUTO_URL}/?token={participante['token_auto']}"
    nombre = f"{participante.get('pers_nombres', '')} {participante.get('pers_apellidos', '')}".strip() or participante.get('nombre', '')
    email = participante.get('pers_correo') or participante.get('email', '')
    asunto = "Invitación a Autoevaluación 360°"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">Evaluación 360°</h1>
        </div>
        <div style="padding: 30px; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
            <p>Hola <strong>{nombre}</strong>,</p>
            <p>Has sido invitado/a a completar tu autoevaluación 360°.</p>
            <p>Este proceso es confidencial y te ayudará en tu desarrollo profesional.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{link}"
                   style="background-color: #4CAF50; color: white; padding: 15px 30px;
                          text-decoration: none; border-radius: 8px; font-size: 16px;">
                    Comenzar Autoevaluación
                </a>
            </div>
            <p style="color: #666; font-size: 12px;">Si el botón no funciona, copia y pega este enlace en tu navegador:<br>
            <a href="{link}">{link}</a></p>
        </div>
    </body>
    </html>
    """
    _enviar_email(email, asunto, cuerpo)


def enviar_invitacion_feedback(evaluador, participante_nombre):
    """Envía invitación de feedback a un evaluador."""
    link = f"{APP_FEEDBACK_URL}/?token={evaluador['token']}"
    asunto = f"Invitación a Evaluación 360° — Feedback para {participante_nombre}"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">Evaluación 360°</h1>
        </div>
        <div style="padding: 30px; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
            <p>Hola <strong>{evaluador['nombre']}</strong>,</p>
            <p>Has sido seleccionado/a para evaluar a <strong>{participante_nombre}</strong> como parte del proceso de Evaluación 360°.</p>
            <p>Tu feedback es anónimo y muy valioso para el desarrollo profesional del evaluado.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{link}"
                   style="background-color: #2196F3; color: white; padding: 15px 30px;
                          text-decoration: none; border-radius: 8px; font-size: 16px;">
                    Completar Evaluación
                </a>
            </div>
            <p style="color: #666; font-size: 12px;">Si el botón no funciona, copia y pega este enlace en tu navegador:<br>
            <a href="{link}">{link}</a></p>
        </div>
    </body>
    </html>
    """
    _enviar_email(evaluador["email"], asunto, cuerpo)


def enviar_recordatorio_autoevaluacion(participante):
    """Envía recordatorio de autoevaluación."""
    link = f"{APP_AUTO_URL}/?token={participante['token_auto']}"
    nombre = f"{participante.get('pers_nombres', '')} {participante.get('pers_apellidos', '')}".strip() or participante.get('nombre', '')
    email = participante.get('pers_correo') or participante.get('email', '')
    asunto = "⏰ Recordatorio — Autoevaluación 360° pendiente"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #e65100; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">⏰ Recordatorio</h1>
        </div>
        <div style="padding: 30px; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
            <p>Hola <strong>{nombre}</strong>,</p>
            <p>Te recordamos que tu autoevaluación 360° aún está pendiente.</p>
            <p>Por favor, complétala lo antes posible.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{link}"
                   style="background-color: #e65100; color: white; padding: 15px 30px;
                          text-decoration: none; border-radius: 8px; font-size: 16px;">
                    Completar Autoevaluación
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    _enviar_email(email, asunto, cuerpo)


def enviar_recordatorio_feedback(evaluador, participante_nombre):
    """Envía recordatorio de feedback."""
    link = f"{APP_FEEDBACK_URL}/?token={evaluador['token']}"
    asunto = f"⏰ Recordatorio — Feedback 360° pendiente para {participante_nombre}"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #e65100; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">⏰ Recordatorio</h1>
        </div>
        <div style="padding: 30px; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
            <p>Hola <strong>{evaluador['nombre']}</strong>,</p>
            <p>Te recordamos que tu evaluación de <strong>{participante_nombre}</strong> aún está pendiente.</p>
            <p>Tu feedback es anónimo y muy importante. Por favor, complétalo lo antes posible.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{link}"
                   style="background-color: #e65100; color: white; padding: 15px 30px;
                          text-decoration: none; border-radius: 8px; font-size: 16px;">
                    Completar Evaluación
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    _enviar_email(evaluador["email"], asunto, cuerpo)


def enviar_invitacion_cc(evaluador, evaluado_nombre):
    """Envía invitación del Cuestionario Complementario a un evaluador."""
    from core.config import APP_CC_URL
    link = f"{APP_CC_URL}/?cc_token={evaluador['token']}"
    asunto = f"Cuestionario Complementario — Feedback para {evaluado_nombre}"
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">Cuestionario Complementario</h1>
        </div>
        <div style="padding: 30px; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
            <p>Hola <strong>{evaluador['nombre']}</strong>,</p>
            <p>Has sido invitado/a a responder un cuestionario sobre el liderazgo de <strong>{evaluado_nombre}</strong>.</p>
            <p>Son solo 3 preguntas abiertas. Tu respuesta es <strong>anónima</strong> y muy valiosa.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{link}"
                   style="background-color: #7c3aed; color: white; padding: 15px 30px;
                          text-decoration: none; border-radius: 8px; font-size: 16px;">
                    Responder Cuestionario
                </a>
            </div>
            <p style="color: #666; font-size: 12px;">Si el botón no funciona, copia y pega este enlace:<br>
            <a href="{link}">{link}</a></p>
        </div>
    </body>
    </html>
    """
    _enviar_email(evaluador["correo"], asunto, cuerpo)
