"""
ZapSign Lead Briefing Generator
==============================

This module implements a simple Streamlit application that helps sales
representatives at ZapSign generate a structured strategic briefing for
potential enterprise clients.  The idea is to capture basic
information about a prospect (company name and website) and combine
that with general market research to produce a consistent set of
insights, discovery questions and a suggested sales pitch.  Because
this environment does not allow outbound HTTP calls, the functions
that would normally perform web scraping or API requests are designed
as placeholders.  You can replace these stubs with real
implementations that query trusted databases or internal APIs.

Usage:

1. Run the app with the Streamlit CLI:

   ````bash
   streamlit run lead_briefing_site.py
   ````

2. Enter the prospect's company name and website URL.

3. Click “Gerar Briefing” to produce a report.  The current
   implementation uses static heuristics and publicly sourced
   information to build the briefing; you should replace
   ``get_company_info`` and ``generate_briefing`` with your own logic
   for production use.

Note: this code intentionally avoids external network calls because
your environment may not have internet access.  To integrate with
real‑world data sources, you can add requests to APIs such as
Clearbit, OpenCorporates or internal CRM systems.
"""

import dataclasses
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

# Importing Streamlit only when needed avoids a hard dependency when
# running the module in environments where Streamlit is not available.
try:
    import streamlit as st  # type: ignore
except ModuleNotFoundError:
    st = None  # type: ignore


@dataclass
class CompanyProfile:
    """Data class to store high‑level information about a prospect."""

    name: str
    website: str
    headquarters: Optional[str] = None
    business_segment: Optional[str] = None
    revenue: Optional[str] = None
    employees: Optional[int] = None
    units: Optional[int] = None  # Number of offices or branches


def classify_company_size(employees: Optional[int], revenue: Optional[str]) -> str:
    """Classify the company based on headcount or revenue.

    This function uses the classification criteria published by
    Exame/BNDES: micro (≤19 employees for industry or ≤9 for commerce),
    small (20–99 employees for industry, 10–49 for commerce),
    medium (100–499 industry, 50–99 commerce) and large (≥500 or
    ≥100 employees depending on the sector).  When the number of
    employees is unknown, the revenue string (if present) is returned
    verbatim; otherwise the function returns "Desconhecido".
    """
    if employees is None:
        return revenue or "Desconhecido"
    # For simplicity we assume the company operates in the industrial
    # sector; if you have sector information, adjust the thresholds.
    if employees <= 19:
        return "Microempresa"
    if 20 <= employees <= 99:
        return "Pequena empresa"
    if 100 <= employees <= 499:
        return "Média empresa"
    if employees >= 500:
        return "Grande empresa"
    return "Desconhecido"


def get_company_info(name: str, website: str) -> CompanyProfile:
    """Retrieve company information from external sources (stub).

    In a production system, this function would call external APIs or
    perform web scraping to gather basic information about the
    company, such as its headquarters location, revenue, number of
    employees, business segment and number of units.  Because this
    environment has restricted internet access, the function returns a
    dummy profile with fields left as None.

    Replace this stub with calls to services like Clearbit
    (https://clearbit.com), OpenCorporates (https://opencorporates.com) or
    your internal CRM to populate these fields automatically.
    """
    # TODO: Replace with real data retrieval logic.
    return CompanyProfile(name=name.strip(), website=website.strip())


