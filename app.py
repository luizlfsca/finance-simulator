import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from copy import deepcopy
from io import BytesIO
from datetime import datetime

# ==================== CONFIGURAÇÃO ====================
st.set_page_config(
    page_title="Simulador de Liberdade Financeira",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {font-size: 1.1rem; color: #666; margin-top: 0;}
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white; font-weight: 600; padding: 0.75rem;
        border-radius: 8px; border: none;
    }
    .info-box {
        background: #f0f2f6; padding: 1rem; border-radius: 8px;
        border-left: 4px solid #667eea; margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-header">💰 Simulador de Liberdade Financeira</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🎯 Configure suas dívidas e receitas abaixo e descubra quando estará livre!</p>', unsafe_allow_html=True)

# ==================== SESSION STATE (Dados Persistentes) ====================
if 'dividas' not in st.session_state:
    st.session_state.dividas = []

if 'receitas' not in st.session_state:
    st.session_state.receitas = []

if 'despesas_fixas' not in st.session_state:
    st.session_state.despesas_fixas = 0.0

# ==================== FUNÇÕES AUXILIARES ====================
def calcular_saldo_livre():
    total_receitas = sum(r['valor'] for r in st.session_state.receitas)
    return total_receitas - st.session_state.despesas_fixas

def simular_quitacao(saldo_mensal, estrategia='avalanche'):
    """Simula mês a mês até quitar todas as dívidas"""
    dividas_copia = deepcopy(st.session_state.dividas)
    meses = 0
    historico = []
    juros_acumulados = 0
    
    while True:
        # Calcular saldo total
        saldo_total = sum(d['saldo'] for d in dividas_copia if d['saldo'] > 0)
        
        if saldo_total <= 1 or meses >= 120:
            break
        
        historico.append({'mes': meses, 'saldo': saldo_total})
        
        # Pagar parcelas mínimas
        saldo_disponivel = saldo_mensal
        for div in dividas_copia:
            if div['saldo'] > 0:
                pagamento = min(div['parcela_minima'], div['saldo'])
                div['saldo'] -= pagamento
                saldo_disponivel -= pagamento
        
        # Aplicar juros COMPOSTOS (realidade bancária)
        for div in dividas_copia:
            if div['saldo'] > 0 and div['taxa_juros'] > 0:
                # Juros compostos mensais
                juros = div['saldo'] * ((1 + div['taxa_juros']) - 1)
                div['saldo'] += juros
                juros_acumulados += juros
        
        # Amortizar extra (estratégia)
        if saldo_disponivel > 0:
            if estrategia == 'avalanche':
                dividas_ordenadas = sorted([d for d in dividas_copia if d['saldo'] > 0], 
                                          key=lambda x: x['taxa_juros'], reverse=True)
            else:  # snowball
                dividas_ordenadas = sorted([d for d in dividas_copia if d['saldo'] > 0], 
                                          key=lambda x: x['saldo'])
            
            for div in dividas_ordenadas:
                if saldo_disponivel <= 0:
                    break
                amortizacao = min(saldo_disponivel, div['saldo'])
                div['saldo'] -= amortizacao
                saldo_disponivel -= amortizacao
        
        meses += 1
    
    return meses, pd.DataFrame(historico), juros_acumulados

# ==================== SIDEBAR: GERENCIAMENTO ====================
with st.sidebar:
    st.header("⚙️ Configuração")
    
    tab1, tab2 = st.tabs(["💳 Dívidas", "💵 Receitas"])
    
    # TAB: DÍVIDAS
    with tab1:
        st.subheader("Adicionar Dívida")
        
        with st.form("form_divida", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome_divida = st.text_input("Nome", placeholder="Ex: Cartão Itaú", 
                                           help="Nome identificador da dívida")
                saldo_divida = st.number_input("Saldo Devedor (R$)", min_value=0.0, step=100.0,
                                              help="Quanto você deve HOJE")
            with col2:
                tipo_divida = st.selectbox("Tipo", ["Cartão Crédito", "Financiamento", "Empréstimo"],
                                          help="Cartão: juros apenas se rotativo. Financiamento: juros embutidos.")
                parcela_min = st.number_input("Parcela Mínima (R$)", min_value=0.0, step=50.0,
                                             help="Valor que você PRECISA pagar por mês")
            
            # Campo de juros CONDICIONAL
            if tipo_divida == "Cartão Crédito":
                st.info("⚠️ **Cartões**: Se você paga no vencimento, deixe juros em 0%. Só preencha se estiver no rotativo.")
                taxa_juros = st.number_input("Juros a.m. (%)", min_value=0.0, max_value=50.0, value=0.0, step=1.0) / 100
            else:
                st.info("💡 **Financiamentos**: Juros já embutidos na parcela. Deixe em 0% se não souber.")
                taxa_juros = st.number_input("Juros a.m. (%)", min_value=0.0, max_value=10.0, value=0.0, step=0.1) / 100
            
            if st.form_submit_button("➕ Adicionar Dívida", width='stretch'):
                if nome_divida and saldo_divida > 0:
                    st.session_state.dividas.append({
                        'nome': nome_divida,
                        'tipo': tipo_divida,
                        'saldo': saldo_divida,
                        'taxa_juros': taxa_juros,
                        'parcela_minima': parcela_min
                    })
                    st.success(f"✅ {nome_divida} adicionada!")
                    st.rerun()
        
        # Lista de Dívidas
        if st.session_state.dividas:
            st.markdown("---")
            st.markdown("**Suas Dívidas:**")
            for i, div in enumerate(st.session_state.dividas):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{div['nome']}** ({div['tipo']})")
                    st.caption(f"R$ {div['saldo']:,.2f} | Juros: {div['taxa_juros']*100:.1f}% a.m.")
                with col2:
                    if st.button("🗑️", key=f"del_div_{i}"):
                        st.session_state.dividas.pop(i)
                        st.rerun()
        else:
            st.info("👆 Adicione suas dívidas acima")
    
    # TAB: RECEITAS
    with tab2:
        st.subheader("Adicionar Receita")
        
        with st.form("form_receita", clear_on_submit=True):
            nome_receita = st.text_input("Fonte", placeholder="Ex: Salário CLT", 
                                        help="Trabalho, freela, app, etc")
            valor_receita = st.number_input("Valor Líquido (R$)", min_value=0.0, step=100.0,
                                          help="Após descontos (INSS, IR")
            
            if st.form_submit_button("➕ Adicionar Receita", width='stretch'):
                if nome_receita and valor_receita > 0:
                    st.session_state.receitas.append({
                        'nome': nome_receita,
                        'valor': valor_receita
                    })
                    st.success(f"✅ {nome_receita} adicionada!")
                    st.rerun()
        
        # Lista de Receitas
        if st.session_state.receitas:
            st.markdown("---")
            st.markdown("**Suas Receitas:**")
            for i, rec in enumerate(st.session_state.receitas):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{rec['nome']}**")
                    st.caption(f"R$ {rec['valor']:,.2f}")
                with col2:
                    if st.button("🗑️", key=f"del_rec_{i}"):
                        st.session_state.receitas.pop(i)
                        st.rerun()
        else:
            st.info("👆 Adicione suas fontes de renda")
        
        # Despesas Fixas
        st.markdown("---")
        st.markdown("**Despesas Fixas Mensais:**")
        st.session_state.despesas_fixas = st.number_input(
            "Valor (R$)", 
            min_value=0.0, 
            value=st.session_state.despesas_fixas,
            step=100.0,
            help="Contas fixas (luz, água, internet, alimentação) SEM as parcelas das dívidas",
            key="despesas_input"
        )

# ==================== ÁREA PRINCIPAL ====================
# Resumo Financeiro
col1, col2, col3 = st.columns(3)

total_receitas = sum(r['valor'] for r in st.session_state.receitas)
total_dividas = sum(d['saldo'] for d in st.session_state.dividas)
saldo_livre = calcular_saldo_livre()

with col1:
    st.metric("💰 Receita Total", f"R$ {total_receitas:,.2f}")
with col2:
    st.metric("📊 Total Devendo", f"R$ {total_dividas:,.2f}", 
             delta=None if total_dividas == 0 else f"-R$ {total_dividas:,.2f}", delta_color="inverse")
with col3:
    if saldo_livre > 0:
        st.metric("✅ Sobra Mensal", f"R$ {saldo_livre:,.2f}", delta=f"+R$ {saldo_livre:,.2f}")
    else:
        st.metric("⚠️ Déficit", f"R$ {saldo_livre:,.2f}", delta=f"{saldo_livre:,.2f}", delta_color="inverse")

# Tabela de Dívidas
if st.session_state.dividas:
    st.markdown("---")
    st.subheader("📋 Resumo das Dívidas")
    df = pd.DataFrame([
        {
            "Nome": d['nome'],
            "Tipo": d['tipo'],
            "Saldo (R$)": f"R$ {d['saldo']:,.2f}",
            "Juros a.m.": f"{d['taxa_juros']*100:.1f}%",
            "Parc. Mín.": f"R$ {d['parcela_minima']:,.2f}"
        }
        for d in st.session_state.dividas
    ])
    st.dataframe(df, width='stretch', hide_index=True)

# Simulação
st.markdown("---")

if not st.session_state.dividas:
    st.warning("⚠️ Adicione pelo menos uma dívida na barra lateral para simular")
elif not st.session_state.receitas:
    st.warning("⚠️ Adicione pelo menos uma fonte de renda na barra lateral")
elif saldo_livre <= 0:
    st.error("❌ Seu saldo mensal está negativo! Aumente a renda ou reduza despesas.")
else:
    col1, col2 = st.columns([3, 1])
    
    with col2:
        estrategia = st.selectbox(
            "Estratégia",
            ["Avalanche 🔥", "Bola de Neve ❄️"],
            help="**Avalanche**: Paga dívidas com maiores juros primeiro (economiza mais)\n\n**Bola de Neve**: Paga dívidas menores primeiro (motivação psicológica)"
        )
        estrategia_key = 'avalanche' if 'Avalanche' in estrategia else 'snowball'
    
    with col1:
        if st.button("🚀 RODAR SIMULAÇÃO", type="primary", width='stretch'):
            with st.spinner("Calculando..."):
                meses, df_hist, juros_total = simular_quitacao(saldo_livre, estrategia_key)
                
                if meses >= 120:
                    st.error("⚠️ Com o saldo atual, levaria mais de 10 anos. Considere aumentar renda ou renegociar dívidas.")
                else:
                    st.success(f"🎉 **Você estará LIVRE em {meses} meses** ({meses//12} anos e {meses%12} meses)!")
                    
                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("⏱️ Prazo", f"{meses} meses")
                    with col2:
                        st.metric("💸 Juros Totais", f"R$ {juros_total:,.2f}")
                    with col3:
                        economia_vs_minimo = total_dividas * 0.10 * meses - juros_total if meses > 0 else 0
                        st.metric("💰 Economia", f"R$ {max(0, economia_vs_minimo):,.2f}")
                    
                    # Gráfico
                    if not df_hist.empty:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df_hist['mes'],
                            y=df_hist['saldo'],
                            mode='lines+markers',
                            fill='tozeroy',
                            line=dict(width=3, color='#667eea')
                        ))
                        fig.update_layout(
                            title="📈 Sua Jornada para R$ 0,00",
                            xaxis_title="Meses",
                            yaxis_title="Dívida Total (R$)",
                            template='plotly_white',
                            height=400
                        )
                        st.plotly_chart(fig, width='stretch')
                    
                    # Explicação Didática
                    st.markdown("---")
                    st.subheader("📖 Como Interpretar Estes Resultados")
                    
                    with st.expander("🎯 O que significam esses números?", expanded=True):
                        st.markdown(f"""
                        **Prazo ({meses} meses):**  
                        É o tempo que você levará para quitar TODAS as dívidas se manter o saldo mensal de R$ {saldo_livre:,.2f} focado nisso.
                        
                        **Juros Totais (R$ {juros_total:,.2f}):**  
                        É quanto você pagará de juros ao longo do processo. Quanto menor, melhor!
                        
                        **Estratégia {estrategia}:**  
                        {'Você está pagando primeiro as dívidas com MAIORES JUROS. Isso economiza dinheiro no longo prazo.' if estrategia_key == 'avalanche' else 'Você está pagando primeiro as MENORES DÍVIDAS. Isso gera motivação rápida (menos boletos).'}
                        """)
                    
                    with st.expander("💡 Dicas para Acelerar"):
                        st.markdown("""
                        1. **Aumente a Renda:** Qualquer extra (freela, app, hora-extra) reduz drasticamente o prazo
                        2. **Reduza Despesas:** Cortar R$ 100/mês pode economizar meses de dívida
                        3. **Negocie Juros:** Ligue para o banco e peça redução de juros do rotativo
                        4. **Evite Novas Dívidas:** Use apenas se realmente necessário
                        """)
                    
                    # Botão Download Excel
                    st.markdown("---")
                    st.subheader("📥 Exportar Relatório")
                    
                    # Preparar dados para Excel
                    df_export = df_hist.copy()
                    df_export.columns = ['Mês', 'Saldo Devedor (R$)']
                    
                    # Adicionar sumário
                    sumario_data = {
                        'Métrica': ['Prazo Total', 'Juros Pagos', 'Estratégia', 'Saldo Mensal', 'Data Simulação'],
                        'Valor': [
                            f'{meses} meses',
                            f'R$ {juros_total:,.2f}',
                            estrategia,
                            f'R$ {saldo_livre:,.2f}',
                            datetime.now().strftime('%d/%m/%Y %H:%M')
                        ]
                    }
                    df_sumario = pd.DataFrame(sumario_data)
                    
                    # Criar Excel em memória
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_sumario.to_excel(writer, sheet_name='Resumo', index=False)
                        df_export.to_excel(writer, sheet_name='Evolução Mensal', index=False)
                        
                        # Adicionar detalhes das dívidas
                        df_dividas_export = pd.DataFrame([
                            {
                                'Nome': d['nome'],
                                'Tipo': d['tipo'],
                                'Saldo Inicial': f"R$ {d['saldo']:,.2f}",
                                'Taxa Juros a.m.': f"{d['taxa_juros']*100:.2f}%",
                                'Parcela Mínima': f"R$ {d['parcela_minima']:,.2f}"
                            }
                            for d in st.session_state.dividas
                        ])
                        df_dividas_export.to_excel(writer, sheet_name='Dívidas', index=False)
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="📥 Baixar Relatório Excel",
                        data=output,
                        file_name=f"simulacao_financeira_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        width='stretch'
                    )


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p style='font-size: 0.9rem;'>💡 <strong>Lembre-se:</strong> Este é um simulador educacional. Sempre consulte um especialista financeiro para decisões importantes.</p>
</div>
""", unsafe_allow_html=True)
