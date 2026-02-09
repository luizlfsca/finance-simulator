# 💰 Simulador de Liberdade Financeira

> **Projeto de portfólio desenvolvido para demonstrar habilidades em Python, visualização de dados e UX**

Um aplicativo web interativo que simula cenários de quitação de dívidas, permitindo ao usuário comparar estratégias de pagamento (Avalanche vs Bola de Neve) e descobrir quanto tempo levará para alcançar a liberdade financeira.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 Funcionalidades

✅ **CRUD Completo**: Adicione/remova dívidas e fontes de renda diretamente na interface  
✅ **Simulação Inteligente**: Calcula prazo de quitação com juros compostos reais  
✅ **Comparação de Estratégias**:
  - **Avalanche**: Prioriza dívidas com maiores juros (economiza dinheiro)
  - **Bola de Neve**: Prioriza dívidas menores (motivação psicológica)  
✅ **Visualizações Interativas**: Gráficos Plotly com zoom e hover  
✅ **Export para Excel**: Baixe relatório completo com resumo + evolução mensal  
✅ **UX Autoexplicativa**: Tooltips, exemplos e explicações didáticas  
✅ **Design Moderno**: CSS customizado com gradientes e animações

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.12+ instalado
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/finance-simulator.git
cd finance-simulator
```

2. **Instale as dependências**
```bash
pip install streamlit pandas plotly openpyxl
```

3. **Execute o aplicativo**
```bash
streamlit run app.py
```

4. **Acesse no navegador**
```
http://localhost:8501
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
|------------|-----------|
| **Python 3.12** | Linguagem principal |
| **Streamlit** | Framework web para aplicações de dados |
| **Pandas** | Manipulação de dados e export Excel |
| **Plotly** | Gráficos interativos |
| **CSS** | Estilização personalizada |

---

## 📊 Conceitos Demonstrados

- **Programação Orientada a Objetos**: Modelagem de dados (`models.py`)
- **Lógica de Negócio**: Simulação financeira com juros compostos
- **Visualização de Dados**: Gráficos interativos e dashboards
- **UX/UI Design**: Interface intuitiva e responsiva
- **Manipulação de Estado**: Session state do Streamlit
- **Export de Dados**: Geração de relatórios Excel

---

## 🎓 Casos de Uso

1. **Educacional**: Entender o impacto de diferentes estratégias de quitação
2. **Planejamento Pessoal**: Simular cenários reais de dívidas
3. **Comparação de Cenários**: "E se eu aumentar minha renda em R$ 500?"

---

## 📸 Screenshots

### Tela Principal
*Interface com CRUD de dívidas e receitas*

### Resultado da Simulação
*Gráfico interativo mostrando evolução da dívida mês a mês*

### Exportação Excel
*Relatório com 3 abas: Resumo, Evolução Mensal e Dívidas*

---

## 🔮 Roadmap Futuro

- [ ] Persistência com SQLite (salvar dados localmente)
- [ ] Modelo avançado de cartões de crédito (compras individuais, parcelas)
- [ ] Dashboard de risco de inadimplência
- [ ] Sugestões inteligentes de investimento
- [ ] PWA (Progressive Web App) para mobile

---

## 👨‍💻 Autor

**Luiz Felipe**  
Analista de Experiência do Cliente em transição para Dados  

📧 [seu-email@exemplo.com](mailto:seu-email@exemplo.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/seu-perfil)  
💼 [Portfólio](https://github.com/SEU_USUARIO)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

- Inspirado em metodologias financeiras de Dave Ramsey (Bola de Neve) e suze Orman (Avalanche)
- Comunidade Streamlit pela documentação excelente
- Plotly pela biblioteca de visualização poderosa

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**