def generate_briefing(profile: CompanyProfile) -> Dict[str, str]:
    """Generate a structured briefing based on the company profile.

    This function composes a strategic briefing using high‑level
    information about the company combined with general insights about
    digital signature adoption in Brazil.  Each section of the
    briefing corresponds to the structure requested by ZapSign:

    * Sede (headquarters)
    * Porte da empresa (company size)
    * Unidades (number of offices)
    * Total de funcionários (employee count)
    * Faturamento Anual (annual revenue)
    * Segmento de atuação (industry segment)
    * Resumo executivo
    * Tipos de documentos
    * Dores prováveis
    * Hipóteses e impacto
    * Sinais de urgência
    * Perguntas de discovery
    * Linha de abordagem e pitch
    * Abordagem comercial

    For demonstration purposes, the function uses static rules and
    publicly sourced information (see the accompanying research
    report) to fill out sections.  You can customize this logic
    depending on your target industry, the client's context and the
    data you retrieve about them.
    """
    # Classify company size
    size = classify_company_size(profile.employees, profile.revenue)

    # Build each section of the briefing
    briefing: Dict[str, str] = {}

    # Headquarters
    briefing["Sede"] = profile.headquarters or "Informação não disponível"

    # Size / company classification
    briefing["Porte da empresa"] = size

    # Units
    briefing["Unidades"] = (
        str(profile.units) if profile.units is not None else "Informação não disponível"
    )

    # Total employees
    briefing["Total de funcionários"] = (
        str(profile.employees) if profile.employees is not None else "Informação não disponível"
    )

    # Annual revenue
    briefing["Faturamento Anual"] = profile.revenue or "Informação não disponível"

    # Segment
    briefing["Segmento de atuação"] = profile.business_segment or "Informação não disponível"

    # Resumo executivo
    briefing["Resumo executivo da conta"] = (
        f"Esta empresa opera no segmento {profile.business_segment or 'desconhecido'}. "
        "A adoção de soluções de assinatura digital pode reduzir custos, acelerar processos "
        "e fortalecer o compliance, conforme evidenciado por pesquisas recentes sobre o mercado "
        "brasileiro【456051814697044†L20-L44】. Ao automatizar fluxos de assinatura, a empresa "
        "diminui burocracia, melhora a rastreabilidade de contratos e aumenta a segurança "
        "jurídica."
    )

    # Tipos de documentos comuns
    briefing["Tipos de documentos mais comuns nesse segmento"] = (
        "Contratos de prestação de serviços, termos de confidencialidade (NDAs), ordens de compra, "
        "propostas comerciais e acordos de parceria. Em setores como RH, os documentos incluem contratos "
        "de trabalho, rescisões, políticas internas e autorizações de férias, enquanto áreas como jurídica "
        "trabalham com procurações, termos de compliance e documentos societários【169039392159633†L190-L281】."
    )

    # Dores prováveis
    briefing["Dores prováveis"] = (
        "Processos manuais de assinatura geram atrasos, custos com papel e deslocamentos, aumentam o risco de "
        "extravio e dificultam o controle de versões【854328562475046†L84-L96】. A falta de digitalização "
        "também expõe a empresa a fraudes e falhas de compliance, pois documentos físicos podem ser "
        "alterados e são difíceis de auditar【854328562475046†L87-L115】."
    )

    # Hipóteses e impacto
    briefing["Hipóteses e impacto"] = (
        "Se a empresa busca aumentar eficiência e segurança, a assinatura digital pode reduzir o tempo de "
        "formalização em até 97% e diminuir custos operacionais acima de 80% (conforme relatos de mercado) ao "
        "eliminar etapas de impressão, envio e armazenamento físico. A organização também melhora o compliance "
        "ao garantir autenticidade, integridade e não repúdio dos documentos【456051814697044†L20-L44】."
    )

    # Sinais de urgência
    briefing["Sinais de urgência"] = (
        "Recentes mudanças regulatórias (por exemplo, LGPD e normas de compliance) exigem rastreabilidade e "
        "segurança nos fluxos documentais【456051814697044†L20-L44】. Acelerado crescimento de tentativas de "
        "fraude digital no Brasil também pressiona empresas a adotarem soluções mais avançadas de autenticação "
        "com inteligência artificial【975651670884422†L168-L188】. Setores competitivos demandam processos "
        "mais ágeis para não perder negócios para concorrentes que já adotam assinatura eletrônica."
    )

    # Perguntas de discovery
    briefing["Perguntas de discovery"] = (
        "1. Como são realizados hoje os processos de assinatura de contratos e documentos internos?\n"
        "2. Quantas pessoas precisam aprovar ou assinar um contrato típico e quanto tempo leva do início ao fim?\n"
        "3. Quais são os principais gargalos (custos, deslocamentos, extravio, aprovações) nesses fluxos?\n"
        "4. Existe preocupação crescente com compliance, rastreabilidade ou LGPD em sua empresa?\n"
        "5. Vocês já avaliaram soluções de assinatura eletrônica ou estão usando alguma plataforma atualmente?"
    )

    # Linha de abordagem e pitch
    briefing["Linha de abordagem e pitch"] = (
        "Destacar que a assinatura digital não é apenas uma substituição da assinatura manuscrita, mas uma peça "
        "estratégica para transformação digital e compliance. Apresentar dados de mercado e tendências (como o uso "
        "de IA para autenticação contínua【975651670884422†L168-L188】) para demonstrar que a solução escolhida deve "
        "ser moderna e escalável. Enfatizar que a ZapSign oferece segurança com certificação ICP‑Brasil, trilha de "
        "auditoria completa e integração com sistemas de gestão, além de reduzir custos e acelerar negócios."
    )

    # Abordagem comercial
    briefing["Abordagem comercial"] = (
        "A abordagem comercial deve começar com uma análise do cenário atual do cliente, quantificando os custos e "
        "tempos envolvidos nos fluxos de assinatura. Em seguida, oferecer uma demonstração prática da plataforma, "
        "mostrando como contratos de diferentes áreas (RH, Vendas, Jurídico) podem ser criados, enviados e "
        "gerenciados de forma centralizada com ZapSign. Destacar diferenciais como: automação de workflows, "
        "autenticação multifatorial, armazenamento seguro em nuvem e integração via API. Propor um projeto piloto "
        "com indicadores claros de sucesso (tempo de processamento, redução de custos, satisfação interna) para "
        "validar o retorno sobre o investimento."
    )

    return briefing


def display_briefing(briefing: Dict[str, str]) -> None:
    """Render the briefing in Streamlit (if available)."""
    if st is None:
        raise RuntimeError(
            "A biblioteca streamlit não está instalada. "
            "Instale-a com `pip install streamlit` para usar a interface web."
        )
    for section, content in briefing.items():
        st.subheader(section)
        st.write(content)


def main() -> None:
    """
    Entry point for the Streamlit application.  If Streamlit is not
    installed, this function will raise an informative error.
    """
    if st is None:
        raise RuntimeError(
            "A biblioteca streamlit não está instalada. "
            "Instale-a com `pip install streamlit` para executar a interface web."
        )

    st.set_page_config(page_title="ZapSign Lead Briefing", layout="wide")
    st.title("Gerador de Briefing Estratégico – ZapSign")

    st.markdown(
        "Preencha o nome e o site da empresa para gerar um briefing estratégico.\n\n"
        "**Observação:** este aplicativo usa dados genéricos como exemplo. Para produzir "
        "briefings mais precisos, conecte sistemas internos ou serviços de inteligência "
        "de mercado no lugar dos exemplos estáticos."
    )

    # Input fields
    company_name = st.text_input("Nome da empresa")
    company_site = st.text_input("Site da empresa")

    # Generate briefing when button is pressed
    if st.button("Gerar Briefing"):
        if not company_name:
            st.warning("Por favor, informe o nome da empresa.")
            return
        # Retrieve company information (stubbed)
        profile = get_company_info(company_name, company_site)
        # Generate briefing
        briefing = generate_briefing(profile)
        # Display
        display_briefing(briefing)


if __name__ == "__main__":
    main()