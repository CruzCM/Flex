"""Renderizacao HTML autocontida do dashboard Radar Financeiro."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from html import escape
from typing import Any
from uuid import uuid4

import pandas as pd


MESES_PT_BR = (
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)


_CSS = r"""
.rf-dashboard {
  --blue-950: #041f4a;
  --blue-900: #062b68;
  --blue-800: #073b85;
  --blue-700: #074bb8;
  --blue-600: #1557d6;
  --blue-100: #eaf1ff;
  --blue-050: #f5f8ff;
  --yellow: #ffdf00;
  --yellow-100: #fff8bf;
  --canvas: #f3f6fb;
  --surface: #ffffff;
  --ink: #14213d;
  --muted: #66758e;
  --line: #e0e6ef;
  --line-strong: #cfd8e6;
  --green: #08795f;
  --green-soft: #edf8f4;
  --red: #b3263e;
  --red-soft: #fff2f4;
  --amber: #8c5a00;
  --amber-soft: #fff8e8;
  --shadow: 0 18px 46px rgba(25, 48, 87, .075);
  --radius-panel: 24px;
  --radius-card: 16px;
  width: 100%;
  min-width: 0;
  color: var(--ink);
  background:
    radial-gradient(circle at 90% 0, rgba(21, 87, 214, .055), transparent 360px),
    var(--canvas);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 14px;
  line-height: 1.45;
  -webkit-font-smoothing: antialiased;
}

.rf-dashboard,
.rf-dashboard * { box-sizing: border-box; }

.rf-dashboard .page {
  width: min(1320px, calc(100% - 32px));
  margin: 0 auto;
  padding: 22px 0 48px;
}

.rf-dashboard .topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 3px 3px 18px;
}

.rf-dashboard .brand { display: flex; align-items: center; gap: 12px; }
.rf-dashboard .brand-mark {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 13px;
  color: var(--yellow);
  background: linear-gradient(145deg, var(--blue-800), var(--blue-700));
  box-shadow: 0 10px 24px rgba(7, 59, 133, .2);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: .04em;
}
.rf-dashboard .brand h1 { margin: 0; font-size: 18px; letter-spacing: -.025em; }
.rf-dashboard .brand p { margin: 2px 0 0; color: var(--muted); font-size: 12px; }
.rf-dashboard .updated { color: var(--muted); font-size: 12px; text-align: right; }
.rf-dashboard .updated strong { display: block; margin-top: 2px; color: var(--ink); font-size: 13px; }

.rf-dashboard .stack {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 16px;
}
.rf-dashboard .panel {
  min-width: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: var(--radius-panel);
  background: rgba(255, 255, 255, .97);
  box-shadow: var(--shadow);
}
.rf-dashboard .panel-inner { padding: 24px; }
.rf-dashboard .section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 22px;
  margin-bottom: 18px;
}
.rf-dashboard .eyebrow {
  display: block;
  margin-bottom: 4px;
  color: var(--blue-600);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: .09em;
  text-transform: uppercase;
}
.rf-dashboard .section-head h2 { margin: 0; font-size: 21px; letter-spacing: -.035em; }
.rf-dashboard .section-head p { margin: 5px 0 0; color: var(--muted); font-size: 12px; }

