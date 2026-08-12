"""Apresentacao HTML do Dashboard Financeiro V1."""
from __future__ import annotations

import json
from typing import Any
from uuid import uuid4


class Visual:
    """Estilo incorporado do dashboard, sem dependencias visuais externas."""

    @staticmethod
    def aplicar_estilo() -> str:
        return r"""
.fin-dashboard{font-family:Inter,Segoe UI,Arial,sans-serif;color:#172033;background:#f5f7fb;border:1px solid #dfe5ef;border-radius:18px;padding:22px;line-height:1.4}
.fin-dashboard *{box-sizing:border-box}.fin-dashboard h2,.fin-dashboard h3,.fin-dashboard p{margin:0}
.fin-header{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:18px}.fin-header h2{font-size:24px}.fin-muted{color:#647089;font-size:13px}.fin-context{display:grid;grid-template-columns:minmax(130px,.7fr) minmax(240px,1.6fr) minmax(160px,1fr) minmax(180px,1fr);gap:10px;margin:14px 0 18px}.fin-context>div,.fin-panel{background:#fff;border:1px solid #e2e7f0;border-radius:12px;padding:12px}.fin-label{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#6d7890}.fin-value{font-size:15px;font-weight:700;margin-top:4px;overflow-wrap:anywhere}.fin-context-list{display:grid;gap:3px;margin-top:4px}.fin-context-secondary{font-size:12px;color:#647089;font-weight:600}
.fin-filters{display:grid;grid-template-columns:repeat(3,minmax(150px,1fr)) auto;gap:10px;align-items:end}.fin-field label{display:block;font-size:12px;font-weight:700;color:#505c73;margin-bottom:5px}.fin-field select,.fin-clear{width:100%;height:38px;border:1px solid #cfd7e5;border-radius:9px;background:#fff;padding:0 10px;color:#172033}.fin-clear{cursor:pointer;font-weight:700}.fin-chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}.fin-chip{background:#edf2ff;color:#244a9b;border-radius:999px;padding:5px 10px;font-size:12px}
.fin-section-title{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:#536079;margin:22px 0 10px}.fin-summary{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.fin-summary details,.fin-card{background:#fff;border:1px solid #dde4ef;border-radius:14px;overflow:hidden}.fin-summary summary,.fin-card>summary,.fin-category summary{list-style:none;cursor:pointer;position:relative;padding-right:42px}.fin-summary summary,.fin-card>summary{padding:15px 42px 15px 15px}.fin-summary summary::-webkit-details-marker,.fin-card>summary::-webkit-details-marker,.fin-category summary::-webkit-details-marker{display:none}.fin-summary summary::after,.fin-card>summary::after,.fin-category summary::after{content:"\25BC";position:absolute;right:15px;top:50%;transform:translateY(-50%);color:#5d6b83;font-size:12px;transition:transform .18s ease}.fin-summary details[open]>summary::after,.fin-card[open]>summary::after,.fin-category[open]>summary::after{transform:translateY(-50%) rotate(180deg)}.fin-summary-name{font-size:13px;color:#59657a}.fin-summary-value{font-size:23px;font-weight:800;margin-top:5px}.fin-summary-qty{font-size:12px;color:#738097;margin-top:2px}.fin-explanation{padding:0 15px 15px;color:#4d596f;font-size:13px}.fin-pair{border-top:1px solid #edf0f5;padding:11px 0}.fin-pair-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.fin-pair-box{background:#f7f9fc;border-radius:9px;padding:9px}
.fin-toolbar{display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap}.fin-toggle{display:inline-flex;border:1px solid #cfd7e5;border-radius:10px;overflow:hidden;background:#fff}.fin-toggle button{border:0;background:#fff;padding:9px 14px;cursor:pointer;color:#526078;font-weight:700}.fin-toggle button.active{background:#173f8f;color:#fff}.fin-analysis-total{display:flex;justify-content:space-between;align-items:center;gap:12px;background:#fff;border:1px solid #dde4ef;border-radius:12px;padding:13px 15px;margin:12px 0}.fin-analysis-total strong{font-size:19px}.fin-analysis-total span{font-size:12px;color:#738097}.fin-diagnostic{margin:12px 0;border-radius:10px;padding:11px 13px;font-size:13px}.fin-diagnostic.ok{background:#eaf7ef;color:#176238}.fin-diagnostic.error{background:#fff0f0;color:#9b1c1c;border:1px solid #f4c7c7}
.fin-analytics{display:grid;gap:10px}.fin-card-head{display:flex;justify-content:space-between;gap:12px;align-items:center}.fin-card-title{font-weight:800}.fin-card-sub{font-size:12px;color:#738097;margin-top:3px}.fin-card-money{font-size:18px;font-weight:800;text-align:right;white-space:nowrap}.fin-card-body{padding:0 15px 15px}.fin-category{border:1px solid #e6eaf1;border-radius:9px;margin-top:8px}.fin-category summary{cursor:pointer;padding:10px 42px 10px 10px;display:flex;justify-content:space-between;gap:10px}.fin-table-wrap{overflow-x:auto;margin-top:9px}.fin-table{width:100%;border-collapse:collapse;min-width:820px;font-size:12px}.fin-table th,.fin-table td{padding:8px;border-bottom:1px solid #e9edf3;text-align:left;vertical-align:top}.fin-table th{background:#f7f9fc;color:#536079;position:sticky;top:0}.fin-table .num{text-align:right;white-space:nowrap}.fin-table tfoot td{font-weight:800;background:#f7f9fc}.fin-empty{background:#fff;border:1px dashed #cbd4e3;border-radius:12px;padding:24px;text-align:center;color:#6b778e}.fin-hidden{display:none!important}
@media(max-width:850px){.fin-context{grid-template-columns:repeat(2,1fr)}.fin-filters{grid-template-columns:1fr 1fr}.fin-summary{grid-template-columns:1fr}.fin-pair-grid{grid-template-columns:1fr}}
@media(max-width:520px){.fin-dashboard{padding:14px}.fin-context,.fin-filters{grid-template-columns:1fr}.fin-header{display:block}.fin-toolbar{align-items:stretch}.fin-toggle{width:100%}.fin-toggle button{flex:1}}
"""


