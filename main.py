import requests

def calcular_risco_risco_hoje(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=relative_humidity_2m&daily=precipitation_sum&timezone=America%2FSao_Paulo&past_days=14"
    
    response = requests.get(url).json()
     
    chuvas_diarias = response['daily']['precipitation_sum']
    umidades_horarias = response['hourly']['relative_humidity_2m']
    
    risco_hoje_acumulado = 0

    # Percorremos os dias (do mais antigo para o mais recente)
    for i in range(len(chuvas_diarias)):
        chuva = chuvas_diarias[i]
        
        # 1. Regra da Chuva (Reset ou Redução)
        if chuva >= 13.0:
            risco_hoje_acumulado = 0 # Chuva forte zera o risco
        elif 5.0 <= chuva < 13.0:
            risco_hoje_acumulado *= 0.30 # Reduz 70% do risco
        elif 2.0 <= chuva < 5.0:
            risco_hoje_acumulado *= 0.70 # Reduz 30% do risco
            
        # 2. Cálculo da Umidade das 13:00 (risco_hoje usa esse horário padrão)
        # O índice 13, 37, 61... refere-se às 13h de cada dia no array hourly
        indice_13h = (i * 24) + 13
        if indice_13h < len(umidades_horarias):
            h13 = umidades_horarias[indice_13h]
            risco_hoje_acumulado += (100 / h13)

    return round(risco_hoje_acumulado, 2)

# Testando para Franco da Rocha
risco_hoje = calcular_risco_risco_hoje(-23.3217, -46.7269)

def classificar_risco(risco_hoje):
    """
    Recebe o valor do índice FMA e retorna a classificação e ação recomendada.
    """
    if risco_hoje <= 1.0:
        grau = "NULO"
        cenario = "Vegetação saturada de umidade. O fogo não se propaga."
        acao = "Monitoramento de rotina."
        cor = "\033[94m" # Azul
        
    elif risco_hoje <= 3.0:
        grau = "PEQUENO"
        cenario = "Materiais finos podem queimar, mas o fogo é lento."
        acao = "Manutenção de aceiros e limpeza."
        cor = "\033[92m" # Verde
        
    elif risco_hoje <= 8.0:
        grau = "MÉDIO"
        cenario = "Fogo ganhando velocidade. Difícil controle manual."
        acao = "ATENÇÃO: Proibir fogueiras e limpezas com fogo."
        cor = "\033[93m" # Amarelo
        
    elif risco_hoje <= 20.0:
        grau = "ALTO"
        cenario = "Propagação rápida. O fogo pula obstáculos e atinge copas."
        acao = "ALERTA: Brigadistas em prontidão total."
        cor = "\033[91m" # Vermelho
        
    else:
        grau = "MUITO ALTO"
        cenario = "CRÍTICO! Incêndios explosivos e calor extremo."
        acao = "EMERGÊNCIA: Patrulhamento ativo e interdição de áreas."
        cor = "\033[1;91m" # Vermelho Negrito e Intenso

    reset_cor = "\033[0m"
    
    # Retorna uma mensagem formatada
    return (f"{cor}--- RELATÓRIO DE RISCO ---\n"
            f"Grau: {grau}\n"
            f"Índice risco_hoje: {risco_hoje}\n"
            f"Cenário: {cenario}\n"
            f"Ação: {acao}{reset_cor}")

relatorio = classificar_risco(risco_hoje)
print(relatorio)