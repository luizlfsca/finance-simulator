from models import Divida, Transacao

def get_dados_iniciais():
    # Renda Mensal Estimada (Líquida)
    # Salário: ~3360 + App: ~1500 (conservador)
    renda_mensal = 3360 + 1500 
    
    # Despesas Fixas (Sem contar dívidas)
    # Seguro Carro (150) + Celular (100) + Combustível (200) + Streaming (50) + Lazer/Extras (300)
    despesas_fixas = 150 + 100 + 200 + 50 + 300

    # Dívidas Atuais
    # Juros de cartão rotativo estimados em 12% a.m (padrão mercado para rotativo/parcelado emissor)
    # Carro: Taxa de juros embutida no financiamento (não calculada aqui, apenas prestação fixa)
    
    dividas = [
        Divida(
            nome="Cartão Itaú",
            saldo_devedor=4803.58,
            taxa_juros_mensal=0.12, 
            parcela_mensal=1000.00 # Pagamento mínimo ou médio atual
        ),
        Divida(
            nome="Cartão Mercado Livre",
            saldo_devedor=4066.61,
            taxa_juros_mensal=0.12,
            parcela_mensal=800.00
        ),
        Divida(
            nome="Financiamento Carro",
            saldo_devedor=28146.99,
            taxa_juros_mensal=0.0, # Simplificação: Juros já estão no valor fixo da parcela
            parcela_mensal=1236.89,
            prazo_restante_meses=31
        )
    ]
    
    return renda_mensal, despesas_fixas, dividas
