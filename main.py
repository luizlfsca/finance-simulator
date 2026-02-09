from data import get_dados_iniciais
from calculator import simular_mes
from visualizer import plotar_evolucao_divida # Importar visualização
from models import Divida

def main():
    print("--- Simulador de Liberdade Financeira ---")
    
    # 1. Carregar Dados
    renda, despesas, dividas = get_dados_iniciais()
    
    print(f"Renda Mensal Estimada: R$ {renda:.2f}")
    print(f"Despesas Fixas Estimadas: R$ {despesas:.2f}")
    print(f"Saldo Inicial Disponível para Dívidas: R$ {renda - despesas:.2f}")
    print("-" * 30)
    
    # 2. Loop de Simulação
    meses = 0
    historico_divida_total = []
    
    while True:
        meses += 1
        
        # Calcular Saldo Total Devedor
        saldo_total = sum(d.saldo_devedor for d in dividas)
        historico_divida_total.append(saldo_total)
        
        if saldo_total <= 1: # Consideramos quitado se for menor que 1 real
            print(f"\nPARABÉNS! Dívidas quitadas em {meses} meses.")
            break
            
        if meses > 120: # Limite de segurança (10 anos)
            print("\nAviso: Simulação interrompida após 10 anos (dívida impagável?)")
            break
            
        resultado = simular_mes(renda, despesas, dividas)
        
        # Opcional: Mostrar progresso a cada ano
        if meses % 12 == 0:
            print(f"Mês {meses}: Saldo Devedor Total R$ {resultado['saldo_devedor_total']:.2f}")

    # 3. Visualizar Resultado
    plotar_evolucao_divida(historico_divida_total)

if __name__ == "__main__":
    main()
