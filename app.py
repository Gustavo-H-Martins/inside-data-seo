"""
Inside Data — SEO Command Center
Streamlit app com geração de artigos via Claude API,
deploy FTP direto na Locaweb e envio via SMTP.
"""

import streamlit as st
from openai import OpenAI
import ftplib
import smtplib
import ssl
import re
import io
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Inside Data — SEO Command Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #0D1B2A; color: #E8F4F8; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Header ── */
.id-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 20px 0; border-bottom: 1px solid rgba(0,188,212,0.2); margin-bottom: 24px;
}
.id-logo {
    font-family: 'Space Mono', monospace; font-size: 13px;
    color: #00BCD4; letter-spacing: 1.2px; display: flex; align-items: center; gap: 10px;
}
.id-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #00BCD4; box-shadow: 0 0 10px #00BCD4; display: inline-block;
}
.id-traffic {
    background: rgba(0,188,212,0.10); border: 1px solid rgba(0,188,212,0.2);
    border-radius: 8px; padding: 6px 16px; font-family: 'Space Mono', monospace;
    color: #00BCD4; font-size: 14px; font-weight: 700;
}

/* ── Cards ── */
.id-card {
    background: #111F2E; border: 1px solid rgba(0,188,212,0.18);
    border-radius: 14px; padding: 22px; margin-bottom: 16px;
}
.id-card-alt {
    background: #162536; border: 1px solid rgba(0,188,212,0.12);
    border-radius: 12px; padding: 18px; margin-bottom: 12px;
    transition: border-color .2s;
}
.id-card-alt:hover { border-color: rgba(0,188,212,0.35); }