def _json_seguro(payload: dict[str, Any]) -> str:
    texto = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        texto.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def render_dashboard(payload: dict[str, Any]) -> str:
    """Renderiza o payload validado com HTML, CSS e JavaScript incorporados."""
    if not isinstance(payload, dict):
        raise TypeError("payload deve ser um dicionario.")
    identificador = f"fin-{uuid4().hex}"
    modelo = r"""
<style>__CSS__</style>
<div id="__ID__" class="fin-dashboard">
  <div class="fin-header">
    <div><h2>Dashboard Financeiro</h2><p class="fin-muted">Leitura do cliente e dos periodos financeiros carregados.</p></div>
    <div class="fin-muted" data-role="currency-status"></div>
  </div>
  <div class="fin-context" data-role="context"></div>
  <div class="fin-panel">
    <div class="fin-filters">
      <div class="fin-field"><label>Periodo</label><select data-filter="period"></select></div>
      <div class="fin-field"><label>Fonte financeira</label><select data-filter="source"></select></div>
      <div class="fin-field"><label>Moeda</label><select data-filter="currency"></select></div>
      <button class="fin-clear" type="button" data-action="clear">Limpar filtros</button>
    </div>
    <div class="fin-chips" data-role="chips"></div>
  </div>
  <div class="fin-section-title">Resumo das entradas</div>
  <div class="fin-summary" data-role="summary"></div>
  <div class="fin-section-title">Analise</div>
  <div class="fin-toolbar">
    <div class="fin-toggle" data-toggle="population"><button data-value="ENTRADAS">Entradas</button><button data-value="SAIDAS">Saidas</button></div>
    <div class="fin-toggle" data-toggle="view"><button data-value="RADAR">Radar</button><button data-value="GRUPO">Grupo</button><button data-value="CATEGORIA">Categoria</button></div>
  </div>
  <div data-role="analysis-total"></div>
  <div data-role="diagnostic"></div>
  <div class="fin-analytics" data-role="analytics"></div>
</div>
<script>
(()=>{
  "use strict";
  const root=document.getElementById("__ID__");
  const data=__PAYLOAD__;
  const byId=new Map(data.transacoes.map(x=>[x.id_transacao,x]));
  const scales=new Map(data.moedas.map(x=>[x.codigo,Number(x.escala)]));
  const initial=data.filtros_iniciais;
  const state={period:null,source:null,currency:initial.moeda,population:"ENTRADAS",view:"RADAR"};
  const $=(selector)=>root.querySelector(selector);
  const $$=(selector)=>Array.from(root.querySelectorAll(selector));
  const esc=(value)=>String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const cmpBig=(a,b)=>{const x=BigInt(a),y=BigInt(b);return x===y?0:(x>y?-1:1)};
  const sum=(rows)=>rows.reduce((acc,row)=>acc+BigInt(row.valor_unidades),0n);
  const scaleFor=(currency)=>scales.has(currency)?scales.get(currency):2;
  const formatUnits=(units,currency)=>{
    let value=BigInt(units||"0"); const negative=value<0n; if(negative)value=-value;
    const scale=scaleFor(currency); const factor=10n**BigInt(scale);
    const integer=value/factor; const fraction=(value%factor).toString().padStart(scale,"0");
    const number=scale?`${integer.toString().replace(/\B(?=(\d{3})+(?!\d))/g,".")},${fraction}`:integer.toString();
    const prefix=currency?`${esc(currency)} `:""; return `${negative?"-":""}${prefix}${number}`;
  };
  const periodLabel=(nr)=>{const p=data.periodos.find(x=>x.nr_periodo===nr);return p?`${p.ref_periodo} (${p.inicio} a ${p.fim})`:String(nr)};
  const sourceLabel=(source)=>`Fonte ${source}`;
  const option=(value,label,selected)=>`<option value="${esc(value)}"${selected?" selected":""}>${esc(label)}</option>`;

  function initialize(){
    const periodosContexto=data.periodos.length
      ?data.periodos.map(p=>`<div title="${esc(periodLabel(p.nr_periodo))}">P${p.nr_periodo} — ${esc(p.inicio)} a ${esc(p.fim)}</div>`).join("")
      :'<div>Sem periodos calculados</div>';
    const moedasContexto=data.moedas.length
      ?data.moedas.map(m=>esc(m.codigo)).join(" · ")
      :'Sem movimentacoes';
    $("[data-role=context]").innerHTML=`
      <div><div class="fin-label">Cliente</div><div class="fin-value" title="${esc(data.contexto.cd_cli)}">${esc(data.contexto.cd_cli)}</div></div>
      <div><div class="fin-label">Periodos carregados</div><div class="fin-value fin-context-list">${periodosContexto}</div></div>
      <div><div class="fin-label">Moedas observadas</div><div class="fin-value" title="${esc(moedasContexto)}">${moedasContexto}</div></div>
      <div><div class="fin-label">Contexto tecnico</div><div class="fin-context-list fin-context-secondary"><div>Origem: ${esc(data.contexto.origem_cd_cli)}</div><div>Status: ${esc(data.contexto.status)}</div><div>Visualizacao: ${esc(data.contexto.data_visualizacao)}</div></div></div>`;
    $("[data-filter=period]").innerHTML=option("TODOS","Todos os periodos",true)+data.periodos.map(p=>option(String(p.nr_periodo),periodLabel(p.nr_periodo),false)).join("");
    $("[data-filter=source]").innerHTML=option("TODAS","Todas as fontes",true)+data.fontes.map(s=>option(s,sourceLabel(s),false)).join("");
    const currency=$("[data-filter=currency]");
    currency.innerHTML=data.moedas.length?data.moedas.map(m=>option(m.codigo,m.codigo,m.codigo===state.currency)).join(""):option("","Sem movimentacoes no periodo carregado",true);
    currency.disabled=!data.moedas.length;
    $("[data-role=currency-status]").textContent=data.moedas.length?`Moeda selecionada: ${state.currency}`:"Moeda: sem movimentacoes no periodo carregado";
    $$('[data-filter]').forEach(el=>el.addEventListener("change",()=>{state.period=$("[data-filter=period]").value==="TODOS"?null:Number($("[data-filter=period]").value);state.source=$("[data-filter=source]").value==="TODAS"?null:$("[data-filter=source]").value;state.currency=$("[data-filter=currency]").value||null;render()}));
    $("[data-action=clear]").addEventListener("click",()=>{state.period=null;state.source=null;state.currency=initial.moeda;$("[data-filter=period]").value="TODOS";$("[data-filter=source]").value="TODAS";$("[data-filter=currency]").value=state.currency||"";render()});
    $$('[data-toggle=population] button').forEach(btn=>btn.addEventListener("click",()=>{state.population=btn.dataset.value;render()}));
    $$('[data-toggle=view] button').forEach(btn=>btn.addEventListener("click",()=>{state.view=btn.dataset.value;render()}));
    render();
  }
  function matches(row){return (!state.currency||row.moeda===state.currency)&&(!state.period||row.nr_periodo===state.period)&&(!state.source||row.fonte===state.source)}
  function baseRows(){return data.transacoes.filter(matches)}
  function summaryRows(){const rows=baseRows().filter(x=>x.natureza==="C"&&x.estado===0);return {identified:rows,own:rows.filter(x=>x.fl_movimentacao_propria==="S"),corrected:rows.filter(x=>x.fl_movimentacao_propria==="N")}}
  function analyticRows(){const nature=state.population==="ENTRADAS"?"C":"D";return baseRows().filter(x=>x.natureza===nature&&x.estado===0&&x.fl_movimentacao_propria==="N")}
  function renderChips(){const labels=[state.period?`Periodo: ${periodLabel(state.period)}`:"Todos os periodos",state.source?sourceLabel(state.source):"Todas as fontes",state.currency?`Moeda: ${state.currency}`:"Sem moeda"];$("[data-role=chips]").innerHTML=labels.map(x=>`<span class="fin-chip">${esc(x)}</span>`).join("")}
  function pairDetails(){
    const visibleCredits=new Set(summaryRows().own.map(x=>x.id_transacao));
    const pairs=data.pares_movimentacao_propria.filter(p=>visibleCredits.has(p.credito_id));
    if(!pairs.length)return '<div class="fin-explanation">Nenhuma movimentacao propria no recorte.</div>';
    return `<div class="fin-explanation">${pairs.map(p=>{
      const c=byId.get(p.credito_id),d=byId.get(p.debito_id);
      const motivos={MATCH_MESMO_DIA:"movimentacoes observadas no mesmo dia",MATCH_1_DIA:"movimentacoes em datas com diferenca de 1 dia",MATCH_2_DIAS:"movimentacoes em datas com diferenca de 2 dias",MATCH_3_DIAS:"movimentacoes em datas com diferenca de 3 dias"};
      const candidatos=p.qt_candidatos>1?`<div class="fin-muted">Foram encontradas ${p.qt_candidatos} movimentacoes compativeis. A associacao apresentada e a selecionada deterministicamente pelo algoritmo; as demais alternativas nao sao consideradas incorretas e a origem real nao e afirmada como comprovada.</div>`:"";
      return `<div class="fin-pair"><div class="fin-pair-grid"><div class="fin-pair-box"><strong>Credito observado</strong><br>${formatUnits(c.valor_unidades,c.moeda)} · ${esc(sourceLabel(c.fonte))} · ${esc(c.data)}<br>${esc(periodLabel(c.nr_periodo))}<br><span title="${esc(c.descricao)}">${esc(c.descricao)}</span></div><div class="fin-pair-box"><strong>Debito considerado compativel</strong><br>${formatUnits(d.valor_unidades,d.moeda)} · ${esc(sourceLabel(d.fonte))} · ${esc(d.data)}<br>${esc(periodLabel(d.nr_periodo))}<br><span title="${esc(d.descricao)}">${esc(d.descricao)}</span></div></div><div class="fin-muted">Diferenca: ${p.diferenca_dias} dia(s) · Evidencia: ${esc(p.nivel_evidencia)} · Candidatos disponiveis: ${p.qt_candidatos}</div><div class="fin-muted">Associacao utilizada: ${esc(motivos[p.motivo]||"regra temporal compativel")}<br>Codigo tecnico: ${esc(p.motivo)}</div>${candidatos}</div>`;
    }).join("")}</div>`;
  }
  function renderSummary(){
    const r=summaryRows();
    const cards=[
      {name:"Entradas identificadas",rows:r.identified,text:"Todos os creditos efetivados observados no recorte."},
      {name:"Movimentacao propria",rows:r.own,text:"Creditos com debito compativel selecionado pelo algoritmo.",pairs:true},
      {name:"Entradas corrigidas",rows:r.corrected,text:"Entradas identificadas menos as provaveis movimentacoes proprias."}
    ];
    $("[data-role=summary]").innerHTML=cards.map(c=>`<details><summary><div class="fin-summary-name">${esc(c.name)}</div><div class="fin-summary-value">${formatUnits(sum(c.rows),state.currency)}</div><div class="fin-summary-qty">${c.rows.length} movimentacao(oes)</div></summary>${c.pairs?pairDetails():`<div class="fin-explanation">${esc(c.text)}${tableTransactions(c.rows)}</div>`}</details>`).join("");
  }
  function control(){return data.controles.find(x=>x.moeda===state.currency&&x.nr_periodo===state.period&&x.fonte===state.source)||null}
  function renderAnalysisTotal(rows){
    const label=state.population==="ENTRADAS"?"Entradas analisadas":"Saidas analisadas";
    $("[data-role=analysis-total]").innerHTML=`<div class="fin-analysis-total"><div><div class="fin-label">${esc(label)}</div><span>${rows.length} movimentacao(oes)</span></div><strong>${formatUnits(sum(rows),state.currency)}</strong></div>`;
  }
  function renderDiagnostic(validation){
    if(validation.ok){
      const mensagem=state.currency?"Valores e quantidades reconciliados para o recorte.":"Sem movimentacoes para reconciliar.";
      $("[data-role=diagnostic]").innerHTML=`<div class="fin-diagnostic ok">${esc(mensagem)}</div>`;
      return;
    }
    const detalhes=validation.issues.map(item=>`<li><strong>${esc(item.etapa)}</strong>: ${esc(item.detalhe)}</li>`).join("");
    $("[data-role=diagnostic]").innerHTML=`<div class="fin-diagnostic error"><strong>Erro de reconciliacao dos dados</strong><br>O total e os cards analiticos foram bloqueados.<ul>${detalhes}</ul></div>`;
  }
  function tableTransactions(rows){
    const ordered=[...rows].sort((a,b)=>a.data.localeCompare(b.data)||a.id_transacao.localeCompare(b.id_transacao));
    if(!ordered.length)return '<div class="fin-empty">Nenhuma transacao neste agrupamento.</div>';
    const body=ordered.map(x=>`<tr title="NR_TRAN_INST_PCT: ${esc(x.id_transacao)}"><td>${esc(x.data)}</td><td title="${esc(sourceLabel(x.fonte))}">${esc(sourceLabel(x.fonte))}</td><td title="${esc(x.grupo_descricao)}">${esc(x.grupo_descricao)}</td><td title="${esc(x.categoria_descricao)}">${esc(x.categoria_descricao)}</td><td title="${esc(x.descricao)}">${esc(x.descricao)}</td><td class="num">${formatUnits(x.valor_unidades,x.moeda)}</td></tr>`).join("");
    return `<div class="fin-table-wrap"><table class="fin-table"><thead><tr><th>Data</th><th>Fonte</th><th>Grupo</th><th>Categoria</th><th>Descricao</th><th class="num">Valor</th></tr></thead><tbody>${body}</tbody><tfoot><tr><td colspan="5">Total</td><td class="num">${formatUnits(sum(ordered),state.currency)}</td></tr></tfoot></table></div>`;
  }
  function categories(rows){
    const groups=new Map();
    rows.forEach(x=>{const key=`${x.categoria_codigo}|${x.categoria_descricao}`;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(x)});
    return Array.from(groups.entries()).map(([key,items])=>({
      key,
      label:items[0].categoria_descricao||`Categoria ${items[0].categoria_codigo}`,
      groupLabel:items[0].grupo_descricao||`Grupo ${items[0].grupo_codigo}`,
      rows:items,
      value:sum(items)
    })).sort((a,b)=>cmpBig(a.value,b.value)||a.label.localeCompare(b.label));
  }
  function compositionTable(items){
    if(!items.length)return '<div class="fin-empty">Sem categorias com transacoes.</div>';
    const body=items.map(item=>`<tr><td title="${esc(item.label)}">${esc(item.label)}</td><td title="${esc(item.groupLabel)}">${esc(item.groupLabel)}</td><td>${item.rows.length}</td><td class="num">${formatUnits(item.value,state.currency)}</td></tr>`).join("");
    const total=items.reduce((acc,item)=>acc+item.value,0n);
    return `<div class="fin-table-wrap"><table class="fin-table"><thead><tr><th>Categoria</th><th>Grupo</th><th>Quantidade</th><th class="num">Valor</th></tr></thead><tbody>${body}</tbody><tfoot><tr><td colspan="2">Total</td><td>${items.reduce((acc,item)=>acc+item.rows.length,0)}</td><td class="num">${formatUnits(total,state.currency)}</td></tr></tfoot></table></div>`;
  }
  function groupRows(rows){
    const map=new Map(); rows.forEach(x=>{let key,label;if(state.view==="RADAR"){key=String(x.radar_codigo);label=x.radar_descricao}else if(state.view==="GRUPO"){key=x.grupo_codigo;label=x.grupo_descricao}else{key=x.categoria_codigo;label=x.categoria_descricao}const full=`${key}|${label}`;if(!map.has(full))map.set(full,[]);map.get(full).push(x)});
    return Array.from(map.entries()).map(([key,items])=>({key,label:(state.view==="CATEGORIA"?items[0].categoria_descricao:(state.view==="GRUPO"?items[0].grupo_descricao:items[0].radar_descricao))||"Nao informado",rows:items,value:sum(items)})).sort((a,b)=>cmpBig(a.value,b.value)||a.label.localeCompare(b.label));
  }
  function validateAnalytics(){
    const issues=[];
    const add=(etapa,detalhe)=>issues.push({etapa,detalhe});
    const resumo=summaryRows(),rows=analyticRows(),groups=groupRows(rows),ctrl=control();
    const identified=sum(resumo.identified),own=sum(resumo.own),corrected=sum(resumo.corrected),analytic=sum(rows);

    if(identified!==own+corrected){
      add("RESUMO_ENTRADAS",`valor identificado=${identified}; proprio+corrigido=${own+corrected}`);
    }
    if(ctrl){
      const expectedValue=state.population==="ENTRADAS"?BigInt(ctrl.entradas_corrigidas_unidades):BigInt(ctrl.saidas_analisadas_unidades);
      const expectedQty=state.population==="ENTRADAS"?Number(ctrl.qt_corrigidas):Number(ctrl.qt_saidas);
      if(analytic!==expectedValue)add("POPULACAO_ANALITICA",`valor esperado=${expectedValue}; observado=${analytic}`);
      if(rows.length!==expectedQty)add("POPULACAO_ANALITICA",`quantidade esperada=${expectedQty}; observada=${rows.length}`);
      if(resumo.identified.length!==Number(ctrl.qt_identificadas))add("RESUMO_ENTRADAS",`quantidade identificada esperada=${ctrl.qt_identificadas}; observada=${resumo.identified.length}`);
      if(resumo.own.length!==Number(ctrl.qt_proprias))add("RESUMO_ENTRADAS",`quantidade propria esperada=${ctrl.qt_proprias}; observada=${resumo.own.length}`);
      if(resumo.corrected.length!==Number(ctrl.qt_corrigidas))add("RESUMO_ENTRADAS",`quantidade corrigida esperada=${ctrl.qt_corrigidas}; observada=${resumo.corrected.length}`);
    }else if(baseRows().length!==0||rows.length!==0){
      add("CONTROLE_DO_FILTRO","controle ausente para uma populacao observada");
    }

    const cardValue=groups.reduce((acc,item)=>acc+item.value,0n);
    const cardQty=groups.reduce((acc,item)=>acc+item.rows.length,0);
    if(cardValue!==analytic)add("CARDS_DA_VISAO",`valor esperado=${analytic}; observado=${cardValue}`);
    if(cardQty!==rows.length)add("CARDS_DA_VISAO",`quantidade esperada=${rows.length}; observada=${cardQty}`);

    groups.forEach(group=>{
      const transactionValue=sum(group.rows),transactionQty=group.rows.length;
      if(group.value!==transactionValue)add("CARD_TRANSACOES",`${group.label}: valor do card=${group.value}; transacoes=${transactionValue}`);
      if(state.view!=="CATEGORIA"){
        const composition=categories(group.rows);
        const compositionValue=composition.reduce((acc,item)=>acc+item.value,0n);
        const compositionQty=composition.reduce((acc,item)=>acc+item.rows.length,0);
        if(compositionValue!==group.value)add("COMPOSICAO_CATEGORIA",`${group.label}: valor do card=${group.value}; composicao=${compositionValue}`);
        if(compositionQty!==transactionQty)add("COMPOSICAO_CATEGORIA",`${group.label}: quantidade do card=${transactionQty}; composicao=${compositionQty}`);
      }
    });
    return {ok:issues.length===0,issues,rows,groups};
  }
  function renderAnalytics(groups){
    const target=$("[data-role=analytics]");
    if(!groups.length){target.innerHTML='<div class="fin-empty">Nenhuma transacao para os filtros atuais.</div>';return}
    target.innerHTML=groups.map(g=>{
      let content;
      if(state.view==="CATEGORIA"){
        content=tableTransactions(g.rows);
      }else{
        const itensCategoria=categories(g.rows);
        const detalhes=itensCategoria.map(c=>`<details class="fin-category"><summary><span title="${esc(c.label)}">${esc(c.label)} &middot; ${c.rows.length} transacao(oes)</span><strong>${formatUnits(c.value,state.currency)}</strong></summary><div class="fin-card-body">${tableTransactions(c.rows)}</div></details>`).join("");
        content=compositionTable(itensCategoria)+detalhes;
      }
      return `<details class="fin-card"><summary><div class="fin-card-head"><div><div class="fin-card-title" title="${esc(g.label)}">${esc(g.label)}</div><div class="fin-card-sub">${g.rows.length} transacao(oes)</div></div><div class="fin-card-money">${formatUnits(g.value,state.currency)}</div></div></summary><div class="fin-card-body">${content}</div></details>`;
    }).join("");
  }
  function render(){
    $$('[data-toggle=population] button').forEach(x=>x.classList.toggle("active",x.dataset.value===state.population));
    $$('[data-toggle=view] button').forEach(x=>x.classList.toggle("active",x.dataset.value===state.view));
    $("[data-role=currency-status]").textContent=state.currency?`Moeda selecionada: ${state.currency}`:"Moeda: sem movimentacoes no periodo carregado";
    renderChips();renderSummary();
    const totalTarget=$("[data-role=analysis-total]"),analyticsTarget=$("[data-role=analytics]");
    totalTarget.innerHTML="";analyticsTarget.innerHTML="";
    totalTarget.classList.add("fin-hidden");analyticsTarget.classList.add("fin-hidden");
    const validation=validateAnalytics();
    renderDiagnostic(validation);
    if(validation.ok){
      renderAnalysisTotal(validation.rows);
      renderAnalytics(validation.groups);
      totalTarget.classList.remove("fin-hidden");analyticsTarget.classList.remove("fin-hidden");
    }
  }
  initialize();
})();
</script>
"""
    return (
        modelo.replace("__CSS__", Visual.aplicar_estilo())
        .replace("__ID__", identificador)
        .replace("__PAYLOAD__", _json_seguro(payload))
    )


__all__ = ["Visual", "render_dashboard"]
