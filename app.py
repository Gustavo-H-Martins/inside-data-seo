"""
Inside Data — SEO Command Center
Geração de artigos HTML publicáveis via DeepSeek API,
deploy FTP direto na Locaweb e envio via SMTP SSL.
"""

import streamlit as st
import streamlit.components.v1 as components
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

# ─── CSS Global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #0D1B2A; color: #E8F4F8; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.id-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 20px 0; border-bottom: 1px solid rgba(0,188,212,0.2); margin-bottom: 24px;
}
.id-logo { font-family: 'Space Mono', monospace; font-size: 13px; color: #00BCD4; letter-spacing: 1.2px; display: flex; align-items: center; gap: 10px; }
.id-dot  { width: 8px; height: 8px; border-radius: 50%; background: #00BCD4; box-shadow: 0 0 10px #00BCD4; display: inline-block; }
.id-traffic { background: rgba(0,188,212,0.10); border: 1px solid rgba(0,188,212,0.2); border-radius: 8px; padding: 6px 16px; font-family: 'Space Mono', monospace; color: #00BCD4; font-size: 14px; font-weight: 700; }

.id-card     { background: #111F2E; border: 1px solid rgba(0,188,212,0.18); border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.id-card-alt { background: #162536; border: 1px solid rgba(0,188,212,0.12); border-radius: 12px; padding: 18px; margin-bottom: 12px; }
.id-card-alt:hover { border-color: rgba(0,188,212,0.35); }

.sec-title { font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #7FA8BE; margin-bottom: 14px; }

.tbar-wrap  { display: flex; align-items: center; gap: 10px; margin-top: 6px; }
.tbar-track { flex: 1; height: 5px; background: rgba(255,255,255,.07); border-radius: 3px; overflow: hidden; }
.tbar-fill  { height: 100%; border-radius: 3px; background: linear-gradient(90deg,#00BCD4,#4DD9EC); }
.tbar-val   { font-family: 'Space Mono', monospace; color: #00BCD4; font-weight: 700; font-size: 13px; min-width: 56px; text-align: right; }

.chip      { border-radius: 4px; padding: 2px 9px; font-size: 11px; font-weight: 600; display: inline-block; margin-right: 4px; }
.chip-cat  { background: rgba(0,188,212,0.12); color: #00BCD4; }
.chip-int  { background: rgba(255,255,255,.05); color: #7FA8BE; }
.chip-diff { background: rgba(255,255,255,.05); color: #7FA8BE; }

.threat-high   { background: rgba(239,68,68,.15);  color: #F87171; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }
.threat-medium { background: rgba(251,191,36,.15); color: #FCD34D; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }
.threat-low    { background: rgba(52,211,153,.15); color: #6EE7B7; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }

.insight { background: rgba(0,188,212,0.08); border: 1px solid rgba(0,188,212,0.2); border-radius: 10px; padding: 18px; margin-top: 16px; }
.insight h4 { color: #00BCD4; font-size: 13px; font-weight: 700; margin-bottom: 8px; }

.theme-item { display: flex; gap: 10px; padding: 10px 14px; background: rgba(0,188,212,.06); border: 1px solid rgba(0,188,212,0.18); border-radius: 8px; margin-bottom: 8px; }
.theme-num  { font-family: 'Space Mono', monospace; font-size: 11px; color: #00BCD4; margin-top: 2px; }

.swatch-row { display: flex; gap: 14px; flex-wrap: wrap; }
.swatch     { text-align: center; }
.swatch-box { width: 50px; height: 50px; border-radius: 10px; border: 2px solid rgba(255,255,255,.1); margin-bottom: 5px; }
.swatch-name { color: #7FA8BE; font-size: 11px; }
.swatch-hex  { font-family: 'Space Mono', monospace; color: #00BCD4; font-size: 10px; }

div[data-testid="stTabs"] button { color: #7FA8BE !important; font-family: 'DM Sans', sans-serif !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #00BCD4 !important; border-bottom-color: #00BCD4 !important; }
div[data-testid="stTabs"] { border-bottom: 1px solid rgba(0,188,212,0.2); }
.stButton > button {
    background: linear-gradient(135deg,#00BCD4,#0097A7) !important;
    color: #0D1B2A !important; border: none !important;
    font-family: 'Space Mono', monospace !important; font-size: 11px !important;
    font-weight: 700 !important; letter-spacing: .5px !important; border-radius: 8px !important;
}
.stButton > button:hover { opacity: .85 !important; }
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    background: #162536 !important; border: 1px solid rgba(0,188,212,0.2) !important;
    color: #E8F4F8 !important; border-radius: 8px !important;
}
div[data-testid="stMetric"] { background: #111F2E; border: 1px solid rgba(0,188,212,0.18); border-radius: 14px; padding: 16px; }
div[data-testid="stMetric"] label { color: #7FA8BE !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #00BCD4 !important; font-family: 'Space Mono', monospace !important; }
div[data-testid="stChatMessage"] { background: #111F2E !important; border: 1px solid rgba(0,188,212,0.15) !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ─── HTML template fiel ao site ───────────────────────────────────────────────
# Capturado de grupolmtech.com.br/insidedata
ARTICLE_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{seo_title} | Inside Data</title>
  <meta name="description" content="{meta_description}"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#f4f7fc;color:#1a202c;line-height:1.7;-webkit-font-smoothing:antialiased}}

    /* NAV */
    nav{{background:#0D1B2A;padding:0 5%;display:flex;align-items:center;justify-content:space-between;height:64px;position:sticky;top:0;z-index:100;border-bottom:1px solid rgba(0,188,212,0.15)}}
    .nav-logo img{{height:36px}}
    .nav-links{{display:flex;gap:28px;list-style:none}}
    .nav-links a{{color:#7FA8BE;text-decoration:none;font-size:14px;font-weight:500;transition:.2s}}
    .nav-links a:hover{{color:#00BCD4}}
    .nav-cta{{background:#00BCD4;color:#0D1B2A!important;padding:8px 20px;border-radius:50px;font-weight:700!important;font-size:13px!important}}
    @media(max-width:700px){{.nav-links{{display:none}}}}

    /* HERO */
    .hero{{background:linear-gradient(135deg,#0D1B2A 0%,#162536 60%,#0D1B2A 100%);padding:64px 5% 48px;border-bottom:1px solid rgba(0,188,212,0.15)}}
    .hero-inner{{max-width:860px;margin:0 auto}}
    .hero-badge{{display:inline-block;background:rgba(0,188,212,0.12);color:#00BCD4;border:1px solid rgba(0,188,212,0.3);border-radius:50px;padding:4px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:20px}}
    .hero h1{{font-size:2.4rem;font-weight:700;color:#E8F4F8;line-height:1.25;letter-spacing:-0.02em;margin-bottom:16px}}
    .hero h1 span{{color:#00BCD4}}
    .hero-meta{{display:flex;gap:20px;flex-wrap:wrap;font-size:13px;color:#7FA8BE}}
    .hero-meta span{{display:flex;align-items:center;gap:6px}}
    @media(max-width:600px){{.hero h1{{font-size:1.7rem}}}}

    /* ARTICLE BODY */
    .article-wrap{{max-width:860px;margin:0 auto;padding:48px 24px 64px}}
    .article-body{{background:#fff;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,0.06);padding:2.8rem}}
    @media(max-width:600px){{.article-body{{padding:1.6rem 1.2rem}}}}

    h2{{font-size:1.75rem;font-weight:700;color:#0D1B2A;margin:2.4rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #e2e8f0;position:relative}}
    h2::after{{content:"";display:block;width:56px;height:4px;background:#00BCD4;margin-top:.5rem;border-radius:4px}}
    h3{{font-size:1.2rem;font-weight:700;color:#0D1B2A;margin:1.8rem 0 .8rem}}
    p{{font-size:1.05rem;margin-bottom:1.3rem;color:#2d3748}}
    strong{{color:#0D1B2A;font-weight:600}}
    ul,ol{{margin:0 0 1.3rem 1.6rem}}
    li{{font-size:1.05rem;color:#2d3748;margin-bottom:.4rem}}

    .intro-highlight{{background:linear-gradient(105deg,#e6f7fb,#fff);padding:1.4rem 1.8rem;border-radius:14px;border-left:5px solid #00BCD4;margin:1.8rem 0 2rem;font-weight:500;color:#0D1B2A;font-size:1.05rem}}

    .insight-box{{background:#0D1B2A;color:#fff;border-radius:20px;padding:2rem;margin:2.8rem 0;position:relative;box-shadow:0 18px 30px -10px rgba(0,188,212,0.2)}}
    .insight-box::before{{content:"\201C";font-size:5rem;color:#00BCD4;position:absolute;top:-15px;left:20px;opacity:.8;line-height:1;font-family:Georgia,serif}}
    .insight-box p{{color:#e2e8f0;font-size:1.2rem;font-style:italic;margin:0;padding-left:1rem;border-left:3px solid #00BCD4}}
    .insight-label{{text-transform:uppercase;letter-spacing:.08em;font-size:.8rem;font-weight:700;color:#00BCD4;margin-bottom:.5rem;display:block}}

    /* CTA */
    .cta-section{{border:2px solid #00BCD4;border-radius:24px;padding:2.4rem;margin:2.8rem 0 1.5rem;background:linear-gradient(to right,#fff,#f0fcff);text-align:center;box-shadow:0 10px 25px -8px rgba(0,188,212,.25)}}
    .cta-section h3{{font-size:1.8rem;font-weight:700;color:#0D1B2A;margin-bottom:.6rem}}
    .cta-section p{{font-size:1.05rem;color:#2d3748;margin-bottom:1.6rem}}
    .cta-button{{display:inline-block;background:#00BCD4;color:#0D1B2A;font-weight:700;font-size:1.05rem;padding:13px 32px;border-radius:50px;text-decoration:none;letter-spacing:.02em;transition:.25s;border:2px solid #00BCD4}}
    .cta-button:hover{{background:#0097A7;border-color:#0097A7}}
    .cta-button-sec{{display:inline-block;margin-left:12px;color:#0D1B2A;font-weight:600;font-size:1rem;padding:13px 28px;border-radius:50px;text-decoration:none;border:2px solid #0D1B2A;transition:.25s}}
    .cta-button-sec:hover{{background:#0D1B2A;color:#fff}}

    /* FOOTER */
    footer{{background:#0D1B2A;border-top:1px solid rgba(0,188,212,0.15);padding:48px 5% 32px}}
    .footer-inner{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px}}
    .footer-brand img{{height:40px;margin-bottom:14px}}
    .footer-brand p{{color:#7FA8BE;font-size:13px;line-height:1.6}}
    .footer-col h4{{color:#E8F4F8;font-size:13px;font-weight:700;margin-bottom:14px;text-transform:uppercase;letter-spacing:.8px}}
    .footer-col ul{{list-style:none}}
    .footer-col ul li{{margin-bottom:8px}}
    .footer-col ul li a{{color:#7FA8BE;text-decoration:none;font-size:13px;transition:.2s}}
    .footer-col ul li a:hover{{color:#00BCD4}}
    .footer-bottom{{max-width:1100px;margin:32px auto 0;padding-top:24px;border-top:1px solid rgba(255,255,255,.06);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
    .footer-bottom p{{color:#7FA8BE;font-size:12px}}
    .social-links{{display:flex;gap:12px}}
    .social-links a{{color:#7FA8BE;font-size:13px;text-decoration:none;transition:.2s}}
    .social-links a:hover{{color:#00BCD4}}
    @media(max-width:700px){{.footer-inner{{grid-template-columns:1fr 1fr}}.footer-brand{{grid-column:1/-1}}}}
  </style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-logo">
    <img src="https://grupolmtech.com.br/images/logo_secondary.png" alt="Inside Data Consultoria"/>
  </div>
  <ul class="nav-links">
    <li><a href="https://grupolmtech.com.br/insidedata#about">Sobre</a></li>
    <li><a href="https://grupolmtech.com.br/insidedata#services">Serviços</a></li>
    <li><a href="https://grupolmtech.com.br/insidedata#portfolio">Portfólio</a></li>
    <li><a href="https://grupolmtech.com.br/insidedata#contact" class="nav-cta">Agendar diagnóstico</a></li>
  </ul>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-inner">
    <div class="hero-badge">{category}</div>
    <h1>{h1_title}</h1>
    <div class="hero-meta">
      <span>📅 {publish_date}</span>
      <span>⏱ {read_time} min de leitura</span>
      <span>✍️ Inside Data</span>
    </div>
  </div>
</div>

<!-- ARTICLE -->
<div class="article-wrap">
  <div class="article-body">
    {article_body}
  </div>
</div>

<!-- FOOTER -->
<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <img src="https://grupolmtech.com.br/images/logo_primary.png" alt="Inside Data"/>
      <p>Transformando dados em inteligência de negócios e automatizando processos.</p>
    </div>
    <div class="footer-col">
      <h4>Serviços</h4>
      <ul>
        <li><a href="https://grupolmtech.com.br/insidedata#services">Arquitetura de Dados</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#services">Engenharia de Dados</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#services">Governança & LGPD</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#services">DataOps & Cloud</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Empresa</h4>
      <ul>
        <li><a href="https://grupolmtech.com.br/insidedata#about">Sobre Nós</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#portfolio">Portfólio</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata/blog">Blog</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#contact">Contato</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contato</h4>
      <ul>
        <li><a href="mailto:contato@grupolmtech.com.br">contato@grupolmtech.com.br</a></li>
        <li><a href="https://wa.me/5531986402114">(31) 98640-2114</a></li>
        <li><a href="#">Lagoa Santa — MG</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© {year} Inside Data Consultoria. Todos os direitos reservados. | CNPJ: 55.299.485/0001-58</p>
    <div class="social-links">
      <a href="https://www.linkedin.com/company/insidedatabr/" target="_blank">LinkedIn</a>
      <a href="https://github.com/insidedatabr" target="_blank">GitHub</a>
      <a href="https://www.instagram.com/insidedata.br/" target="_blank">Instagram</a>
    </div>
  </div>
</footer>

</body>
</html>"""

# ─── Dados ────────────────────────────────────────────────────────────────────
IDEAS = [
    {"id":1,"title":"Como Estruturar Uma Arquitetura de Dados Escalável","keyword":"arquitetura de dados escalável","traffic":1300,"difficulty":"Média","intent":"Educacional","category":"Arquitetura","slug":"arquitetura-dados-escalavel"},
    {"id":2,"title":"Melhores Práticas de Governança de Dados LGPD","keyword":"governança de dados LGPD","traffic":1100,"difficulty":"Média-Alta","intent":"Informacional","category":"Governança","slug":"governanca-dados-lgpd"},
    {"id":3,"title":"Consultoria de Arquitetura de Dados Para Empresas","keyword":"consultoria arquitetura de dados","traffic":900,"difficulty":"Alta","intent":"Comercial","category":"Serviços","slug":"consultoria-arquitetura-dados"},
    {"id":4,"title":"Consultoria de Governança de Dados em Nuvem","keyword":"governança de dados nuvem","traffic":720,"difficulty":"Média","intent":"Comercial","category":"Governança","slug":"consultoria-governanca-dados-nuvem"},
    {"id":5,"title":"Consultoria Agnóstica AWS, Azure e GCP","keyword":"consultoria cloud agnóstica","traffic":240,"difficulty":"Baixa","intent":"Comercial","category":"Cloud","slug":"consultoria-agnostica-aws-azure-gcp"},
]

COMPETITORS = [
    {"name":"KPMG","domain":"kpmg.com.br","da":92,"threat":"high"},
    {"name":"Deloitte","domain":"deloitte.com.br","da":95,"threat":"high"},
    {"name":"Accenture","domain":"accenture.com/br-pt","da":94,"threat":"high"},
    {"name":"Thoughtworks","domain":"thoughtworks.com/pt-br","da":78,"threat":"medium"},
    {"name":"Consultorias especializadas","domain":"mercado fragmentado","da":45,"threat":"low"},
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
for key in ["generated", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = {} if key == "generated" else []

# ─── Helpers ──────────────────────────────────────────────────────────────────
def tbar(value: int, max_val: int = MAX_TRAFFIC) -> str:
    pct = round(value / max_val * 100)
    return f'<div class="tbar-wrap"><div class="tbar-track"><div class="tbar-fill" style="width:{pct}%"></div></div><div class="tbar-val">+{value:,}/mês</div></div>'.replace(",",".")

def threat_badge(level: str) -> str:
    labels = {"high":"Alto","medium":"Médio","low":"Baixo"}
    return f'<span class="threat-{level}">{labels[level]}</span>'

def clean_html(raw: str) -> str:
    """Remove markdown fences que alguns modelos retornam."""
    raw = raw.strip()
    raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return raw.strip()

def build_full_html(article_body: str, meta: dict) -> str:
    """Injeta o corpo do artigo no template fiel ao site."""
    return ARTICLE_HTML_TEMPLATE.format(
        seo_title=meta.get("seo_title", meta["title"]),
        meta_description=meta.get("meta_description", ""),
        h1_title=meta["title"],
        category=meta.get("category", "Blog"),
        publish_date=datetime.now().strftime("%d/%m/%Y"),
        read_time=meta.get("read_time", "7"),
        article_body=article_body,
        year=datetime.now().year,
    )

# ─── DeepSeek API ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Você é especialista em SEO e content marketing B2B de tecnologia de dados no Brasil.
A empresa é a Inside Data — consultoria de Arquitetura, Engenharia e Governança de Dados, agnóstica em cloud (AWS/Azure/GCP).
Tom: consultivo, técnico, executivo. Target: Diretores e Heads de Dados.
Identidade visual: background navy #0D1B2A, destaque cyan #00BCD4, texto #2d3748.
Contato: contato@grupolmtech.com.br | (31) 98640-2114 | grupolmtech.com.br/insidedata

IMPORTANTE: Retorne APENAS o corpo interno do artigo em HTML puro — sem DOCTYPE, sem <html>, sem <head>, sem <body>, sem <nav>, sem <footer>.
Retorne somente o conteúdo que vai dentro do <div class="article-body">.
Use as classes CSS disponíveis: intro-highlight, insight-box, insight-label, cta-section, cta-button, cta-button-sec.
NÃO use markdown. NÃO use fences de código. Retorne HTML direto."""

def call_deepseek(user_prompt: str) -> str:
    client = OpenAI(
        api_key=st.secrets["deepseek"]["api_key"],
        base_url="https://api.deepseek.com/v1",
    )
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        max_tokens=2500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
    )
    return clean_html(response.choices[0].message.content)

def generate_from_idea(idea: dict) -> str:
    prompt = f"""Gere o corpo de um artigo de blog completo e otimizado para SEO sobre: "{idea['title']}"
Keyword principal: "{idea['keyword']}" | Intenção: {idea['intent']} | Categoria: {idea['category']}

Estrutura obrigatória do corpo:
1. <div class="intro-highlight"> com parágrafo de introdução impactante
2. Parágrafo de contexto executivo
3. Três seções <h2> com conteúdo técnico real, exemplos práticos e listas <ul>
4. <div class="insight-box"> com <span class="insight-label">Insight Inside Data</span> e um insight estratégico
5. <div class="cta-section"> com h3 "Pronto para estruturar seus dados?", parágrafo e dois links:
   - <a class="cta-button" href="https://grupolmtech.com.br/insidedata#contact">Agendar diagnóstico gratuito</a>
   - <a class="cta-button-sec" href="https://grupolmtech.com.br/downloads/business-case-onepager.pdf">Baixar one-pager</a>"""
    body = call_deepseek(prompt)
    return build_full_html(body, {
        "title": idea["title"],
        "seo_title": idea["title"],
        "meta_description": f"Saiba como a Inside Data pode ajudar sua empresa com {idea['keyword']}. Consultoria agnóstica em cloud, LGPD e governança de dados.",
        "category": idea["category"],
        "read_time": "7",
    })

def generate_from_chat(topic: str) -> tuple[str, str]:
    """Gera artigo a partir de tema livre. Retorna (html_completo, slug)."""
    prompt = f"""Gere o corpo de um artigo de blog completo e otimizado para SEO sobre o tema: "{topic}"
Adapte keyword, intenção e categoria automaticamente para o público da Inside Data.

Estrutura obrigatória do corpo:
1. <div class="intro-highlight"> com parágrafo de introdução impactante
2. Parágrafo de contexto executivo
3. Três seções <h2> com conteúdo técnico real, exemplos práticos e listas <ul>
4. <div class="insight-box"> com <span class="insight-label">Insight Inside Data</span> e um insight estratégico
5. <div class="cta-section"> com h3 "Pronto para estruturar seus dados?", parágrafo e dois links:
   - <a class="cta-button" href="https://grupolmtech.com.br/insidedata#contact">Agendar diagnóstico gratuito</a>
   - <a class="cta-button-sec" href="https://grupolmtech.com.br/downloads/business-case-onepager.pdf">Baixar one-pager</a>"""
    body = call_deepseek(prompt)
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower().strip())[:60].strip("-")
    html = build_full_html(body, {
        "title": topic,
        "seo_title": topic,
        "meta_description": f"Saiba mais sobre {topic} com a Inside Data, consultoria especializada em dados e cloud.",
        "category": "Blog",
        "read_time": "7",
    })
    return html, slug

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
            try:
                ftp.mkd(cfg["base_dir"])
            except ftplib.error_perm:
                pass
            ftp.storbinary(f"STOR {remote_path}", buf)
        return True, public_url
    except Exception as e:
        return False, str(e)

# ─── SMTP ─────────────────────────────────────────────────────────────────────
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

# ─── Render helpers ───────────────────────────────────────────────────────────
def render_article_actions(key_prefix: str, idea_title: str, idea_slug: str, html: str):
    col_ftp, col_mail, col_both, col_dl = st.columns(4)
    with col_ftp:
        if st.button("💾 DEPLOY FTP", key=f"{key_prefix}_ftp"):
            with st.spinner("Enviando para Locaweb..."):
                ok, result = deploy_ftp(html, idea_slug)
                if ok: st.success(f"✓ Publicado! [Ver artigo]({result})")
                else:  st.error(f"FTP: {result}")
    with col_mail:
        if st.button("📧 ENVIAR E-MAIL", key=f"{key_prefix}_mail"):
            with st.spinner("Enviando..."):
                ok, result = send_email(html, f"[Inside Data SEO] {idea_title}")
                if ok: st.success(f"✓ Enviado para {result}")
                else:  st.error(f"SMTP: {result}")
    with col_both:
        if st.button("🚀 DEPLOY + E-MAIL", key=f"{key_prefix}_both"):
            with st.spinner("Salvando e enviando..."):
                ok1, r1 = deploy_ftp(html, idea_slug)
                ok2, r2 = send_email(html, f"[Inside Data SEO] {idea_title}")
                if ok1 and ok2: st.success(f"✓ Publicado + enviado! [Ver]({r1})")
                else:
                    if not ok1: st.error(f"FTP: {r1}")
                    if not ok2: st.error(f"SMTP: {r2}")
    with col_dl:
        st.download_button("⬇ BAIXAR HTML", data=html, file_name=f"{idea_slug}.html", mime="text/html", key=f"{key_prefix}_dl")

    with st.expander("👁 Prévia do artigo", expanded=False):
        components.html(html, height=600, scrolling=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="id-header">
  <div class="id-logo"><span class="id-dot"></span> INSIDE DATA — SEO COMMAND CENTER</div>
  <div class="id-traffic">+14.260 visitantes/mês</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visão Geral",
    "🏢 Concorrentes",
    "✍️ Pautas SEO",
    "💬 Gerar Artigo Livre",
    "🎨 Brand Brief",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Tráfego Potencial",     "+14.260", "visitantes/mês")
    c2.metric("Pautas Identificadas",  "5",        "artigos estratégicos")
    c3.metric("Concorrentes",          "5",        "mapeados")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="id-card"><div class="sec-title">Top Content Opportunities</div>', unsafe_allow_html=True)
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
        c1, c2, c3, c4 = st.columns([0.5, 4, 1.5, 1.5])
        c1.markdown(f"<span style='font-family:Space Mono,monospace;color:#7FA8BE;font-size:12px'>#{str(i+1).zfill(2)}</span>", unsafe_allow_html=True)
        c2.markdown(f"<div style='font-weight:600;font-size:15px'>{c['name']}</div><div style='color:#7FA8BE;font-size:12px'>{c['domain']}</div>", unsafe_allow_html=True)
        c3.markdown(f"<div style='font-family:Space Mono,monospace;color:#00BCD4;font-weight:700;font-size:18px;text-align:center'>{c['da']}</div><div style='color:#7FA8BE;font-size:10px;text-align:center'>Domain Auth.</div>", unsafe_allow_html=True)
        c4.markdown(threat_badge(c["threat"]), unsafe_allow_html=True)
        st.markdown("<hr style='border-color:rgba(0,188,212,0.1);margin:8px 0'>", unsafe_allow_html=True)
    st.markdown("""<div class="insight"><h4>💡 Insight Estratégico</h4>
      <p style="font-size:14px;line-height:1.7">KPMG, Deloitte e Accenture dominam termos genéricos mas raramente produzem
      conteúdo técnico profundo em PT-BR sobre implementações reais. A Inside Data tem vantagem em
      <strong style="color:#00BCD4">especificidade técnica + linguagem executiva BR</strong> — um gap que o conteúdo SEO deve explorar.</p>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PAUTAS SEO (hardcoded, editáveis)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<p style='color:#7FA8BE;font-size:14px;margin-bottom:20px'>Pautas mapeadas com potencial de tráfego orgânico. Gere, visualize e publique.</p>", unsafe_allow_html=True)
    for idea in IDEAS:
        st.markdown(f"""
        <div class="id-card-alt">
          <span class="chip chip-cat">{idea['category']}</span>
          <span class="chip chip-int">{idea['intent']}</span>
          <span class="chip chip-diff">Dif: {idea['difficulty']}</span>
          <div style="font-size:16px;font-weight:600;margin:8px 0">{idea['title']}</div>
          {tbar(idea['traffic'])}
        </div>""", unsafe_allow_html=True)

        already = idea["id"] in st.session_state.generated
        col_gen, _ = st.columns([2, 6])
        with col_gen:
            label = "↺ REGENERAR" if already else "✦ GERAR ARTIGO"
            if st.button(label, key=f"gen_{idea['id']}"):
                with st.spinner(f"Gerando '{idea['title']}'..."):
                    try:
                        html = generate_from_idea(idea)
                        st.session_state.generated[idea["id"]] = {"html": html, "slug": idea["slug"], "title": idea["title"]}
                        st.success("✓ Artigo gerado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro na API: {e}")

        if already:
            d = st.session_state.generated[idea["id"]]
            render_article_actions(f"idea_{idea['id']}", d["title"], d["slug"], d["html"])

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CHAT LIVRE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<p style='color:#7FA8BE;font-size:14px;margin-bottom:20px'>Peça qualquer artigo em linguagem natural. Ex: <em>\"post sobre data mesh para times de engenharia\"</em></p>", unsafe_allow_html=True)

    # Histórico de artigos gerados via chat
    for i, entry in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(entry["topic"])
        with st.chat_message("assistant"):
            st.write(f"✓ Artigo gerado: **{entry['topic']}**")
            render_article_actions(f"chat_{i}", entry["topic"], entry["slug"], entry["html"])

    # Input
    topic = st.chat_input("Sobre o que você quer um artigo?")
    if topic:
        with st.chat_message("user"):
            st.write(topic)
        with st.chat_message("assistant"):
            with st.spinner("Gerando artigo..."):
                try:
                    html, slug = generate_from_chat(topic)
                    st.session_state.chat_history.append({"topic": topic, "html": html, "slug": slug})
                    st.write(f"✓ Artigo gerado: **{topic}**")
                    render_article_actions(f"chat_{len(st.session_state.chat_history)-1}", topic, slug, html)
                except Exception as e:
                    st.error(f"Erro na API: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — BRAND BRIEF
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""<div class="id-card"><div class="sec-title">Sobre a Empresa</div>
          <p style="font-size:14px;line-height:1.75">Consultoria executiva especializada em
          <strong style="color:#00BCD4">Arquitetura, Engenharia e Governança de Dados</strong>.
          Diferencial: posicionamento <strong style="color:#00BCD4">agnóstico em cloud</strong> — AWS, Azure e GCP —
          com foco em clareza operacional, segurança, compliance e valor mensurável.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="id-card"><div class="sec-title">Tom & Voz</div>
          <p style="font-size:14px;line-height:1.7">Comunicação <strong>consultiva, técnica e executiva</strong>.
          Autoridade, objetividade e precisão — maturidade estratégica e profundidade de engenharia.</p>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""<div class="id-card"><div class="sec-title">Público-Alvo</div>
          <p style="font-size:14px;line-height:1.7"><strong>Diretores, Heads de Dados, tecnologia, engenharia e
          transformação digital</strong> em empresas com múltiplos sistemas e alto volume de dados.</p>
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
            st.markdown(f'<div class="theme-item"><span class="theme-num">{str(i+1).zfill(2)}</span><span style="font-size:13px;line-height:1.5">{theme}</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
