import sqlite3
import smtplib
from email.message import EmailMessage

def buscar_emails():
    conexao = sqlite3.connect('alertas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT email FROM usuarios')
    # Transforma a lista de tuplas em uma lista simples de strings
    emails = [linha[0] for linha in cursor.fetchall()]
    conexao.close()
    return emails

def enviar_alerta(grau, resultado, cenario, acao, cor):
    lista_contatos = buscar_emails()
    if not lista_contatos: return

    EMAIL_ORIGEM = "meu_email@gmail.com"
    SENHA_APP = "~fçlkfl çksd~fm d~sfkdk"

    msg = EmailMessage()
    msg['Subject'] = f"⚠️ ALERTA: Risco de Incêndio {grau}"
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = ", ".join(lista_contatos)

    # Aqui montamos o corpo do e-mail usando as variáveis
    conteudo_html = f"""
    <html>
        <body style="font-family: sans-serif;">
            <div style="background-color: {cor}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h1>Grau de Perigo: {grau}</h1>
                <p>O índice FMA atual é de <strong>{resultado}</strong></p>
            </div>
            <div style="padding: 20px; border: 1px solid #ccc; margin-top: 10px;">
                <p><strong>Cenário observado:</strong> {cenario}</p>
                <p><strong>Recomendação:</strong> {acao}</p>
            </div>
            <p style="font-size: 12px; color: #666;">Monitoramento Fire 0 - Parque Estadual do Juquery</p>
        </body>
    </html>
    """
    msg.set_content("Aviso de risco de incêndio.", subtype='html') # Fallback texto
    msg.add_alternative(conteudo_html, subtype='html') # Versão visual

    # ... (código de envio smtplib continua igual)

    # Envio Real
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ORIGEM, SENHA_APP)
            smtp.send_message(msg)
            print("Alertas enviados com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