.rf-dashboard .client-overview {
  display: grid;
  grid-template-columns: .72fr 1.05fr 1.4fr;
  gap: 12px;
}
.rf-dashboard .info-card {
  min-width: 0;
  padding: 17px 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius-card);
  background: #fff;
}
.rf-dashboard .info-card.primary {
  border-color: transparent;
  color: #fff;
  background: linear-gradient(135deg, var(--blue-800), var(--blue-600));
  box-shadow: 0 10px 28px rgba(7, 75, 184, .16);
}
.rf-dashboard .info-label { display: block; color: var(--muted); font-size: 12px; font-weight: 700; }
.rf-dashboard .primary .info-label { color: rgba(255, 255, 255, .74); }
.rf-dashboard .info-value {
  display: block;
  margin-top: 7px;
  overflow-wrap: anywhere;
  font-size: 27px;
  line-height: 1.05;
  font-weight: 900;
  letter-spacing: -.04em;
}
.rf-dashboard .period {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
  font-size: 20px;
  font-weight: 850;
  letter-spacing: -.025em;
}
.rf-dashboard .period i { width: 26px; height: 1px; flex: 0 0 26px; background: var(--line-strong); }
.rf-dashboard .context-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 9px;
  margin-top: 12px;
}
.rf-dashboard .context-card {
  min-width: 0;
  padding: 13px 14px;
  border: 1px solid transparent;
  border-radius: 13px;
  background: var(--blue-050);
}
.rf-dashboard .context-card > span { display: block; color: var(--muted); font-size: 11px; }
.rf-dashboard .context-card strong { display: block; margin-top: 4px; overflow-wrap: anywhere; font-size: 13px; line-height: 1.35; }
.rf-dashboard .context-card small { display: block; margin-top: 2px; color: var(--muted); font-size: 11px; }
.rf-dashboard .context-card.pending { border-color: #f2e5b8; background: var(--amber-soft); }
.rf-dashboard .context-card.pending strong { color: var(--amber); }

.rf-dashboard .metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}
.rf-dashboard .metric-card {
  min-width: 0;
  padding: 17px;
  border: 1px solid var(--line);
  border-radius: var(--radius-card);
  background: #fff;
}
.rf-dashboard .metric-card.positive { border-color: #d4ece3; background: var(--green-soft); }
.rf-dashboard .metric-card.negative { border-color: #efd3da; background: var(--red-soft); }
.rf-dashboard .metric-card > span { color: var(--muted); font-size: 12px; font-weight: 700; }
.rf-dashboard .metric-card strong {
  display: block;
  margin-top: 7px;
  overflow-wrap: anywhere;
  font-size: 24px;
  line-height: 1.05;
  letter-spacing: -.035em;
}
.rf-dashboard .metric-card.positive strong { color: var(--green); }
.rf-dashboard .metric-card.negative strong { color: var(--red); }
.rf-dashboard .metric-card small { display: block; margin-top: 7px; color: var(--muted); font-size: 11px; }
.rf-dashboard .metric-card small b { color: var(--ink); }
.rf-dashboard .status-row { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 11px; }
.rf-dashboard .chip {
  padding: 7px 10px;
  border: 1px solid var(--line);
  border-radius: 999px;
  color: var(--muted);
  background: #fff;
  font-size: 11px;
  white-space: normal;
}
.rf-dashboard .chip strong { color: var(--ink); }

.rf-dashboard .flow-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 15px;
}
.rf-dashboard .flow-card {
  min-width: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 19px;
  background: #fff;
}
.rf-dashboard .flow-card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--line);
  background: var(--blue-050);
}
.rf-dashboard .flow-card.entries .flow-card-head { background: var(--green-soft); }
.rf-dashboard .flow-card-head h3 { margin: 0; font-size: 16px; letter-spacing: -.015em; }
.rf-dashboard .flow-card-head p { margin: 3px 0 0; color: var(--muted); font-size: 11px; }
.rf-dashboard .flow-total { text-align: right; white-space: nowrap; }
.rf-dashboard .flow-total span { display: block; color: var(--muted); font-size: 11px; }
.rf-dashboard .flow-total strong { display: block; margin-top: 3px; font-size: 17px; }
.rf-dashboard .entries .flow-total strong { color: var(--green); }
.rf-dashboard .flow-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.rf-dashboard .flow-table caption,
.rf-dashboard .theme-table caption {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
.rf-dashboard .flow-table thead th {
  padding: 9px 12px;
  color: var(--muted);
  background: #fbfcfe;
  border-bottom: 1px solid var(--line);
  font-size: 11px;
  font-weight: 750;
  text-align: left;
}
.rf-dashboard .flow-table thead th:last-child { text-align: right; }
.rf-dashboard .flow-row th,
.rf-dashboard .flow-row td {
  height: 57px;
  padding: 10px 12px;
  border-bottom: 1px solid #edf1f5;
  vertical-align: middle;
}
.rf-dashboard .flow-row:last-of-type th,
.rf-dashboard .flow-row:last-of-type td { border-bottom: 0; }
.rf-dashboard .flow-row th { width: 31%; font-size: 12px; text-align: left; }
.rf-dashboard .flow-row .bar-cell { width: 34%; }
.rf-dashboard .flow-row .value-cell { width: 35%; text-align: right; }
.rf-dashboard .track { height: 7px; overflow: hidden; border-radius: 999px; background: #e9eef5; }
.rf-dashboard .track span { display: block; height: 100%; border-radius: inherit; background: var(--blue-600); }
.rf-dashboard .entries .track span { background: var(--green); }
.rf-dashboard .flow-value { display: block; font-size: 12px; font-weight: 850; white-space: nowrap; }
.rf-dashboard .flow-reference { display: block; margin-top: 2px; color: var(--muted); font-size: 11px; white-space: nowrap; }
.rf-dashboard .flow-state { display: block; margin-top: 2px; color: var(--red); font-size: 11px; font-weight: 750; }
.rf-dashboard .flow-row.attention th,
.rf-dashboard .flow-row.attention .flow-value { color: var(--red); }
.rf-dashboard .future-detail-row[hidden] { display: none; }

.rf-dashboard .priority-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  max-width: 100%;
  padding: 8px 11px;
  border: 1px solid #edda38;
  border-radius: 999px;
  color: var(--blue-950);
  background: var(--yellow-100);
  font-size: 11px;
  font-weight: 850;
  white-space: normal;
}
.rf-dashboard .priority-badge::before {
  content: "";
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: 50%;
  background: var(--yellow);
  box-shadow: 0 0 0 1px #d4ba00;
}
.rf-dashboard .theme-table-wrap { overflow: hidden; border: 1px solid var(--line); border-radius: var(--radius-card); }
.rf-dashboard .theme-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.rf-dashboard .theme-table thead th {
  padding: 10px 13px;
  color: var(--muted);
  background: #f7f9fc;
  border-bottom: 1px solid var(--line);
  font-size: 11px;
  text-align: center;
}
.rf-dashboard .theme-table thead th:first-child { width: 42%; text-align: left; }
.rf-dashboard .theme-table tbody th,
.rf-dashboard .theme-table tbody td {
  height: 55px;
  padding: 10px 13px;
  border-bottom: 1px solid var(--line);
  text-align: center;
}
.rf-dashboard .theme-table tbody tr:last-child th,
.rf-dashboard .theme-table tbody tr:last-child td { border-bottom: 0; }
.rf-dashboard .theme-table tbody th { text-align: left; font-size: 12px; }
.rf-dashboard .theme-table tbody td { font-size: 13px; font-weight: 820; }
.rf-dashboard .theme-table tbody tr.selected { background: linear-gradient(90deg, #fffbe2, #fff 48%); }
.rf-dashboard .theme-table tbody tr.selected th { color: var(--blue-900); box-shadow: inset 4px 0 var(--yellow); }
.rf-dashboard .winner-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-left: 8px;
  padding: 4px 7px;
  border-radius: 999px;
  color: var(--blue-900);
  background: var(--yellow-100);
  font-size: 11px;
  font-weight: 850;
  vertical-align: middle;
}
.rf-dashboard .final-score { color: var(--blue-700); font-size: 17px !important; font-weight: 950 !important; }
.rf-dashboard .selected .final-score span {
  display: inline-grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 9px;
  color: var(--blue-950);
  background: var(--yellow);
}
.rf-dashboard .note { margin: 11px 2px 0; color: var(--muted); font-size: 11px; }

@media (max-width: 1040px) {
  .rf-dashboard .client-overview { grid-template-columns: 1fr 1fr; }
  .rf-dashboard .client-overview > :last-child { grid-column: 1 / -1; }
  .rf-dashboard .context-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .rf-dashboard .metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .rf-dashboard .flow-grid { grid-template-columns: 1fr; }
}

@media (max-width: 720px) {
  .rf-dashboard .page { width: min(calc(100% - 20px), 1320px); padding-top: 12px; }
  .rf-dashboard .topbar { align-items: flex-start; }
  .rf-dashboard .updated { max-width: 220px; }
  .rf-dashboard .panel-inner { padding: 19px; }
  .rf-dashboard .section-head { align-items: flex-start; flex-direction: column; gap: 11px; }
  .rf-dashboard .client-overview { grid-template-columns: 1fr; }
  .rf-dashboard .client-overview > :last-child { grid-column: auto; }
  .rf-dashboard .context-grid,
  .rf-dashboard .metric-grid { grid-template-columns: 1fr 1fr; }
  .rf-dashboard .period { font-size: 18px; }
  .rf-dashboard .theme-table thead th:first-child { width: 36%; }
}

@media (max-width: 560px) {
  .rf-dashboard .topbar { flex-direction: column; }
  .rf-dashboard .updated { max-width: none; text-align: left; }
  .rf-dashboard .context-grid,
  .rf-dashboard .metric-grid { grid-template-columns: 1fr; }
  .rf-dashboard .panel-inner { padding: 16px; }
  .rf-dashboard .flow-card-head { align-items: flex-start; flex-wrap: wrap; }
  .rf-dashboard .flow-row th { width: 30%; }
  .rf-dashboard .flow-row .bar-cell { width: 22%; }
  .rf-dashboard .flow-row .value-cell { width: 48%; }
  .rf-dashboard .flow-row th,
  .rf-dashboard .flow-row td { padding: 10px 8px; }
  .rf-dashboard .theme-table-wrap { border: 0; overflow: visible; }
  .rf-dashboard .theme-table,
  .rf-dashboard .theme-table tbody { display: block; }
  .rf-dashboard .theme-table thead {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  .rf-dashboard .theme-table tbody { display: grid; gap: 8px; }
  .rf-dashboard .theme-table tbody tr {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    overflow: hidden;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: #fff;
  }
  .rf-dashboard .theme-table tbody tr.selected { background: #fffbe5; }
  .rf-dashboard .theme-table tbody th {
    grid-column: 1 / -1;
    width: auto;
    height: auto;
    min-height: 45px;
    padding: 12px;
    border-bottom: 1px solid var(--line);
    box-shadow: none !important;
  }
  .rf-dashboard .theme-table tbody td {
    display: grid;
    align-content: center;
    min-width: 0;
    height: 60px;
    padding: 7px 4px;
    border-right: 1px solid var(--line);
    border-bottom: 0;
    font-size: 12px;
  }
  .rf-dashboard .theme-table tbody td:last-child { border-right: 0; }
  .rf-dashboard .theme-table tbody td::before {
    content: attr(data-label);
    display: block;
    margin-bottom: 3px;
    color: var(--muted);
    font-size: 11px;
    font-weight: 650;
    line-height: 1.1;
  }
  .rf-dashboard .winner-label { margin-left: 5px; }
}

@media (max-width: 390px) {
  .rf-dashboard .page { width: calc(100% - 14px); }
  .rf-dashboard .brand h1 { font-size: 17px; }
  .rf-dashboard .period { gap: 8px; font-size: 16px; }
  .rf-dashboard .period i { width: 15px; flex-basis: 15px; }
  .rf-dashboard .flow-card-head { flex-direction: column; gap: 8px; padding: 14px; }
  .rf-dashboard .flow-total { text-align: left; }
  .rf-dashboard .flow-total strong { font-size: 15px; }
  .rf-dashboard .flow-row th { width: 31%; }
  .rf-dashboard .flow-row .bar-cell { width: 17%; }
  .rf-dashboard .flow-row .value-cell { width: 52%; }
  .rf-dashboard .flow-reference { white-space: normal; }
}
"""


def _nulo(valor: Any) -> bool:
    if valor is None:
        return True
    try:
        return bool(pd.isna(valor))
    except (TypeError, ValueError):
        return False


def _decimal(valor: Any) -> Decimal | None:
    if _nulo(valor):
        return None
    try:
        if isinstance(valor, Decimal):
            return valor
        return Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _inteiro(valor: Any) -> int | None:
    numero = _decimal(valor)
    if numero is None or numero != numero.to_integral_value():
        return None
    return int(numero)


def _texto(valor: Any, ausente: str = "Não disponível") -> str:
    if _nulo(valor):
        return ausente
    texto = str(valor).strip()
    return texto or ausente


def _e(valor: Any, ausente: str = "Não disponível") -> str:
    return escape(_texto(valor, ausente), quote=True)


def _numero_br(numero: Decimal, casas: int) -> str:
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "\u0000").replace(".", ",").replace("\u0000", ".")


def _moeda(valor: Any, ausente: str = "Não disponível") -> str:
    numero = _decimal(valor)
    if numero is None:
        return ausente
    sinal = "− " if numero < 0 else ""
    return f"{sinal}R$ {_numero_br(abs(numero), 2)}"


def _percentual(valor: Any, ausente: str = "Não calculado") -> str:
    numero = _decimal(valor)
    if numero is None:
        return ausente
    return f"{_numero_br(numero * Decimal('100'), 1)}%"


def _contagem(valor: Any) -> str:
    numero = _inteiro(valor)
    if numero is None:
        return "Não disponível"
    return f"{numero:,}".replace(",", ".")


def _identificador(valor: Any) -> str:
    numero = _inteiro(valor)
    return str(numero) if numero is not None else "Não disponível"


def _data(valor: Any) -> date | None:
    if _nulo(valor):
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if hasattr(valor, "to_pydatetime"):
        convertido = valor.to_pydatetime()
        return convertido.date() if isinstance(convertido, datetime) else convertido
    texto = str(valor).strip()
    try:
        return date.fromisoformat(texto[:10])
    except ValueError:
        return None


def _data_br(valor: Any) -> str:
    convertido = _data(valor)
    return convertido.strftime("%d/%m/%Y") if convertido else "Não disponível"


def _mes_br(valor: Any) -> str:
    convertido = _data(valor)
    if convertido is None:
        return "Não disponível"
    return f"{MESES_PT_BR[convertido.month - 1]}/{convertido.year}"


def _timestamp_br(valor: Any) -> str:
    if _nulo(valor):
        return "Não disponível"
    convertido: datetime | None = None
    if isinstance(valor, datetime):
        convertido = valor
    elif hasattr(valor, "to_pydatetime"):
        candidato = valor.to_pydatetime()
        convertido = candidato if isinstance(candidato, datetime) else None
    else:
        texto = str(valor).strip().replace("Z", "+00:00")
        try:
            convertido = datetime.fromisoformat(texto)
        except ValueError:
            convertido = None
    return convertido.strftime("%d/%m/%Y às %H:%M:%S") if convertido else _texto(valor)


def _codigo(valor: Any, rotulo: str = "código") -> str:
    numero = _inteiro(valor)
    return f"{rotulo} {numero}" if numero is not None else f"{rotulo} não disponível"


def _flag(valor: Any, ausente: str = "Não definida") -> str:
    if _nulo(valor):
        return ausente
    texto = str(valor).strip().upper()
    return {"S": "Sim", "N": "Não"}.get(texto, str(valor).strip())


def _dia_base(valor: Any) -> str:
    numero = _inteiro(valor)
    especiais = {
        996: "Múltiplas contas elegíveis (996)",
        997: "Sem conta BB identificável (997)",
        999: "Conta sem data cadastrada (999)",
    }
    if numero is None:
        return "Não disponível"
    return especiais.get(numero, str(numero))


def _largura_barra(fracao: Any) -> float:
    numero = _decimal(fracao)
    if numero is None:
        return 0.0
    return max(0.0, min(100.0, float(numero * Decimal("100"))))


def _participacao(valor: Any, total: Any) -> Decimal:
    numerador = _decimal(valor) or Decimal("0")
    denominador = _decimal(total) or Decimal("0")
    if denominador <= 0:
        return Decimal("0")
    return numerador / denominador


def _pontuacao(valor: Any) -> str:
    numero = _inteiro(valor)
    return str(numero) if numero is not None else "—"


def _linhas_entradas(registro: dict[str, Any]) -> str:
    configuracao = (
        ("entrada-renda", "Renda", "VL_ENT_REN"),
        ("entrada-estorno", "Estorno", "VL_ENT_EST"),
        ("entrada-resgate", "Resgate", "VL_ENT_RESG"),
        ("entrada-outras", "Outras entradas", "VL_ENT_OUT"),
        ("entrada-credito", "Crédito", "VL_ENT_CRED"),
    )
    linhas: list[str] = []
    for chave, rotulo, campo in configuracao:
        fracao = _participacao(registro.get(campo), registro.get("VL_ENT_TOTAL"))
        percentual = _percentual(fracao, "0,0%")
        largura = _largura_barra(fracao)
        linhas.append(
            f'<tr class="flow-row" data-row-key="{chave}">'
            f'<th scope="row">{escape(rotulo)}</th>'
            f'<td class="bar-cell"><div class="track" role="img" '
            f'aria-label="{escape(rotulo)} representa {percentual} das entradas">'
            f'<span style="width:{largura:.2f}%"></span></div></td>'
            f'<td class="value-cell"><span class="flow-value" data-field="{campo}">'
            f'{escape(_moeda(registro.get(campo)))}</span></td></tr>'
            f'<tr class="future-detail-row" data-detail-for="{chave}" hidden>'
            '<td colspan="3"></td></tr>'
        )
    return "".join(linhas)


def _linhas_saidas(registro: dict[str, Any]) -> str:
    configuracao = (
        ("saida-indeterminado", "Indeterminado", "VL_SAI_IND", "PC_SAI_IND", "PC_REF_IND"),
        ("saida-essenciais", "Essenciais", "VL_SAI_ESS", "PC_SAI_ESS", "PC_REF_ESS"),
        ("saida-flexiveis", "Flexíveis", "VL_SAI_FLEX", "PC_SAI_FLEX", "PC_REF_FLEX"),
        ("saida-futuro", "Futuro", "VL_SAI_FUT", "PC_SAI_FUT", "PC_REF_FUT"),
        ("saida-obrigacoes", "Obrigações", "VL_SAI_OBR", "PC_SAI_OBR", "PC_REF_OBR"),
    )
    linhas: list[str] = []
    for chave, rotulo, campo_valor, campo_pc, campo_ref in configuracao:
        percentual = registro.get(campo_pc)
        referencia = registro.get(campo_ref)
        numero_pc = _decimal(percentual)
        numero_ref = _decimal(referencia)
        acima = numero_pc is not None and numero_ref is not None and numero_pc > numero_ref
        classe = "flow-row attention" if acima else "flow-row"
        estado = '<span class="flow-state">Acima da referência</span>' if acima else ""
        descricao = f"{rotulo} equivale a {_percentual(percentual)} das entradas"
        if acima:
            descricao += ", acima da referência"
        linhas.append(
            f'<tr class="{classe}" data-row-key="{chave}">'
            f'<th scope="row">{escape(rotulo)}</th>'
            f'<td class="bar-cell"><div class="track" role="img" aria-label="{escape(descricao)}">'
            f'<span style="width:{_largura_barra(percentual):.2f}%"></span></div></td>'
            f'<td class="value-cell"><span class="flow-value" data-field="{campo_valor}">'
            f'{escape(_moeda(registro.get(campo_valor)))}</span>'
            f'<span class="flow-reference"><span data-field="{campo_pc}">'
            f'{escape(_percentual(percentual))}</span> · referência '
            f'<span data-field="{campo_ref}">{escape(_percentual(referencia))}</span></span>'
            f'{estado}</td></tr>'
            f'<tr class="future-detail-row" data-detail-for="{chave}" hidden>'
            '<td colspan="3"></td></tr>'
        )
    return "".join(linhas)


def _temas(registro: dict[str, Any]) -> tuple[str, str]:
    configuracao = (
        (1, "Categorização dos gastos", "NR_PONT_CONC_IND", "NR_PONT_ORC_IND", "NR_PONT_PRFL_IND", "NR_PONT_IND_FIM"),
        (2, "Gestão de orçamento", "NR_PONT_CONC_ESS", "NR_PONT_ORC_ESS", "NR_PONT_PRFL_ESS", "NR_PONT_ESS_FIM"),
        (3, "Consumo planejado", "NR_PONT_CONC_FLEX", "NR_PONT_ORC_FLEX", "NR_PONT_PRFL_FLEX", "NR_PONT_FLEX_FIM"),
        (4, "Formação de reserva", "NR_PONT_CONC_FUT", "NR_PONT_ORC_FUT", "NR_PONT_PRFL_FUT", "NR_PONT_FUT_FIM"),
        (5, "Uso consciente do crédito", "NR_PONT_CONC_OBR", "NR_PONT_ORC_OBR", "NR_PONT_PRFL_OBR", "NR_PONT_OBR_FIM"),
    )
    codigo_vencedor = _inteiro(registro.get("CD_TEMA_VENCEDOR"))
    finais = {codigo: _inteiro(registro.get(campo_final)) for codigo, _, _, _, _, campo_final in configuracao}
    selecionados: set[int] = set()
    if codigo_vencedor in finais:
        selecionados.add(codigo_vencedor)
    elif codigo_vencedor == 9:
        preenchidos = [valor for valor in finais.values() if valor is not None]
        if preenchidos:
            maior = max(preenchidos)
            selecionados = {codigo for codigo, valor in finais.items() if valor == maior}

    linhas: list[str] = []
    for codigo, rotulo, campo_conc, campo_orc, campo_perfil, campo_final in configuracao:
        selecionado = codigo in selecionados
        classe = ' class="selected"' if selecionado else ""
        if selecionado:
            texto_selo = "Empatado" if codigo_vencedor == 9 else "Tema vencedor"
            selo = f'<span class="winner-label">{texto_selo}</span>'
            final = f'<span>{_pontuacao(registro.get(campo_final))}</span>'
        else:
            selo = ""
            final = _pontuacao(registro.get(campo_final))
        linhas.append(
            f'<tr{classe}><th scope="row">{escape(rotulo)} {selo}</th>'
            f'<td data-label="Concentração" data-field="{campo_conc}">{_pontuacao(registro.get(campo_conc))}</td>'
            f'<td data-label="Orçamento" data-field="{campo_orc}">{_pontuacao(registro.get(campo_orc))}</td>'
            f'<td data-label="Perfil" data-field="{campo_perfil}">{_pontuacao(registro.get(campo_perfil))}</td>'
            f'<td class="final-score" data-label="Final" data-field="{campo_final}">{final}</td></tr>'
        )

    texto_vencedor = _e(registro.get("TX_TEMA_VENCEDOR"), "Tema não calculado")
    codigo_formatado = escape(_codigo(registro.get("CD_TEMA_VENCEDOR")))
    pontos = ""
    if selecionados:
        valores = [finais[codigo] for codigo in selecionados if finais[codigo] is not None]
        if valores:
            maior = max(valores)
            pontos = f" · {maior} {'ponto' if maior == 1 else 'pontos'}"
    badge = (
        f'<div class="priority-badge"><span data-field="TX_TEMA_VENCEDOR">{texto_vencedor}</span>'
        f' · <span data-field="CD_TEMA_VENCEDOR">{codigo_formatado}</span>{pontos}</div>'
    )
    return badge, "".join(linhas)


def render_dashboard(registro: dict[str, Any]) -> str:
    """Monta o HTML do dashboard para uma única linha ANA_EDU_FIN_CLI."""
    identificador = uuid4().hex
    cliente_title = f"cliente-title-{identificador}"
    resultado_title = f"resultado-title-{identificador}"
    entradas_title = f"entradas-title-{identificador}"
    saidas_title = f"saidas-title-{identificador}"
    temas_title = f"temas-title-{identificador}"

    valor_resultado = _decimal(registro.get("VL_RES_ORC"))
    classe_resultado = " negative" if valor_resultado is not None and valor_resultado < 0 else ""
    if valor_resultado is not None and valor_resultado > 0:
        classe_resultado = " positive"

    renda_disponivel = not _nulo(registro.get("VL_REN_PRES"))
    radar_definido = not _nulo(registro.get("FL_PARTICIPA_RADAR"))
    badge_tema, linhas_temas = _temas(registro)

    return f"""
<style>{_CSS}</style>
<div class="rf-dashboard" id="rf-dashboard-{identificador}">
  <main class="page">
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark">RF</div>
        <div><h1>Radar Financeiro</h1><p>Visão única do cliente</p></div>
      </div>
      <div class="updated">Última atualização das transações
        <strong data-field="TS_ATL_TRAN">{escape(_timestamp_br(registro.get('TS_ATL_TRAN')))}</strong>
      </div>
    </header>

    <div class="stack">
      <section class="panel" aria-labelledby="{cliente_title}">
        <div class="panel-inner">
          <header class="section-head">
            <div><span class="eyebrow">Cliente</span><h2 id="{cliente_title}">Contexto da análise</h2><p>Identificação, perfil e período em uma leitura rápida.</p></div>
          </header>
          <div class="client-overview">
            <div class="info-card"><span class="info-label">Cliente</span><strong class="info-value" data-field="CD_CLI">{escape(_identificador(registro.get('CD_CLI')))}</strong></div>
            <div class="info-card primary"><span class="info-label">Perfil financeiro</span><strong class="info-value" data-field="NM_PRFL_FIN">{_e(registro.get('NM_PRFL_FIN'))}</strong></div>
            <div class="info-card">
              <span class="info-label">Período analisado</span>
              <div class="period"><span data-field="DT_REF_INI">{escape(_data_br(registro.get('DT_REF_INI')))}</span><i aria-hidden="true"></i><span data-field="DT_REF_FIM">{escape(_data_br(registro.get('DT_REF_FIM')))}</span></div>
            </div>
          </div>
          <div class="context-grid">
            <div class="context-card"><span>Perfil macro</span><strong data-field="NM_MAC_PRFL_CLI">{_e(registro.get('NM_MAC_PRFL_CLI'))}</strong><small data-field="CD_MAC_PRFL_CLI">{escape(_codigo(registro.get('CD_MAC_PRFL_CLI')))}</small></div>
            <div class="context-card"><span>Perfil micro</span><strong data-field="NM_MIC_PRFL_CLI">{_e(registro.get('NM_MIC_PRFL_CLI'))}</strong><small data-field="CD_MIC_PRFL_CLI">{escape(_codigo(registro.get('CD_MIC_PRFL_CLI')))}</small></div>
            <div class="context-card"><span>Mês de execução</span><strong data-field="DT_MES_EXEA">{escape(_mes_br(registro.get('DT_MES_EXEA')))}</strong></div>
            <div class="context-card"><span>Data de execução</span><strong data-field="DT_EXEA">{escape(_data_br(registro.get('DT_EXEA')))}</strong></div>
            <div class="context-card"><span>Dia-base do cálculo</span><strong data-field="DD_INC_MM_CLC_BLC">{escape(_dia_base(registro.get('DD_INC_MM_CLC_BLC')))}</strong></div>
            <div class="context-card"><span>Movimentação agro</span><strong data-field="FL_TEM_MOV_AGRO">{escape(_flag(registro.get('FL_TEM_MOV_AGRO')))}</strong></div>
            <div class="context-card{' pending' if not renda_disponivel else ''}"><span>Renda presumida</span><strong data-field="VL_REN_PRES">{escape(_moeda(registro.get('VL_REN_PRES'), 'Não disponível'))}</strong>{'<small>Integração futura</small>' if not renda_disponivel else ''}</div>
            <div class="context-card{' pending' if not radar_definido else ''}"><span>Participação no Radar</span><strong data-field="FL_PARTICIPA_RADAR">{escape(_flag(registro.get('FL_PARTICIPA_RADAR')))}</strong>{'<small>Regra futura</small>' if not radar_definido else ''}</div>
          </div>
        </div>
      </section>

      <section class="panel" aria-labelledby="{resultado_title}">
        <div class="panel-inner">
          <header class="section-head">
            <div><span class="eyebrow">Financeiro</span><h2 id="{resultado_title}">Resultado do período</h2><p>Resumo técnico, classificação e distribuição dos movimentos.</p></div>
          </header>
          <div class="metric-grid">
            <div class="metric-card positive">
              <span>Entradas nas transações</span><strong data-field="VL_TRANS_ENT">{escape(_moeda(registro.get('VL_TRANS_ENT')))}</strong>
              <small><b data-field="QT_TRANS_ENT">{escape(_contagem(registro.get('QT_TRANS_ENT')))} transações</b> de entrada</small>
            </div>
            <div class="metric-card">
              <span>Saídas nas transações</span><strong data-field="VL_TRANS_SAI">{escape(_moeda(registro.get('VL_TRANS_SAI')))}</strong>
              <small><b data-field="QT_TRANS_SAI">{escape(_contagem(registro.get('QT_TRANS_SAI')))} transações</b> de saída</small>
            </div>
            <div class="metric-card{classe_resultado}">
              <span>Resultado orçamentário</span><strong data-field="VL_RES_ORC">{escape(_moeda(registro.get('VL_RES_ORC'), 'Não calculado'))}</strong>
              <small data-field="TX_STS_FINAL">{_e(registro.get('TX_STS_FINAL'), 'Não calculado')}</small>
            </div>
            <div class="metric-card">
              <span>Movimentação total</span><strong data-field="QT_TRANS_TOTAL">{escape(_contagem(registro.get('QT_TRANS_TOTAL')))}</strong>
              <small>Saídas equivalem a <b data-field="PC_SAI_ENT">{escape(_percentual(registro.get('PC_SAI_ENT')))}</b> das entradas</small>
            </div>
          </div>
          <div class="status-row" aria-label="Classificações do resultado">
            <span class="chip"><strong>Situação:</strong> <span data-field="TX_RES_ORC">{_e(registro.get('TX_RES_ORC'), 'Não calculada')}</span> · <span data-field="CD_RES_ORC">{escape(_codigo(registro.get('CD_RES_ORC')))}</span></span>
            <span class="chip"><strong>Intensidade:</strong> <span data-field="TX_STS_RES">{_e(registro.get('TX_STS_RES'), 'Não calculada')}</span> · <span data-field="CD_FAIXA_ORC">{escape(_codigo(registro.get('CD_FAIXA_ORC'), 'faixa'))}</span></span>
          </div>
          <div class="flow-grid">
            <article class="flow-card entries" aria-labelledby="{entradas_title}">
              <header class="flow-card-head">
                <div><h3 id="{entradas_title}">Entradas</h3><p>De onde vieram os recursos no período.</p></div>
                <div class="flow-total"><span>Total classificado</span><strong data-field="VL_ENT_TOTAL">{escape(_moeda(registro.get('VL_ENT_TOTAL')))}</strong></div>
              </header>
              <table class="flow-table">
                <caption>Composição das entradas classificadas</caption>
                <thead><tr><th scope="col">Classificação</th><th scope="col">Participação</th><th scope="col">Valor</th></tr></thead>
                <tbody>{_linhas_entradas(registro)}</tbody>
              </table>
            </article>
            <article class="flow-card" aria-labelledby="{saidas_title}">
              <header class="flow-card-head">
                <div><h3 id="{saidas_title}">Saídas</h3><p>Como os gastos estão distribuídos.</p></div>
                <div class="flow-total"><span>Total classificado</span><strong data-field="VL_SAI_TOTAL">{escape(_moeda(registro.get('VL_SAI_TOTAL')))}</strong></div>
              </header>
              <table class="flow-table">
                <caption>Composição das saídas classificadas</caption>
                <thead><tr><th scope="col">Classificação</th><th scope="col">% das entradas</th><th scope="col">Valor e referência</th></tr></thead>
                <tbody>{_linhas_saidas(registro)}</tbody>
              </table>
            </article>
          </div>
        </div>
      </section>

      <section class="panel" aria-labelledby="{temas_title}">
        <div class="panel-inner">
          <header class="section-head">
            <div><span class="eyebrow">Educação financeira</span><h2 id="{temas_title}">Temas prioritários</h2><p>Os componentes formam a prioridade educacional do cliente.</p></div>
            {badge_tema}
          </header>
          <div class="theme-table-wrap">
            <table class="theme-table">
              <caption>Pontuações por tema de educação financeira</caption>
              <thead><tr><th scope="col">Tema</th><th scope="col">Concentração</th><th scope="col">Orçamento</th><th scope="col">Perfil</th><th scope="col">Final</th></tr></thead>
              <tbody>{linhas_temas}</tbody>
            </table>
          </div>
          <p class="note">Quanto maior a pontuação, maior a prioridade educacional. O componente “Indeterminado” utiliza uma escala técnica especial de 0/99.</p>
        </div>
      </section>
    </div>
  </main>
</div>
"""


__all__ = ["render_dashboard"]
