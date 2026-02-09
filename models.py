from dataclasses import dataclass
from typing import Optional

@dataclass
class Divida:
    nome: str
    saldo_devedor: float
    taxa_juros_mensal: float  # Ex: 0.12 para 12% ao mês
    parcela_mensal: float
    prazo_restante_meses: Optional[int] = None # Para financiamentos com prazo fixo

    def aplicar_juros(self):
        """Aplica juros ao saldo devedor."""
        juros = self.saldo_devedor * self.taxa_juros_mensal
        self.saldo_devedor += juros
        return juros

    def pagar(self, valor: float):
        """Reduz o saldo devedor pelo valor pago."""
        if valor > self.saldo_devedor:
            valor = self.saldo_devedor
        self.saldo_devedor -= valor
        return valor

@dataclass
class Transacao:
    nome: str
    valor: float
    tipo: str # 'receita' ou 'despesa'
