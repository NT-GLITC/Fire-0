import requests
from flask import Flask, render_template, request
from database import criar_banco, salvar_email
from comunicacao import enviar_alerta

criar_banco()

app = Flask(__name__)

def calcular_risco_fma(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=relative_humidity_2m&daily=precipitation_sum&timezone=America%2FSao_Paulo&past_days=14"
        response = requests.get(url).json()
        
        chuvas_diarias = response['daily']['precipitation_sum']
        umidades_horarias = response['hourly']['relative_humidity_2m']
        
        acumulado = 0
        for i in range(len(chuvas_diarias)):
            chuva = chuvas_diarias[i]
            
            # Regra da Chuva
            if chuva >= 13.0:
                acumulado = 0 
            elif 5.0 <= chuva < 13.0:
                acumulado *= 0.30 
            elif 2.0 <= chuva < 5.0:
                acumulado *= 0.70 
                
            # Umidade das 13h
            indice_13h = (i * 24) + 13
            if indice_13h < len(umidades_horarias):
                h13 = umidades_horarias[indice_13h]
                acumulado += (100 / h13)

        return round(acumulado, 2)
    except:
        return 0.0

def classificar_para_web(valor_fma):
    if valor_fma <= 1.0:
        return {
            "grau": "NULO", 
            "cor": "#3498db", 
            "cenario": "O ambiente está úmido, chance de fogo começar ou se espalhar baixa.", # <-- A KEY FALTANTE
            "acao": [
                "Evite acender fogueiras em áreas de mato ou próximo à vegetação.",
                "Não jogue pontas de cigarro ou fósforos no chão, especialmente perto de folhas ou galhos secos.",
                "Não queime lixo ou restos de poda ao ar livre.",
                "Mantenha terrenos limpos, retirando excesso de folhas e galhos secos.",
                "Oriente familiares e vizinhos sobre cuidados básicos com fogo."
            ]
        }
    elif valor_fma <= 3.0:
        return {
            "grau": "PEQUENO", 
            "cor": "#2ecc71", 
            "cenario": "Condições mais secas. Sem grande risco de incêndio.",
            "acao": ["Evite acender fogueiras em áreas de mato ou próximo à vegetação",
                    "Não jogue pontas de cigarro ou fósforos no chão, especialmente perto de folhas ou galhos secos.",
                    "Não queime lixo ou restos de poda ao ar livre."
            ]
        }
    elif valor_fma <= 8.0:
        return {
            "grau": "MÉDIO", 
            "cor": "#f1c40f", 
            "cenario": "Condições muito favoráveis para início e rápida propagação do fogo.",
            "acao": [
                "Não faça fogueiras ou queimadas de qualquer tipo.",
                "Evite acender fogões a lenha próximos a áreas com vegetação seca.",
                "Não utilize fogo para limpeza de terrenos ou descarte de resíduos.",
                "Evite estacionar veículos sobre capim seco.",
                "Comunique imediatamente qualquer foco de incêndio ao Corpo de Bombeiros (193)."
            ]
        }
    elif valor_fma <= 20.0:
        return {
            "grau": "ALTO", 
            "cor": "#e67e22", 
            "cenario": "Condições muito favoráveis para início e rápida propagação do fogo.",
            "acao": [
                "Não faça fogueiras ou queimadas de qualquer tipo.",
                "Evite acender fogões a lenha próximos a áreas com vegetação seca.",
                "Não utilize fogo para limpeza de terrenos ou descarte de resíduos.",
                "Evite estacionar veículos sobre capim seco.",
                "Comunique imediatamente qualquer foco de incêndio ao Corpo de Bombeiros (193)."
            ]
        }
    else:
        return {
            "grau": "MUITO ALTO", 
            "cor": "#e74c3c", 
            "cenario": "Condições críticas, com altíssimo risco de incêndio e propagação rápida.",
            "acao": [
                "Não realize nenhuma atividade que envolva fogo.",
                "Suspenda totalmente fogueiras, queimadas e uso de fogo a céu aberto.",
                "Evite qualquer atividade rural que possa gerar calor ou faíscas.",
                "Siga rigorosamente orientações e alertas das autoridades locais.",
                "Reporte imediatamente qualquer sinal de fumaça ou incêndio ao 193."
            ]
        }

# --- ROTAS ---

@app.route('/')
def home():
    # Página inicial limpa
    return render_template('index.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    valor_fma = calcular_risco_fma(-23.3217, -46.7269)
    detalhes = classificar_para_web(valor_fma)

    # Dispara o e-mail com as informações do dicionário 'detalhes'
    # Você pode colocar um 'if' para enviar e-mail apenas se o risco for alto
    enviar_alerta(
        grau=detalhes['grau'],
        resultado=valor_fma,
        cenario=detalhes['cenario'],
        acao=detalhes['acao'],
        cor=detalhes['cor']
    )

    return render_template('index.html', 
                           resultado=valor_fma, 
                           grau=detalhes['grau'], 
                           cor=detalhes['cor'], 
                           cenario=detalhes['cenario'],
                           acao=detalhes['acao'])

@app.route('/cadastrar-email', methods=['POST'])
def cadastrar_email():
    email_usuario = request.form.get('email')
    sucesso = salvar_email(email_usuario)
    
    if sucesso:
        msg = "E-mail cadastrado com sucesso!"
    else:
        msg = "Este e-mail já está cadastrado ou é inválido."
        
    return render_template('index.html', mensagem_email=msg)

if __name__ == '__main__':
    app.run(debug=True)