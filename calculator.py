from typing import List, Dict
from models import Divida

def simular_mes(renda: float, despesas: float, dividas: List[Divida], estrategia: str = 'avalanche') -> Dict:
    """
    Simula um mês de pagamentos.
    Retorna o resumo do mês.
    """
    saldo_disponivel = renda - despesas
    pagamento_total_dividas = 0
    
    # 1. Pagar parcelas fixas/mínimas obrigatórias
    for div in dividas:
        if div.saldo_devedor > 0:
            valor_pagar = min(div.parcela_mensal, div.saldo_devedor)
            div.pagar(valor_pagar)
            pagamento_total_dividas += valor_pagar
            saldo_disponivel -= valor_pagar

    # 2. Se sobrar dinheiro, antecipar dívidas (Snowball ou Avalanche)
    # Avalanche: Paga a com maior juros primeiro
    # Snowball: Paga a com menor saldo devedor primeiro
    
    if saldo_disponivel > 0:
        if estrategia == 'avalanche':
            dividas_ordenadas = sorted(dividas, key=lambda x: x.taxa_juros_mensal, reverse=True)
        else: # snowball
            dividas_ordenadas = sorted(dividas, key=lambda x: x.saldo_devedor)
            
        for div in dividas_ordenadas:
            if saldo_disponivel <= 0:
                break
            if div.saldo_devedor > 0:
                # Se for financiamento com prazo fixo, muitas vezes antecipar desconta juros futuros.
                # Aqui simplificamos assumindo que reduz o saldo direto.
                pagamento_extra = saldo_disponivel
                if pagamento_extra > div.saldo_devedor:
                    pagamento_extra = div.saldo_devedor
                
                div.pagar(pagamento_extra)
                pagamento_total_dividas += pagamento_extra
                saldo_disponivel -= pagamento_extra

    # 3. Aplicar Juros sobre o saldo restante
    juros_totais = 0
    saldo_devedor_total = 0
    dividas_ativas = 0
    
    for div in dividas:
        if div.saldo_devedor > 0.01: # Considerar quitado se for centavos
            # Só projeta juros se não for parcela fixa sem juros compostos (ex: carro)
            # No data.py colocamos juros 0 para o carro para simplificar
            juros = div.aplicar_juros()
            juros_totais += juros
            saldo_devedor_total += div.saldo_devedor
            dividas_ativas += 1
            
            # Decrementar prazo se houver
            if div.prazo_restante_meses and div.prazo_restante_meses > 0:
                div.prazo_restante_meses -= 1
        else:
            div.saldo_devedor = 0

    return {
        "saldo_devedor_total": saldo_devedor_total,
        "juros_pagos_mes": juros_totais,
        "dividas_ativas": dividas_ativas
    }
