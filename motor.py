"""Motor do fluxo de geracao."""

from __future__ import annotations

import copy
import json
import os
import uuid
from pathlib import Path
from typing import Any, Optional, Union

from .modelos import (
    Apresentacao,
    Cenario,
    Etapa,
    Produto,
    Prompt,
    Publico,
    Resultado,
    ResultadoEtapa,
    Selecao,
    Tendencia,
    validar_catalogos,
)
from .yaml_utils import raiz_projeto


URL_GATEWAY = "https://generabb-acs.gbb.servicos.bb.com.br/gateway/agent"
CHAVES_CONFIG = ("CLIENT_ID", "UOR", "CHAVE")


def uma_linha(texto: Any) -> str:
    return " ".join(str(texto or "").split())


def limitar(texto: str, limite: int) -> str:
    texto = uma_linha(texto)

    if limite <= 0 or len(texto) <= limite:
        return texto

    return texto[: max(0, limite - 1)].rstrip() + "…"


class Genera:
    """Cliente real do gateway."""

    def __init__(
        self,
        *,
        agent_id: str = "mf-insights",
        config_path: Union[str, Path] = "config.env",
        timeout: int = 30,
    ):
        import requests
        import urllib3
        from dotenv import load_dotenv

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        load_dotenv(raiz_projeto() / config_path)

        self.requests = requests
        self.agent_id = agent_id
        self.url_gateway = URL_GATEWAY
        self.timeout = timeout
        self.conversation_id = str(uuid.uuid4())
        self.messages: list[dict[str, str]] = []
        self.last_result: Optional[dict[str, Any]] = None
        self.last_output: Optional[str] = None

    def headers(self) -> dict[str, Optional[str]]:
        return {
            "Accept": "application/json",
            "X-Client-Id": os.getenv("CLIENT_ID"),
            "UOR": os.getenv("UOR"),
            "userIdentification": os.getenv("CHAVE"),
            "Content-Type": "application/json",
        }

    def validar_config(self) -> None:
        faltantes = [chave for chave in CHAVES_CONFIG if not os.getenv(chave)]

        if faltantes:
            raise RuntimeError(
                "config.env sem chaves obrigatorias para geracao: "
                + ", ".join(faltantes)
            )

    def call(
        self,
        *,
        prompt: str,
        system: str,
        template: str,
        prompt_params: Optional[dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        best_of: int = 1,
    ) -> dict[str, Any]:
        self.validar_config()

        headers = self.headers()
        mensagens = [
            {"role": "system", "content": system},
            {"role": "user", "content": template},
        ]
        mensagens.extend(copy.deepcopy(self.messages))
        mensagens.append({"role": "user", "content": prompt})

        payload = {
            "action": "conversar",
            "agent_id": self.agent_id,
            "body": {
                "data": {
                    "input": prompt,
                    "context": {
                        "conversation_id": self.conversation_id,
                        "messages": mensagens,
                    },
                    "prompt_params": prompt_params or {},
                    "config": {
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "top_p": top_p,
                        "frequency_penalty": frequency_penalty,
                        "presence_penalty": presence_penalty,
                        "best_of": best_of,
                    },
                }
            },
        }

        try:
            response = self.requests.post(
                self.url_gateway,
                headers=headers,
                json=payload,
                verify=False,
                timeout=self.timeout,
            )
            status = response.status_code
            response_headers = dict(response.headers)

            try:
                body = response.json()
            except Exception:
                body = response.text

        except Exception as erro:
            status = None
            response_headers = {}
            body = {"erro": str(erro)}

        output = None

        try:
            output = body["data"]["output"]["text"][0]
        except Exception:
            output = None

        if output is not None:
            self.messages.append({"role": "user", "content": prompt})
            self.messages.append({"role": "assistant", "content": output})

        resultado = {
            "output": output,
            "request_headers": copy.deepcopy(headers),
            "request_payload": copy.deepcopy(payload),
            "response_status": status,
            "response_headers": response_headers,
            "response_body": body,
        }

        self.last_result = resultado
        self.last_output = output
        return resultado

    def reset(self) -> None:
        self.conversation_id = str(uuid.uuid4())
        self.messages = []
        self.last_result = None
        self.last_output = None

    def historico(self) -> list[dict[str, str]]:
        return self.messages

    def exibir_historico(self) -> None:
        print(json.dumps(self.messages, indent=4, ensure_ascii=False))

    def ultima_resposta(self) -> Optional[str]:
        return self.last_output

    def ultimo_resultado(self) -> Optional[dict[str, Any]]:
        return self.last_result


class Simulador:
    """Cliente falso para rodar o fluxo sem gateway."""

    def call(
        self,
        *,
        etapa_id: str,
        prompt: str,
        system: str,
        template: str,
        valores: dict[str, Any],
        limite_tagline: int = 120,
        limite_headline: int = 60,
        **_: Any,
    ) -> dict[str, Any]:
        output = self.simular(
            etapa_id,
            valores,
            limite_tagline=limite_tagline,
            limite_headline=limite_headline,
        )

        return {
            "output": output,
            "request_headers": {},
            "request_payload": {
                "prompt": prompt,
                "system": system,
                "template": template,
                "valores": valores,
            },
            "response_status": "simulado",
            "response_headers": {},
            "response_body": {"simulado": True, "etapa": etapa_id},
        }

    def simular(
        self,
        etapa_id: str,
        valores: dict[str, Any],
        *,
        limite_tagline: int,
        limite_headline: int,
    ) -> str:
        if etapa_id == "revisor_textual":
            return uma_linha(valores["PH_APRESENTACAO"])
        if etapa_id == "copywriter":
            return uma_linha(valores["PH_APRESENTACAO_REVISADA"])
        if etapa_id == "tendencia_cognitiva":
            return uma_linha(valores["PH_BASE_SEM_VIES"])
        if etapa_id == "voz_bb":
            return uma_linha(valores["PH_BASE_COM_VIES"])
        if etapa_id == "tagline":
            return limitar(valores["PH_BASE_BB"], limite_tagline)
        if etapa_id == "headline":
            return limitar(valores["PH_TEXTO"], limite_headline)
        if etapa_id == "cta":
            return "Avaliar proposta"

        return uma_linha(next(iter(valores.values()), ""))


ETAPAS = [
    Etapa("revisor_textual", "Revisão textual", "1_revisor_textual", "PH_APRESENTACAO_REVISADA", "PH_APRESENTACAO"),
    Etapa("copywriter", "Copywriting pelo cenário", "2_copywriter", "PH_BASE_SEM_VIES", "PH_APRESENTACAO_REVISADA", temperature=0.7, max_tokens=700),
    Etapa("tendencia_cognitiva", "Tendência cognitiva", "3_tendencia_cognitiva", "PH_BASE_COM_VIES", "PH_BASE_SEM_VIES", temperature=0.7, max_tokens=700),
    Etapa("voz_bb", "Voz institucional BB", "4_voz_BB", "PH_BASE_BB", "PH_BASE_COM_VIES", temperature=0.5, max_tokens=700),
    Etapa("tagline", "Tagline", "5_tagline", "PH_TEXTO", "PH_BASE_BB", temperature=0.7, max_tokens=180),
    Etapa("headline", "Headline", "6_headline", "PH_TITULO", "PH_TEXTO", temperature=0.7, max_tokens=120),
    Etapa("cta", "CTA", "7_cta", "PH_CTA", "PH_TITULO", temperature=0.6, max_tokens=60),
]


def carregar_selecao(selecao: Selecao) -> dict[str, Any]:
    return {
        "produto": Produto(selecao.produto),
        "publico": Publico(selecao.publico),
        "apresentacao": Apresentacao(selecao.apresentacao),
        "cenario": Cenario(selecao.cenario),
        "tendencia": Tendencia(selecao.tendencia),
    }


def contexto_inicial(
    selecao: Selecao,
    objetos: Optional[dict[str, Any]] = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    objetos = objetos or carregar_selecao(selecao)
    apresentacao = objetos["apresentacao"].montar(
        objetos["produto"],
        objetos["publico"],
    )

    contexto = {
        "PH_APRESENTACAO": apresentacao["texto"],
        "PH_LIMITE_CARACTER_TEXTO": str(selecao.limite_tagline),
        "PH_LIMITE_CARACTER_TITULO": str(selecao.limite_headline),
    }

    return contexto, apresentacao


def valores_etapa(
    etapa_id: str,
    contexto: dict[str, Any],
    objetos: dict[str, Any],
) -> dict[str, Any]:
    cenario = objetos["cenario"]
    tendencia = objetos["tendencia"]

    if etapa_id == "revisor_textual":
        return {"PH_APRESENTACAO": contexto["PH_APRESENTACAO"]}
    if etapa_id == "copywriter":
        return {
            "PH_APRESENTACAO_REVISADA": contexto["PH_APRESENTACAO_REVISADA"],
            "PH_CENARIO_FUNCAO": cenario.funcao_prompt,
            "PH_CENARIO_DESCRICAO": cenario.texto_prompt,
        }
    if etapa_id == "tendencia_cognitiva":
        return {
            "PH_BASE_SEM_VIES": contexto["PH_BASE_SEM_VIES"],
            "PH_VIES_FUNCAO": tendencia.funcao_prompt,
            "PH_VIES_DESCRICAO": tendencia.texto_prompt,
        }
    if etapa_id == "voz_bb":
        return {"PH_BASE_COM_VIES": contexto["PH_BASE_COM_VIES"]}
    if etapa_id == "tagline":
        return {
            "PH_BASE_BB": contexto["PH_BASE_BB"],
            "PH_LIMITE_CARACTER_TEXTO": contexto["PH_LIMITE_CARACTER_TEXTO"],
        }
    if etapa_id == "headline":
        return {
            "PH_BASE_BB": contexto["PH_BASE_BB"],
            "PH_TEXTO": contexto["PH_TEXTO"],
            "PH_LIMITE_CARACTER_TITULO": contexto["PH_LIMITE_CARACTER_TITULO"],
        }
    if etapa_id == "cta":
        return {
            "PH_BASE_BB": contexto["PH_BASE_BB"],
            "PH_TITULO": contexto["PH_TITULO"],
            "PH_TEXTO": contexto["PH_TEXTO"],
        }

    raise ValueError(f"Etapa desconhecida: {etapa_id}")


def rodar_fluxo(selecao: Selecao, *, modo: str = "simulacao") -> Resultado:
    objetos = carregar_selecao(selecao)
    contexto, apresentacao = contexto_inicial(selecao, objetos)
    resultados: list[ResultadoEtapa] = []
    modo = modo.lower().strip()

    if modo not in {"simulacao", "real"}:
        raise ValueError("modo deve ser 'simulacao' ou 'real'.")

    cliente = Simulador() if modo == "simulacao" else Genera()

    for etapa in ETAPAS:
        prompt_nome = selecao.prompt_revisor if etapa.id == "revisor_textual" else etapa.prompt_nome
        prompt = Prompt(etapa.grupo_prompt, prompt_nome)
        valores = valores_etapa(etapa.id, contexto, objetos)
        template = prompt.montar(valores)
        entrada = str(valores[etapa.entrada])

        if modo == "simulacao":
            bruto = cliente.call(
                etapa_id=etapa.id,
                prompt=entrada,
                system=prompt.system,
                template=template,
                valores=valores,
                limite_tagline=selecao.limite_tagline,
                limite_headline=selecao.limite_headline,
                temperature=etapa.temperature,
                max_tokens=etapa.max_tokens,
            )
        else:
            bruto = cliente.call(
                prompt=entrada,
                system=prompt.system,
                template=template,
                temperature=etapa.temperature,
                max_tokens=etapa.max_tokens,
            )

        output = bruto.get("output")

        if output is None:
            raise RuntimeError(f"A etapa '{etapa.titulo}' nao retornou output.")

        contexto[etapa.saida] = str(output)

        resultados.append(
            ResultadoEtapa(
                id=etapa.id,
                titulo=etapa.titulo,
                prompt=f"{etapa.grupo_prompt}/{prompt_nome}",
                system=prompt.system,
                template=template,
                entrada=entrada,
                output=str(output),
                bruto=bruto,
                simulado=modo == "simulacao",
            )
        )

    return Resultado(
        selecao=selecao,
        apresentacao_visual=apresentacao["visual"],
        apresentacao_texto=apresentacao["texto"],
        placeholders=apresentacao["placeholders"],
        contexto=contexto,
        etapas=resultados,
    )
