import matplotlib.pyplot as plt

def plotar_evolucao_divida(historico_saldos):
    """
    Plota um gráfico simples da evolução do saldo devedor ao longo dos meses.
    """
    meses = range(len(historico_saldos))
    
    plt.figure(figsize=(10, 6))
    plt.plot(meses, historico_saldos, marker='o', linestyle='-', color='b')
    
    plt.title('Evolução do Saldo Devedor Total')
    plt.xlabel('Meses')
    plt.ylabel('Saldo Devedor (R$)')
    plt.grid(True)
    
    # Adicionar anotação no ponto final
    if historico_saldos:
        ultimo_mes = len(historico_saldos) - 1
        ultimo_valor = historico_saldos[-1]
        plt.annotate(f'Quitado em {ultimo_mes} meses!', 
                     xy=(ultimo_mes, ultimo_valor), 
                     xytext=(ultimo_mes - 2, ultimo_valor + 5000),
                     arrowprops=dict(facecolor='black', shrink=0.05))

    # Salvar a imagem ao invés de mostrar (para garantir que funcione sem interface gráfica se necessário)
    plt.savefig('evolucao_divida.png')
    print("Gráfico 'evolucao_divida.png' gerado com sucesso!")
    
    # Tentar mostrar se possível
    try:
        plt.show()
    except:
        pass
