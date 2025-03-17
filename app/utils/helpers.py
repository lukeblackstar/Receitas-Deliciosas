import re
from datetime import datetime

def formatar_tempo(minutos):
    """Converte minutos em uma string formatada de horas e minutos."""
    if minutos < 60:
        return f"{minutos} minutos"
    horas = minutos // 60
    min_restantes = minutos % 60
    if min_restantes == 0:
        return f"{horas} hora{'s' if horas > 1 else ''}"
    return f"{horas}h {min_restantes}min"

def validar_receita(nome, ingredientes, modo_preparo, tempo, porcoes):
    """Valida os dados de uma receita antes de salvar."""
    erros = []
    
    if not nome or len(nome.strip()) < 3:
        erros.append("O nome da receita deve ter pelo menos 3 caracteres")
    
    if not ingredientes or len(ingredientes.strip()) < 10:
        erros.append("A lista de ingredientes está muito curta")
    
    if not modo_preparo or len(modo_preparo.strip()) < 20:
        erros.append("O modo de preparo está muito curto")
    
    try:
        tempo = int(tempo)
        if tempo <= 0:
            erros.append("O tempo de preparo deve ser maior que zero")
    except (ValueError, TypeError):
        erros.append("O tempo de preparo deve ser um número válido")
    
    try:
        porcoes = int(porcoes)
        if porcoes <= 0:
            erros.append("O número de porções deve ser maior que zero")
    except (ValueError, TypeError):
        erros.append("O número de porções deve ser um número válido")
    
    return erros

def formatar_ingredientes(texto):
    """Formata a lista de ingredientes para melhor visualização."""
    linhas = texto.strip().split('\n')
    formatado = []
    
    for linha in linhas:
        linha = linha.strip()
        if linha:
            
            if not linha.startswith(('•', '-', '*')):
                linha = f"• {linha}"
            formatado.append(linha)
    
    return '\n'.join(formatado)

def formatar_modo_preparo(texto):
    """Formata o modo de preparo para melhor visualização."""
    linhas = texto.strip().split('\n')
    formatado = []
    passo = 1
    
    for linha in linhas:
        linha = linha.strip()
        if linha:
            linha = re.sub(r'^\d+[\s.-]+', '', linha)
            formatado.append(f"{passo}. {linha}")
            passo += 1
    
    return '\n'.join(formatado)

def calcular_tempo_leitura(texto):
    """Calcula o tempo estimado de leitura do modo de preparo."""
    palavras = len(texto.split())
    minutos = max(1, round(palavras / 200))
    return f"{minutos} min de leitura" 