/* ── KPI ── */
.kpi-val {
    font-family: 'Space Mono', monospace; font-size: 36px;
    font-weight: 700; color: #00BCD4; line-height: 1;
}
.kpi-label { color: #7FA8BE; font-size: 12px; margin-top: 5px; }
.kpi-sub   { color: #7FA8BE; font-size: 11px; opacity: .6; }

/* ── Section title ── */
.sec-title {
    font-size: 11px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #7FA8BE; margin-bottom: 14px;
}

/* ── Traffic bar ── */
.tbar-wrap { display: flex; align-items: center; gap: 10px; margin-top: 6px; }
.tbar-track {
    flex: 1; height: 5px; background: rgba(255,255,255,.07);
    border-radius: 3px; overflow: hidden;
}
.tbar-fill  { height: 100%; border-radius: 3px; background: linear-gradient(90deg,#00BCD4,#4DD9EC); }
.tbar-val   { font-family: 'Space Mono', monospace; color: #00BCD4; font-weight: 700; font-size: 13px; min-width: 56px; text-align: right; }

/* ── Chips ── */
.chip      { border-radius: 4px; padding: 2px 9px; font-size: 11px; font-weight: 600; display: inline-block; margin-right: 4px; }
.chip-cat  { background: rgba(0,188,212,0.12); color: #00BCD4; }
.chip-int  { background: rgba(255,255,255,.05); color: #7FA8BE; }
.chip-diff { background: rgba(255,255,255,.05); color: #7FA8BE; }

/* ── Threat badges ── */
.threat-high   { background: rgba(239,68,68,.15);  color: #F87171; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }
.threat-medium { background: rgba(251,191,36,.15); color: #FCD34D; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }
.threat-low    { background: rgba(52,211,153,.15); color: #6EE7B7; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }

/* ── Insight box ── */
.insight {
    background: rgba(0,188,212,0.08); border: 1px solid rgba(0,188,212,0.2);
    border-radius: 10px; padding: 18px; margin-top: 16px;
}
.insight h4 { color: #00BCD4; font-size: 13px; font-weight: 700; margin-bottom: 8px; }

/* ── Theme item ── */
.theme-item {
    display: flex; gap: 10px; padding: 10px 14px;
    background: rgba(0,188,212,.06); border: 1px solid rgba(0,188,212,0.18);
    border-radius: 8px; margin-bottom: 8px;
}
.theme-num { font-family: 'Space Mono', monospace; font-size: 11px; color: #00BCD4; margin-top: 2px; }

/* ── Swatch ── */
.swatch-row { display: flex; gap: 14px; flex-wrap: wrap; }
.swatch { text-align: center; }
.swatch-box { width: 50px; height: 50px; border-radius: 10px; border: 2px solid rgba(255,255,255,.1); margin-bottom: 5px; }
.swatch-name { color: #7FA8BE; font-size: 11px; }
.swatch-hex  { font-family: 'Space Mono', monospace; color: #00BCD4; font-size: 10px; }

/* ── Streamlit overrides ── */
div[data-testid="stTabs"] button { color: #7FA8BE !important; font-family: 'DM Sans', sans-serif !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #00BCD4 !important; border-bottom-color: #00BCD4 !important; }
div[data-testid="stTabs"] { border-bottom: 1px solid rgba(0,188,212,0.2); }
.stButton > button {
    background: linear-gradient(135deg,#00BCD4,#0097A7) !important;
    color: #0D1B2A !important; border: none !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: .5px !important; border-radius: 8px !important;
}
.stButton > button:hover { opacity: .85 !important; }
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    background: #162536 !important; border: 1px solid rgba(0,188,212,0.2) !important;
    color: #E8F4F8 !important; border-radius: 8px !important;
}
div[data-testid="stMetric"] {
    background: #111F2E; border: 1px solid rgba(0,188,212,0.18);
    border-radius: 14px; padding: 16px;
}
div[data-testid="stMetric"] label { color: #7FA8BE !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #00BCD4 !important; font-family: 'Space Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
IDEAS = [
    {"id": 1, "title": "Como Estruturar Uma Arquitetura de Dados Escalável",    "keyword": "arquitetura de dados escalável",   "traffic": 1300, "difficulty": "Média",      "intent": "Educacional", "category": "Arquitetura", "slug": "arquitetura-dados-escalavel"},
    {"id": 2, "title": "Melhores Práticas de Governança de Dados LGPD",         "keyword": "governança de dados LGPD",          "traffic": 1100, "difficulty": "Média-Alta",  "intent": "Informacional","category": "Governança",  "slug": "governanca-dados-lgpd"},
    {"id": 3, "title": "Consultoria de Arquitetura de Dados Para Empresas",     "keyword": "consultoria arquitetura de dados",  "traffic": 900,  "difficulty": "Alta",        "intent": "Comercial",   "category": "Serviços",    "slug": "consultoria-arquitetura-dados"},
    {"id": 4, "title": "Consultoria de Governança de Dados em Nuvem",           "keyword": "governança de dados nuvem",         "traffic": 720,  "difficulty": "Média",       "intent": "Comercial",   "category": "Governança",  "slug": "consultoria-governanca-dados-nuvem"},
    {"id": 5, "title": "Consultoria Agnóstica AWS, Azure e GCP",                "keyword": "consultoria cloud agnóstica",       "traffic": 240,  "difficulty": "Baixa",       "intent": "Comercial",   "category": "Cloud",       "slug": "consultoria-agnostica-aws-azure-gcp"},
]

COMPETITORS = [
    {"name": "KPMG",                       "domain": "kpmg.com.br",          "da": 92, "threat": "high"},
    {"name": "Deloitte",                   "domain": "deloitte.com.br",       "da": 95, "threat": "high"},
    {"name": "Accenture",                  "domain": "accenture.com/br-pt",   "da": 94, "threat": "high"},
    {"name": "Thoughtworks",               "domain": "thoughtworks.com/pt-br","da": 78, "threat": "medium"},
    {"name": "Consultorias especializadas","domain": "mercado fragmentado",   "da": 45, "threat": "low"},
]

THEMES = [
    "Arquitetura de dados escalável e agnóstica",
    "Engenharia de dados, pipelines e integrações",
    "Governança, qualidade e catálogo de dados",
    "Segurança, compliance e LGPD em ambientes cloud",
    "Modernização multicloud e otimização de custos",
    "Automação de processos, DataOps e sustentação operacional",
]

MAX_TRAFFIC = 1300

# ─── Session state ────────────────────────────────────────────────────────────
if "generated" not in st.session_state:
    st.session_state.generated = {}   # id -> html string

# ─── Helpers ──────────────────────────────────────────────────────────────────
def tbar(value: int, max_val: int = MAX_TRAFFIC) -> str:
    pct = round(value / max_val * 100)
    return f"""
    <div class="tbar-wrap">
      <div class="tbar-track"><div class="tbar-fill" style="width:{pct}%"></div></div>
      <div class="tbar-val">+{value:,}/mês</div>
    </div>""".replace(",", ".")

def threat_badge(level: str) -> str:
    labels = {"high": "Alto", "medium": "Médio", "low": "Baixo"}
    return f'<span class="threat-{level}">{labels[level]}</span>'

# ─── Claude API ───────────────────────────────────────────────────────────────
def generate_article(idea: dict) -> str:
    client = OpenAI(
        api_key=st.secrets["deepseek"]["api_key"],
        base_url="https://api.deepseek.com/v1",
    )
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": """Você é especialista em SEO e content marketing B2B de tecnologia de dados no Brasil.
A empresa é a Inside Data — consultoria de Arquitetura, Engenharia e Governança de Dados, agnóstica em cloud (AWS/Azure/GCP).
Tom: consultivo, técnico, executivo. Target: Diretores e Heads de Dados.
RETORNE APENAS HTML COMPLETO E PUBLICÁVEL — sem markdown, sem explicações, sem backticks.
HTML standalone com CSS inline, identidade visual navy #0D1B2A + cyan #00BCD4, fonte system-ui, responsivo.""",
            },
            {
                "role": "user",
                "content": f"""Gere um artigo de blog HTML completo sobre: "{idea['title']}"
Keyword: "{idea['keyword']}" | Intenção: {idea['intent']} | Categoria: {idea['category']}

Estrutura obrigatória:
- <head> com title, meta description, charset UTF-8 e CSS inline completo
- H1 com a keyword
- Introdução impactante (2 parágrafos)
- 3 seções H2 com conteúdo técnico-executivo e exemplos práticos
- Blockquote ou box destacado com insight-chave
- CTA final: diagnóstico gratuito com a Inside Data
- Footer: "Inside Data Consultoria | grupolmtech.com.br/insidedata"
- Design responsivo, identidade visual navy/cyan

Retorne SOMENTE o HTML, começando com <!DOCTYPE html>.""",
            },
        ],
    )
    return response.choices[0].message.content

# ─── FTP Deploy ───────────────────────────────────────────────────────────────
def deploy_ftp(html: str, slug: str) -> tuple[bool, str]:
    cfg = st.secrets["ftp"]
    filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.html"
    remote_path = f"{cfg['base_dir']}/{filename}"
    public_url  = f"{cfg['base_url']}/{filename}"
    try:
        buf = io.BytesIO(html.encode("utf-8"))
        with ftplib.FTP() as ftp:
            ftp.connect(cfg["host"], int(cfg["port"]), timeout=20)
            ftp.login(cfg["user"], cfg["password"])
            # garante que o diretório existe
            try:
                ftp.mkd(cfg["base_dir"])
            except ftplib.error_perm:
                pass  # já existe
            ftp.storbinary(f"STOR {remote_path}", buf)
        return True, public_url
    except Exception as e:
        return False, str(e)

# ─── SMTP Send ────────────────────────────────────────────────────────────────
def send_email(html: str, subject: str) -> tuple[bool, str]:
    cfg = st.secrets["smtp"]
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = cfg["user"]
        msg["To"]      = cfg["to"]
        msg.attach(MIMEText(html, "html", "utf-8"))

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(cfg["host"], int(cfg["port"]), context=ctx) as server:
            server.login(cfg["user"], cfg["password"])
            server.sendmail(cfg["user"], cfg["to"], msg.as_string())
        return True, cfg["to"]
    except Exception as e:
        return False, str(e)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="id-header">
  <div class="id-logo"><span class="id-dot"></span> INSIDE DATA — SEO COMMAND CENTER</div>
  <div class="id-traffic">+14.260 visitantes/mês</div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🏢 Concorrentes", "✍️ Conteúdo SEO", "🎨 Brand Brief"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Tráfego Potencial", "+14.260", "visitantes/mês")
    c2.metric("Pautas Identificadas", "5", "artigos estratégicos")
    c3.metric("Concorrentes", "5", "mapeados")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="id-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Top Content Opportunities</div>', unsafe_allow_html=True)
    for idea in IDEAS:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;gap:16px;flex-wrap:wrap">
          <div style="flex:1">
            <div style="font-size:14px;margin-bottom:4px">{idea['title']}</div>
            {tbar(idea['traffic'])}
          </div>
          <span class="chip chip-cat">{idea['category']}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CONCORRENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    for i, c in enumerate(COMPETITORS):
        col_num, col_info, col_da, col_threat = st.columns([0.5, 4, 1.5, 1.5])
        with col_num:
            st.markdown(f"<span style='font-family:Space Mono,monospace;color:#7FA8BE;font-size:12px'>#{str(i+1).zfill(2)}</span>", unsafe_allow_html=True)
        with col_info:
            st.markdown(f"<div style='font-weight:600;font-size:15px'>{c['name']}</div><div style='color:#7FA8BE;font-size:12px'>{c['domain']}</div>", unsafe_allow_html=True)
        with col_da:
            st.markdown(f"<div style='font-family:Space Mono,monospace;color:#00BCD4;font-weight:700;font-size:18px;text-align:center'>{c['da']}</div><div style='color:#7FA8BE;font-size:10px;text-align:center'>Domain Auth.</div>", unsafe_allow_html=True)
        with col_threat:
            st.markdown(threat_badge(c["threat"]), unsafe_allow_html=True)
        st.markdown("<hr style='border-color:rgba(0,188,212,0.1);margin:8px 0'>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight">
      <h4>💡 Insight Estratégico</h4>
      <p style="font-size:14px;line-height:1.7">KPMG, Deloitte e Accenture dominam termos genéricos mas raramente produzem conteúdo técnico profundo em PT-BR sobre implementações reais.
      A Inside Data tem vantagem em <strong style="color:#00BCD4">especificidade técnica + linguagem executiva BR</strong> — um gap que o conteúdo SEO deve explorar ativamente.</p>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CONTEÚDO SEO
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<p style='color:#7FA8BE;font-size:14px;margin-bottom:24px'>Gere, visualize e publique artigos diretamente na Locaweb.</p>", unsafe_allow_html=True)

    for idea in IDEAS:
        with st.container():
            st.markdown(f"""
            <div class="id-card-alt">
              <div class="idea-meta">
                <span class="chip chip-cat">{idea['category']}</span>
                <span class="chip chip-int">{idea['intent']}</span>
                <span class="chip chip-diff">Dif: {idea['difficulty']}</span>
              </div>
              <div style="font-size:16px;font-weight:600;margin:8px 0">{idea['title']}</div>
              {tbar(idea['traffic'])}
            </div>""", unsafe_allow_html=True)

            already = idea["id"] in st.session_state.generated
            btn_label = "↺ REGENERAR ARTIGO" if already else "✦ GERAR ARTIGO"

            col_gen, col_ftp, col_mail, col_both = st.columns([2, 2, 2, 2])

            with col_gen:
                if st.button(btn_label, key=f"gen_{idea['id']}"):
                    with st.spinner(f"Gerando '{idea['title']}'..."):
                        try:
                            html = generate_article(idea)
                            st.session_state.generated[idea["id"]] = html
                            st.success("✓ Artigo gerado!")
                        except Exception as e:
                            st.error(f"Erro na API: {e}")

            if already:
                with col_ftp:
                    if st.button("💾 DEPLOY FTP", key=f"ftp_{idea['id']}"):
                        with st.spinner("Enviando para Locaweb..."):
                            ok, result = deploy_ftp(st.session_state.generated[idea["id"]], idea["slug"])
                            if ok:
                                st.success(f"✓ Publicado! [Ver artigo]({result})")
                            else:
                                st.error(f"FTP erro: {result}")

                with col_mail:
                    if st.button("📧 ENVIAR E-MAIL", key=f"mail_{idea['id']}"):
                        with st.spinner("Enviando por SMTP..."):
                            ok, result = send_email(
                                st.session_state.generated[idea["id"]],
                                f"[Inside Data SEO] {idea['title']}"
                            )
                            if ok:
                                st.success(f"✓ Enviado para {result}")
                            else:
                                st.error(f"SMTP erro: {result}")

                with col_both:
                    if st.button("🚀 DEPLOY + E-MAIL", key=f"both_{idea['id']}"):
                        with st.spinner("Salvando e enviando..."):
                            html = st.session_state.generated[idea["id"]]
                            ok_ftp,  r_ftp  = deploy_ftp(html, idea["slug"])
                            ok_mail, r_mail = send_email(html, f"[Inside Data SEO] {idea['title']}")
                            if ok_ftp and ok_mail:
                                st.success(f"✓ Publicado + e-mail enviado! [Ver artigo]({r_ftp})")
                            else:
                                if not ok_ftp:  st.error(f"FTP: {r_ftp}")
                                if not ok_mail: st.error(f"SMTP: {r_mail}")

                # Prévia
                with st.expander("👁 Ver prévia do HTML gerado", expanded=False):
                    html_preview = st.session_state.generated[idea["id"]]
                    st.components.v1.html(html_preview, height=500, scrolling=True)
                    st.download_button(
                        "⬇ Baixar HTML",
                        data=html_preview,
                        file_name=f"{idea['slug']}.html",
                        mime="text/html",
                        key=f"dl_{idea['id']}"
                    )

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — BRAND BRIEF
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""<div class="id-card">
          <div class="sec-title">Sobre a Empresa</div>
          <p style="font-size:14px;line-height:1.75">Consultoria executiva especializada em
          <strong style="color:#00BCD4">Arquitetura, Engenharia e Governança de Dados</strong> para empresas que precisam
          transformar ambientes complexos em plataformas confiáveis e escaláveis. Atua do diagnóstico até a implementação
          e transferência de conhecimento. Diferencial: posicionamento
          <strong style="color:#00BCD4">agnóstico em cloud</strong> — AWS, Azure e GCP — com foco em clareza operacional,
          segurança, compliance e valor mensurável.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="id-card">
          <div class="sec-title">Tom & Voz</div>
          <p style="font-size:14px;line-height:1.7">Comunicação <strong>consultiva, técnica e executiva</strong>.
          Autoridade, objetividade e precisão — maturidade estratégica e profundidade de engenharia.
          Foco em decisão de negócio sustentada por dados e métricas.</p>
        </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""<div class="id-card">
          <div class="sec-title">Público-Alvo</div>
          <p style="font-size:14px;line-height:1.7">Empresas em crescimento acelerado com múltiplos sistemas e alto
          volume de dados. <strong>Diretores, Heads de Dados, tecnologia, engenharia e transformação digital</strong>
          que precisam reduzir risco, padronizar processos e defender investimentos internamente.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="id-card"><div class="sec-title">Identidade Visual</div>', unsafe_allow_html=True)
        st.markdown("""<div class="swatch-row">
          <div class="swatch"><div class="swatch-box" style="background:#0D1B2A"></div><div class="swatch-name">Navy</div><div class="swatch-hex">#0D1B2A</div></div>
          <div class="swatch"><div class="swatch-box" style="background:#00BCD4"></div><div class="swatch-name">Cyan</div><div class="swatch-hex">#00BCD4</div></div>
          <div class="swatch"><div class="swatch-box" style="background:#111F2E"></div><div class="swatch-name">Surface</div><div class="swatch-hex">#111F2E</div></div>
          <div class="swatch"><div class="swatch-box" style="background:#4DD9EC"></div><div class="swatch-name">Cyan Lt</div><div class="swatch-hex">#4DD9EC</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="id-card"><div class="sec-title">Temas Estratégicos</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, theme in enumerate(THEMES):
        with cols[i % 2]:
            st.markdown(f"""<div class="theme-item">
              <span class="theme-num">{str(i+1).zfill(2)}</span>
              <span style="font-size:13px;line-height:1.5">{theme}</span>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
