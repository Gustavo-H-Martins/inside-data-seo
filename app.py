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
.stApp { background-color: #000000; color: #ffffff; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.id-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 20px 0; border-bottom: 1px solid rgba(33,186,231,0.18); margin-bottom: 24px;
}
.id-logo { font-family: 'Space Mono', monospace; font-size: 13px; color: #21bae7; letter-spacing: 1.2px; display: flex; align-items: center; gap: 10px; }
.id-dot  { width: 8px; height: 8px; border-radius: 50%; background: #21bae7; box-shadow: 0 0 10px #21bae7; display: inline-block; }
.id-traffic { background: rgba(33,186,231,0.08); border: 1px solid rgba(33,186,231,0.18); border-radius: 8px; padding: 6px 16px; font-family: 'Space Mono', monospace; color: #21bae7; font-size: 14px; font-weight: 700; }

.id-card     { background: #101010; border: 1px solid rgba(33,186,231,0.14); border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.id-card-alt { background: #141414; border: 1px solid rgba(33,186,231,0.10); border-radius: 12px; padding: 18px; margin-bottom: 12px; }
.id-card-alt:hover { border-color: rgba(33,186,231,0.30); }

.sec-title { font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #888888; margin-bottom: 14px; }

.tbar-wrap  { display: flex; align-items: center; gap: 10px; margin-top: 6px; }
.tbar-track { flex: 1; height: 5px; background: rgba(255,255,255,.06); border-radius: 3px; overflow: hidden; }
.tbar-fill  { height: 100%; border-radius: 3px; background: linear-gradient(90deg,#21bae7,#5cc8ee); }
.tbar-val   { font-family: 'Space Mono', monospace; color: #21bae7; font-weight: 700; font-size: 13px; min-width: 56px; text-align: right; }

.chip      { border-radius: 4px; padding: 2px 9px; font-size: 11px; font-weight: 600; display: inline-block; margin-right: 4px; }
.chip-cat  { background: rgba(33,186,231,0.10); color: #21bae7; }
.chip-int  { background: rgba(255,255,255,.04); color: #888888; }
.chip-diff { background: rgba(255,255,255,.04); color: #888888; }

.threat-high   { background: rgba(239,68,68,.15);  color: #F87171; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }
.threat-medium { background: rgba(251,191,36,.15); color: #FCD34D; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }
.threat-low    { background: rgba(52,211,153,.15); color: #6EE7B7; border-radius: 4px; padding: 2px 10px; font-size: 11px; font-weight: 700; }

.insight { background: rgba(33,186,231,0.06); border: 1px solid rgba(33,186,231,0.14); border-radius: 10px; padding: 18px; margin-top: 16px; }
.insight h4 { color: #21bae7; font-size: 13px; font-weight: 700; margin-bottom: 8px; }

.theme-item { display: flex; gap: 10px; padding: 10px 14px; background: rgba(33,186,231,.04); border: 1px solid rgba(33,186,231,0.12); border-radius: 8px; margin-bottom: 8px; }
.theme-num  { font-family: 'Space Mono', monospace; font-size: 11px; color: #21bae7; margin-top: 2px; }

.swatch-row { display: flex; gap: 14px; flex-wrap: wrap; }
.swatch     { text-align: center; }
.swatch-box { width: 50px; height: 50px; border-radius: 10px; border: 2px solid rgba(255,255,255,.08); margin-bottom: 5px; }
.swatch-name { color: #888888; font-size: 11px; }
.swatch-hex  { font-family: 'Space Mono', monospace; color: #21bae7; font-size: 10px; }

div[data-testid="stTabs"] button { color: #888888 !important; font-family: 'DM Sans', sans-serif !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #21bae7 !important; border-bottom-color: #21bae7 !important; }
div[data-testid="stTabs"] { border-bottom: 1px solid rgba(33,186,231,0.14); }
.stButton > button {
    background: #21bae7 !important;
    color: #000000 !important; border: none !important;
    font-family: 'Space Mono', monospace !important; font-size: 11px !important;
    font-weight: 700 !important; letter-spacing: .5px !important; border-radius: 8px !important;
}
.stButton > button:hover { opacity: .85 !important; }
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    background: #141414 !important; border: 1px solid rgba(33,186,231,0.14) !important;
    color: #ffffff !important; border-radius: 8px !important;
}
div[data-testid="stMetric"] { background: #101010; border: 1px solid rgba(33,186,231,0.12); border-radius: 14px; padding: 16px; }
div[data-testid="stMetric"] label { color: #888888 !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #21bae7 !important; font-family: 'Space Mono', monospace !important; }
div[data-testid="stChatMessage"] { background: #101010 !important; border: 1px solid rgba(33,186,231,0.10) !important; border-radius: 12px !important; }
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
  <meta name="robots" content="index, follow"/>
  <link rel="canonical" href="https://grupolmtech.com.br/insidedata/blog/{slug}"/>
  <style>
    *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
    html{{scroll-behavior:smooth}}
    body{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#000;color:#fff;line-height:1.7;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}

    /* ── NAV ── */
    nav{{position:sticky;top:0;z-index:100;background:rgba(0,0,0,.85);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid rgba(33,186,231,.12);padding:0 max(5vw,24px);display:flex;align-items:center;justify-content:space-between;height:64px}}
    .nav-logo img{{height:32px;width:auto;object-fit:contain}}
    .nav-links{{display:flex;gap:28px;list-style:none;align-items:center}}
    .nav-links a{{color:#bfbfbf;text-decoration:none;font-size:14px;font-weight:500;transition:color .2s}}
    .nav-links a:hover{{color:#21bae7}}
    .nav-cta{{background:#21bae7!important;color:#000!important;padding:8px 20px;border-radius:50px;font-weight:700!important;font-size:13px!important;transition:opacity .2s}}
    .nav-cta:hover{{opacity:.85}}
    @media(max-width:768px){{.nav-links{{display:none}}}}

    /* ── HERO ── */
    .hero{{padding:80px max(5vw,24px) 64px;border-bottom:1px solid rgba(33,186,231,.10);background:linear-gradient(180deg,#000 0%,#0a0a0a 100%)}}
    .hero-inner{{max-width:960px;margin:0 auto}}
    .hero-badge{{display:inline-block;background:rgba(33,186,231,.10);color:#21bae7;border:1px solid rgba(33,186,231,.22);border-radius:50px;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:24px}}
    .hero h1{{font-size:clamp(1.8rem,4.5vw,2.8rem);font-weight:700;color:#fff;line-height:1.2;letter-spacing:-0.02em;margin-bottom:16px}}
    .hero h1 span{{color:#21bae7}}
    .hero-subtitle{{font-size:1.1rem;color:#bfbfbf;line-height:1.6;margin-bottom:24px;max-width:680px}}
    .hero-meta{{display:flex;gap:24px;flex-wrap:wrap;font-size:13px;color:#888}}

    /* ── SECTIONS ── */
    .section{{padding:80px max(5vw,24px)}}
    .section-dark{{background:#0a0a0a}}
    .container{{max-width:960px;margin:0 auto}}

    .section-label{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#21bae7;margin-bottom:16px;background:rgba(33,186,231,.08);padding:4px 12px;border-radius:4px}}

    h2{{font-size:clamp(1.5rem,3.5vw,2rem);font-weight:700;color:#fff;line-height:1.25;letter-spacing:-0.02em;margin-bottom:24px}}
    h3{{font-size:1.15rem;font-weight:700;color:#fff;margin-bottom:12px}}
    p{{font-size:1.05rem;color:#bfbfbf;line-height:1.75;margin-bottom:1.2rem}}
    strong{{color:#fff;font-weight:600}}
    ul,ol{{margin:0 0 1.5rem 1.5rem;color:#bfbfbf}}
    li{{font-size:1.02rem;margin-bottom:.5rem;line-height:1.65}}
    li::marker{{color:#21bae7}}

    /* ── CARDS ── */
    .card{{background:#141414;border:1px solid rgba(33,186,231,.14);border-radius:16px;padding:28px;transition:border-color .3s}}
    .card:hover{{border-color:rgba(33,186,231,.30)}}
    .card h3{{margin-bottom:8px}}
    .card p{{font-size:.98rem;margin-bottom:0}}

    /* ── GRIDS ── */
    .grid-2{{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}}
    .grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
    .grid-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
    @media(max-width:768px){{.grid-2,.grid-3,.grid-4{{grid-template-columns:1fr}}}}

    /* ── STATS ── */
    .stat-number{{font-family:'SF Mono','Fira Code','Cascadia Code',monospace;font-size:2.2rem;font-weight:700;color:#21bae7;line-height:1.1;margin-bottom:6px}}
    .stat-label{{font-size:.85rem;color:#888}}

    /* ── QUOTE ── */
    .quote-block{{background:#0a0a0a;border-left:3px solid #21bae7;border-radius:0 12px 12px 0;padding:24px 28px;margin:32px 0}}
    .quote-block p{{font-size:1.1rem;color:#e0e0e0;font-style:italic;margin-bottom:8px}}
    .quote-block .quote-author{{font-size:.85rem;color:#888;font-style:normal}}

    /* ── DIVIDER ── */
    .divider{{width:100%;height:1px;background:rgba(33,186,231,.10);margin:0}}

    /* ── CTA BLOCK ── */
    .cta-block{{background:linear-gradient(135deg,rgba(33,186,231,.06),rgba(33,186,231,.02));border:1px solid rgba(33,186,231,.18);border-radius:24px;padding:48px;text-align:center;margin:20px 0}}
    .cta-block h2{{margin-bottom:12px}}
    .cta-block p{{max-width:600px;margin:0 auto 28px;font-size:1.05rem}}
    .cta-block .btn-row{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}}

    .cta-button{{display:inline-block;background:#21bae7;color:#000;font-weight:700;font-size:1rem;padding:14px 36px;border-radius:50px;text-decoration:none;letter-spacing:.02em;transition:all .25s;border:2px solid #21bae7}}
    .cta-button:hover{{background:#1aa3cc;border-color:#1aa3cc;transform:translateY(-1px)}}

    .cta-button-ghost{{display:inline-block;color:#fff;font-weight:600;font-size:1rem;padding:14px 36px;border-radius:50px;text-decoration:none;border:2px solid rgba(255,255,255,.25);transition:all .25s}}
    .cta-button-ghost:hover{{border-color:#21bae7;color:#21bae7;transform:translateY(-1px)}}

    /* ── FAQ ── */
    details{{background:#141414;border:1px solid rgba(33,186,231,.12);border-radius:12px;padding:0;margin-bottom:10px;overflow:hidden;transition:border-color .2s}}
    details:hover{{border-color:rgba(33,186,231,.25)}}
    details[open]{{border-color:rgba(33,186,231,.30)}}
    summary{{padding:18px 24px;font-weight:600;font-size:1rem;color:#fff;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;user-select:none}}
    summary::-webkit-details-marker{{display:none}}
    summary::after{{content:"+";font-size:1.3rem;color:#21bae7;font-weight:400;transition:transform .2s}}
    details[open] summary::after{{content:"\2212"}}
    details .faq-answer{{padding:0 24px 20px;color:#bfbfbf;font-size:.98rem;line-height:1.7}}

    /* ── FOOTER ── */
    footer{{background:#000;border-top:1px solid rgba(33,186,231,.10);padding:56px max(5vw,24px) 32px}}
    .footer-inner{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px}}
    .footer-brand img{{height:40px;width:auto;object-fit:contain;margin-bottom:14px}}
    .footer-brand p{{color:#888;font-size:13px;line-height:1.6}}
    .footer-col h4{{color:#fff;font-size:12px;font-weight:700;margin-bottom:14px;text-transform:uppercase;letter-spacing:.8px}}
    .footer-col ul{{list-style:none;margin:0}}
    .footer-col ul li{{margin-bottom:8px}}
    .footer-col ul li a{{color:#888;text-decoration:none;font-size:13px;transition:color .2s}}
    .footer-col ul li a:hover{{color:#21bae7}}
    .footer-bottom{{max-width:1100px;margin:40px auto 0;padding-top:24px;border-top:1px solid rgba(255,255,255,.06);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
    .footer-bottom p{{color:#666;font-size:12px}}
    .social-links{{display:flex;gap:14px}}
    .social-links a{{color:#888;font-size:13px;text-decoration:none;transition:color .2s}}
    .social-links a:hover{{color:#21bae7}}
    @media(max-width:768px){{.footer-inner{{grid-template-columns:1fr 1fr}}.footer-brand{{grid-column:1/-1}}}}

    /* ── UTILS ── */
    .text-center{{text-align:center}}
    .mt-0{{margin-top:0}}
    .mb-0{{margin-bottom:0}}

    /* ── MERMAID DIAGRAMS ── */
    .diagram-card{{background:#0a0a0a;border:1px solid rgba(33,186,231,.14);border-radius:16px;padding:32px 24px;margin:32px 0;overflow-x:auto}}
    .diagram-card .mermaid{{display:flex;justify-content:center}}
    .diagram-card .mermaid svg{{max-width:100%;height:auto}}
    .diagram-caption{{text-align:center;color:#888;font-size:.85rem;margin-top:16px;font-style:italic}}
    .diagram-label{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#21bae7;margin-bottom:8px;background:rgba(33,186,231,.08);padding:4px 10px;border-radius:4px}}

    /* ── MERMAID THEME OVERRIDES ── */
    .mermaid .node rect,.mermaid .node circle,.mermaid .node polygon{{fill:#141414!important;stroke:rgba(33,186,231,.30)!important}}
    .mermaid .edgePath .path{{stroke:rgba(33,186,231,.40)!important}}
    .mermaid .edgeLabel rect{{fill:#0a0a0a!important}}
    .mermaid .edgeLabel span{{color:#bfbfbf!important}}
    .mermaid .nodeLabel,.mermaid .node text{{fill:#ffffff!important}}
    .mermaid .cluster rect{{fill:#0a0a0a!important;stroke:rgba(33,186,231,.18)!important}}
    .mermaid .cluster text,.mermaid .cluster span{{fill:#21bae7!important}}
    .mermaid .titleText{{fill:#ffffff!important}}
    .mermaid g.stateGroup rect{{fill:#141414!important;stroke:rgba(33,186,231,.25)!important}}
    .mermaid g.stateGroup text{{fill:#ffffff!important}}
  </style>
  <script>
    document.addEventListener('DOMContentLoaded',function(){{
      mermaid.initialize({{startOnLoad:true,theme:'dark',themeVariables:{{primaryColor:'#141414',primaryBorderColor:'rgba(33,186,231,.30)',primaryTextColor:'#ffffff',lineColor:'rgba(33,186,231,.40)',secondaryColor:'#0a0a0a',tertiaryColor:'#141414'}},securityLevel:'loose'}});
    }});
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-logo">
    <img src="https://grupolmtech.com.br/images/logo_secondary.png" alt="Inside Data Consultoria" width="180" height="32" style="height:32px;width:auto;object-fit:contain"/>
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
    <p class="hero-subtitle">{hero_subtitle}</p>
    <div class="hero-meta">
      <span>{publish_date}</span>
      <span>{read_time} min de leitura</span>
      <span>Inside Data</span>
    </div>
  </div>
</div>

<!-- PAGE CONTENT (gerado pelo modelo) -->
<main class="page-content">
  {article_body}
</main>

<!-- FOOTER -->
<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <img src="https://grupolmtech.com.br/images/logo_primary.png" alt="Inside Data" width="180" height="40" style="height:40px;width:auto;object-fit:contain"/>
      <p>Consultoria especializada em Arquitetura, Engenharia e Governança de Dados. Posicionamento agnóstico em cloud com foco em resultado mensurável.</p>
    </div>
    <div class="footer-col">
      <h4>Serviços</h4>
      <ul>
        <li><a href="https://grupolmtech.com.br/insidedata#services">Arquitetura de Dados</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#services">Engenharia de Dados</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#services">Governança & LGPD</a></li>
        <li><a href="https://grupolmtech.com.br/insidedata#services">FinOps & Cloud</a></li>
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
        <li><a href="https://wa.me/5531982273761">(31) 98227-3761</a></li>
        <li><a href="#">Lagoa Santa — MG</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© {year} Inside Data Consultoria. Todos os direitos reservados. | CNPJ: 55.299.485/0001-58</p>
    <div class="social-links">
      <a href="https://www.linkedin.com/company/insidedatabr/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://github.com/insidedatabr" target="_blank" rel="noopener">GitHub</a>
      <a href="https://www.instagram.com/insidedata.br/" target="_blank" rel="noopener">Instagram</a>
    </div>
  </div>
</footer>

<script>mermaid.initialize({{startOnLoad:true,theme:'dark',securityLevel:'loose'}});</script>
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
    """Injeta o corpo da landing page no template."""
    return ARTICLE_HTML_TEMPLATE.format(
        seo_title=meta.get("seo_title", meta["title"]),
        meta_description=meta.get("meta_description", ""),
        h1_title=meta["title"],
        hero_subtitle=meta.get("hero_subtitle", ""),
        category=meta.get("category", "Blog"),
        slug=meta.get("slug", ""),
        publish_date=datetime.now().strftime("%d/%m/%Y"),
        read_time=meta.get("read_time", "7"),
        article_body=article_body,
        year=datetime.now().year,
    )

# ─── DeepSeek API ─────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT EM 5 CAMADAS — Inside Data Authority Page Generator
# ═══════════════════════════════════════════════════════════════════════════════

# ─── CAMADA 1: PERSONA ───────────────────────────────────────────────────────
PERSONA_LAYER = """
Você é Principal Data Architect e Consultor Sênior da Inside Data.

Possui mais de 20 anos implementando plataformas modernas de dados em grandes empresas.
Já liderou projetos de arquitetura, engenharia e governança em dezenas de organizações
dos mais variados setores: financeiro, varejo, indústria, saúde, logística e governo.

Especialista em:
• Databricks
• Snowflake
• Engenharia de Dados
• Data Lakehouse
• IA aplicada a dados
• Cloud FinOps
• Governança de Dados
• BI e Analytics
• Arquitetura Corporativa de Dados
• Modernização de plataformas legadas

Seu trabalho NÃO é escrever artigos de blog.
Seu trabalho é demonstrar autoridade técnica da Inside Data e convencer um executivo
de que existe um caminho mais inteligente para resolver seus problemas de dados.

Você escreve como uma consultoria premium — no nível de McKinsey, BCG, Accenture, Deloitte.
Seu conteúdo deve parecer um white paper executivo, não um post de blog.
"""

# ─── CAMADA 2: EDITORIAL ─────────────────────────────────────────────────────
EDITORIAL_LAYER = """
## PÚBLICO-ALVO (ESCREVA EXCLUSIVAMENTE PARA ELES)

Seu leitor é:
• CIO — Chief Information Officer
• CTO — Chief Technology Officer
• CDO — Chief Data Officer
• Diretor de Dados e Analytics
• Head de Engenharia de Dados
• Gerente de Plataformas Cloud
• Arquiteto Corporativo
• Head de DataOps e Infraestrutura

Seu leitor tem 10+ anos de experiência em tecnologia.
Ele conhece os conceitos. Ele já leu centenas de artigos.
Ele não precisa de definições. Ele precisa de profundidade, diagnóstico e caminhos.

## REGRAS DE OURO — NUNCA FAÇA ISSO

NUNCA escreva para iniciantes.
NUNCA explique conceitos básicos.
NUNCA defina o que é Data Lake, Lakehouse, Data Warehouse, ETL, ELT ou BI.
NUNCA explique IA, Machine Learning ou GenAI de forma genérica e introdutória.
NUNCA use frases de blogueiro repetitivo.

## PALAVRAS E FRASES PROIBIDAS (NUNCA USE NENHUMA DESTAS)

Proibido:
• "A importância dos dados"
• "O poder da IA" / "O poder dos dados"
• "No mundo atual" / "No mundo de hoje"
• "Vivemos uma transformação digital"
• "As empresas precisam inovar"
• "Os dados são o novo petróleo"
• "Na era da informação"
• "Cada vez mais"
• "A tecnologia avança rapidamente"
• "É fundamental" / "É essencial" / "É crucial"
• "Sem dúvida"
• "Podemos afirmar que"
• "Não é novidade que"
• "Estamos vivendo"
• "O cenário atual"
• "Desafios do mercado"

Se você sentir vontade de usar qualquer uma dessas frases, pare e reescreva com
um exemplo concreto de projeto.

## TOM E VOZ

• Consultivo, não professoral
• Técnico, não acadêmico
• Executivo, não marketeiro
• Direto, não prolixo
• Experiente, não teórico
• Estratégico, não tático

Você não está "explicando" nada. Você está compartilhando achados de campo.

## REGRA DE EXPERIÊNCIA

Sempre escreva como alguém que já participou de dezenas de projetos reais.
Cada afirmação técnica deve vir acompanhada de um exemplo de campo.

Exemplos do tom correto:
"Em muitos projetos encontramos clusters Databricks superdimensionados
consumindo recursos durante toda a madrugada sem necessidade operacional."

"Nossa experiência mostra que tabelas Snowflake sem estratégia de clustering
costumam aumentar significativamente o custo conforme o volume cresce."

"É comum encontrar pipelines que executam centenas de transformações
desnecessárias apenas porque nunca foram revisados."

"Em diagnósticos de FinOps, identificamos que em média 35% do spend mensal
de cloud para dados é evitável com ajustes de arquitetura e governança."

## REGRA DE EXEMPLOS REAIS

Cada seção precisa conter pelo menos um cenário concreto encontrado em empresas.
Nunca escrever apenas teoria. Sempre ancorar em experiência de campo.

Exemplo ERRADO:
"Databricks melhora a performance de processamento de dados."

Exemplo CERTO:
"Em uma indústria com 12 milhões de registros diários de sensores IoT,
encontramos 47 notebooks Spark executando independentemente, muitos deles
processando as mesmas bases repetidas vezes. Após reorganizar os pipelines,
eliminar duplicidades e implementar orquestração por DAGs, o tempo total
de processamento caiu de 9 horas para 42 minutos, e o custo mensal com
DBUs reduziu 62%."

## VOCÊ NÃO VENDE TECNOLOGIA — VOCÊ VENDE DIAGNÓSTICO

Nunca diga:
"Contrate Databricks."
"Use Snowflake."
"Migre para Cloud."
"Implemente IA."

Sempre diga:
"Primeiro avaliamos a arquitetura atual."
"Depois identificamos gargalos e desperdícios."
"Só então propomos um roadmap de melhorias."
"A tecnologia é consequência do diagnóstico, nunca o ponto de partida."

A Inside Data não vende ferramentas. Vende conhecimento especializado e método.
"""

# ─── CAMADA 3: DESIGN SYSTEM ─────────────────────────────────────────────────
DESIGN_SYSTEM_LAYER = """
## IDENTIDADE VISUAL OBRIGATÓRIA — LANDING PAGE DE CONSULTORIA PREMIUM

Toda página deve transmitir a aparência de uma consultoria premium de tecnologia
— no nível de McKinsey, BCG, Accenture, Deloitte.

NUNCA gerar aparência de blog WordPress, Medium, TechCrunch ou artigo genérico.

### PALETA DE CORES (USO OBRIGATÓRIO)

• Fundo principal (body/sections alternadas): #000000
• Superfícies e seções: #0a0a0a
• Cards e blocos de destaque: #141414
• Bordas sutis: rgba(33, 186, 231, 0.18)
• Bordas em hover/destaque: rgba(33, 186, 231, 0.30)
• Azul institucional Inside Data: #21bae7
• Texto principal (headings, body): #ffffff
• Texto secundário (metadados, notas): #bfbfbf
• Texto terciário (legendas): #888888
• Gradientes: sempre usar #21bae7 como cor âncora

### TIPOGRAFIA

• Família: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif
• Headings: font-weight 700, letter-spacing -0.02em
• Body: font-size 1.05rem, line-height 1.75, font-weight 400
• Código/números: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace

### ESPAÇAMENTO E LAYOUT

• Container máximo: 960px centralizado
• Padding lateral em mobile: 5vw (aprox 20px)
• Espaçamento entre seções: 80px a 120px
• Espaçamento interno de seções: 64px a 80px
• Border-radius padrão: 16px
• Border-radius de cards internos: 12px
• Border-radius de botões: 50px (pill shape)
• Sombras: discretas, jamais exageradas

### COMPONENTES REUTILIZÁVEIS

Use estas classes CSS nos elementos que gerar (elas já existem no template):

• .section — seção padrão com padding e max-width
• .section-dark — seção com fundo #0a0a0a
• .section-label — label superior com azul institucional (ex: "PROBLEMA", "DIAGNÓSTICO")
• .card — card com fundo #141414, borda sutil, border-radius 12px
• .stat-number — números grandes com #21bae7 e font-mono
• .stat-label — label abaixo de números
• .quote-block — citação/depoimento estilizada
• .cta-button — botão CTA primário (fundo #21bae7, texto #000)
• .cta-button-ghost — botão CTA secundário (borda #21bae7, texto #fff)
• .divider — linha divisória sutil entre seções
• .grid-2, .grid-3, .grid-4 — grids responsivos

### LOGO DA INSIDE DATA

A logo da Inside Data deve sempre:
• Ser inserida via <img> com src="https://grupolmtech.com.br/images/logo_secondary.png"
• Permanecer proporcional (nunca distorcer)
• Nunca ultrapassar 200px de largura
• Usar height="auto" e object-fit: contain
• Ter padding adequado ao redor
• Manter boa legibilidade em desktop e mobile
"""

# ─── CAMADA 4: CONVERSÃO ─────────────────────────────────────────────────────
CONVERSION_LAYER = """
## DNA INSIDE DATA — ATUAÇÃO OBRIGATÓRIA EM TODO CONTEÚDO

Toda landing page deve reforçar que a Inside Data atua em:

• Arquitetura de Dados (desenho, seleção de tecnologias, padrões)
• Engenharia de Dados (pipelines, ingestão, transformação, orquestração)
• Governança de Dados (catálogo, qualidade, linhagem, metadados)
• FinOps para Dados (otimização de custos cloud, redução de spend)
• IA Aplicada a Dados (casos de uso reais, não hype)
• Modernização de Plataformas (legado → cloud, migrações)
• Observabilidade de Dados (monitoramento, alertas, SLAs)
• Performance e Tuning (SQL, Spark, clusters, queries)
• Capacitação de Equipes (treinamento técnico, mentoria)
• Sustentação e Operação Assistida (managed services)

Nunca vender APENAS ferramentas.
Sempre vender conhecimento especializado, método e resultado mensurável.

## OBJEÇÕES A ENDEREÇAR IMPLICITAMENTE

O conteúdo deve naturalmente responder estas objeções sem parecer defensivo:
• "Já temos time interno de dados."
• "Já usamos [Databricks/Snowflake/AWS]."
• "Consultoria é cara e não entrega."
• "Isso não é prioridade agora."
• "Nosso case é muito específico."

## ESTRUTURA DE CTA (CALL TO ACTION)

No mínimo 2 CTAs por página:
1. Um CTA de meio de página — diagnóstico ou avaliação
2. Um CTA de fim de página — contato direto

CTAs devem focar em:
• "Agendar diagnóstico de arquitetura"
• "Solicitar avaliação de FinOps"
• "Falar com um especialista"
• "Receber uma análise preliminar"

NUNCA usar CTAs genéricos como "Saiba mais" ou "Clique aqui".
Sempre usar verbos de ação com valor percebido claro.

## PROVA DE AUTORIDADE (USAR NATURALMENTE)

• Mencionar experiência acumulada em projetos reais
• Citar cenários complexos já resolvidos
• Demonstrar profundidade técnica sem arrogância
• Usar dados e métricas de projetos (sem expor clientes)
"""

# ─── CAMADA 5: TÉCNICA ───────────────────────────────────────────────────────
TECHNICAL_LAYER = """
## FORMATO DE SAÍDA

IMPORTANTE: Retorne APENAS o conteúdo HTML que vai dentro da tag <main class="page-content">.
NÃO inclua DOCTYPE, <html>, <head>, <body>, <nav>, <footer>.

O template já possui:
• <nav> com logo e links
• Hero wrapper estrutural
• <main class="page-content"> ← seu conteúdo entra AQUI
• <footer> completo

## ESTRUTURA OBRIGATÓRIA DA LANDING PAGE

Gere o conteúdo nesta ordem exata, usando as classes CSS fornecidas:

1. HERO CONTENT — Dentro de <div class="hero-content">:
   - <p class="section-label"> com a categoria/tema
   - <h1> com o título principal (incluir keyword)
   - <p class="hero-subtitle"> subtítulo de 1-2 frases com gancho executivo
   - Metadados: data, tempo de leitura

2. PROBLEMA — <section class="section"><div class="container">:
   - <p class="section-label">O PROBLEMA</p>
   - <h2> descrevendo o problema real (com exemplos de campo)
   - Parágrafos com dados concretos de projetos

3. CONSEQUÊNCIAS — <section class="section section-dark"><div class="container">:
   - <p class="section-label">O CUSTO DE NÃO AGIR</p>
   - <h2> impactos financeiros e operacionais
   - 3-4 cards (.card) com consequências específicas

4. DIAGNÓSTICO — <section class="section"><div class="container">:
   - <p class="section-label">COMO RESOLVER</p>
   - <h2> abordagem metodológica
   - Exemplos de diagnóstico e intervenção

4.5 ARQUITETURA & DIAGRAMAS — <section class="section section-dark"><div class="container">:
   - <p class="section-label">ARQUITETURA</p>
   - <h2> título contextual (ex: "Fluxo de Dados Recomendado", "Arquitetura-Alvo")
   - <div class="diagram-card"> contendo <div class="mermaid"> com diagrama Mermaid.js
   - <p class="diagram-caption"> legenda explicativa do diagrama
   - OBS: gere SEMPRE pelo menos 1 diagrama Mermaid relevante ao tema. Escolha o tipo certo:
     • graph LR/TB — para fluxos de dados, pipelines, arquiteturas
     • flowchart LR/TB — para processos de decisão, esteiras CI/CD
     • sequenceDiagram — para interações entre sistemas
     • stateDiagram-v2 — para ciclo de vida de dados
   - Use edge labels (-- Texto -->) para explicar o que trafega em cada etapa
   - Use subgraphs para agrupar domínios (ex: "Camada de Ingestão", "Camada de Processamento")
   - Exemplo de sintaxe Mermaid:
     <div class="mermaid">
     graph LR
       subgraph "Ingestão"
         ADF[Azure Data Factory] --> B[ADLS Gen2 - Raw]
       end
       subgraph "Processamento"
         B --> C[Databricks - Bronze]
         C --> D[Databricks - Silver]
         D --> E[Databricks - Gold]
       end
       subgraph "Consumo"
         E --> F[Power BI]
         E --> G[ML Models]
       end
     </div>

5. ATUAÇÃO INSIDE DATA — <section class="section"><div class="container">:
   - <p class="section-label">COMO A INSIDE DATA ATUA</p>
   - <h2> metodologia e diferenciais
   - Grid de serviços aplicáveis ao tema

6. CASES — <section class="section section-dark"><div class="container">:
   - <p class="section-label">CENÁRIOS REAIS</p>
   - <h2> situações que encontramos
   - 2-3 parágrafos com cenários de campo (sem nomes de clientes)

7. BENEFÍCIOS — <section class="section"><div class="container">:
   - <p class="section-label">RESULTADOS ESPERADOS</p>
   - Grid de 3-4 benefícios com métricas

8. CTA PRINCIPAL — <section class="section section-dark"><div class="container">:
   - <div class="cta-block"> com h2, parágrafo e 2 botões:
   - <a class="cta-button" href="https://grupolmtech.com.br/insidedata#contact">Agendar diagnóstico</a>
   - <a class="cta-button-ghost" href="https://grupolmtech.com.br/insidedata#services">Conhecer serviços</a>

9. FAQ — <section class="section"><div class="container">:
   - <p class="section-label">PERGUNTAS FREQUENTES</p>
   - 4-5 perguntas e respostas em formato <details><summary>

10. SCHEMA SEO — Dentro de <script type="application/ld+json">:
    - FAQPage schema com as perguntas do FAQ
    - Organization schema da Inside Data
    - WebPage schema

## REGRAS TÉCNICAS

• HTML válido e semanticamente correto
• Todas as classes CSS devem ser as fornecidas pelo template
• DIAGRAMAS MERMAID: gere SEMPRE pelo menos 1 diagrama na seção 4.5. Use sintaxe Mermaid.js
  dentro de <div class="mermaid">. Não use fences de código (```mermaid). O HTML com <div class="mermaid">
  já é suficiente para o Mermaid renderizar. Prefira graph, flowchart ou sequenceDiagram.
  NUNCA use sintaxe de outras ferramentas (PlantUML, Graphviz, etc.) — apenas Mermaid.js.
• Imagens: usar apenas a logo fornecida. Não inventar imagens.
• Links: sempre abrir na mesma aba (não usar target="_blank" exceto em redes sociais)
• NÃO usar markdown. NÃO usar fences de código (```). Retorne APENAS HTML.
• Não usar emojis no conteúdo (apenas nos metadados de data se apropriado)
• Não usar &nbsp; ou &mdash; como muletas de espaçamento
• O conteúdo deve ter entre 1500 e 2500 palavras
• Links: sempre abrir na mesma aba (não usar target="_blank" exceto em redes sociais)
• NÃO usar markdown. NÃO usar fences de código (```). Retorne APENAS HTML.
• Não usar emojis no conteúdo (apenas nos metadados de data se apropriado)
• Não usar &nbsp; ou &mdash; como muletas de espaçamento
• O conteúdo deve ter entre 1500 e 2500 palavras
"""

# ─── SYSTEM PROMPT COMPLETO ──────────────────────────────────────────────────
SYSTEM_PROMPT = f"""{PERSONA_LAYER}

---

{EDITORIAL_LAYER}

---

{DESIGN_SYSTEM_LAYER}

---

{CONVERSION_LAYER}

---

{TECHNICAL_LAYER}

---

CONTATO INSIDE DATA:
• Email: contato@grupolmtech.com.br
• WhatsApp: (31) 98227-3761
• Site: grupolmtech.com.br/insidedata
• LinkedIn: linkedin.com/company/insidedatabr
• Localização: Lagoa Santa — MG
• CNPJ: 55.299.485/0001-58
"""

def call_deepseek(user_prompt: str) -> str:
    client = OpenAI(
        api_key=st.secrets["deepseek"]["api_key"],
        base_url="https://api.deepseek.com/v1",
    )
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
    )
    return clean_html(response.choices[0].message.content)

def generate_from_idea(idea: dict) -> str:
    """Gera landing page de autoridade a partir de pauta mapeada."""
    prompt = f"""Gere uma LANDING PAGE DE AUTORIDADE (NÃO um artigo de blog) sobre:

TEMA: "{idea['title']}"
KEYWORD PRINCIPAL: "{idea['keyword']}"
INTENÇÃO DE BUSCA: {idea['intent']}
CATEGORIA: {idea['category']}

Aplique TODAS as regras do system prompt.
Siga a estrutura obrigatória de 10 seções (Hero Content até Schema SEO).
Inclua exemplos reais de campo em cada seção — nunca apenas teoria.
Use as classes CSS fornecidas (.section, .section-dark, .section-label, .card, .grid-2, .grid-3, .cta-button, .cta-button-ghost, .quote-block, details/summary para FAQ).
Gere conteúdo proprietário — nada de frases prontas de blog."""
    body = call_deepseek(prompt)
    return build_full_html(body, {
        "title": idea["title"],
        "seo_title": f"{idea['title']} | Inside Data",
        "meta_description": f"Diagnóstico especializado da Inside Data sobre {idea['keyword']}. Abordagem consultiva com exemplos reais de arquitetura, engenharia e governança de dados.",
        "hero_subtitle": f"Um diagnóstico técnico sobre {idea['keyword']} baseado em mais de 20 anos de projetos reais de dados.",
        "category": idea["category"],
        "slug": idea["slug"],
        "read_time": "8",
    })

def generate_from_chat(topic: str) -> tuple[str, str]:
    """Gera landing page de autoridade a partir de tema livre. Retorna (html_completo, slug)."""
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower().strip())[:60].strip("-")
    prompt = f"""Gere uma LANDING PAGE DE AUTORIDADE (NÃO um artigo de blog) sobre:

TEMA: "{topic}"

Você deve adaptar keyword, intenção, categoria e subtítulo automaticamente
para o público executivo da Inside Data.

Aplique TODAS as regras do system prompt.
Siga a estrutura obrigatória de 10 seções (Hero Content até Schema SEO).
Inclua exemplos reais de campo em cada seção — nunca apenas teoria.
Use as classes CSS fornecidas (.section, .section-dark, .section-label, .card, .grid-2, .grid-3, .cta-button, .cta-button-ghost, .quote-block, details/summary para FAQ).
Gere conteúdo proprietário — nada de frases prontas de blog."""
    body = call_deepseek(prompt)
    html = build_full_html(body, {
        "title": topic,
        "seo_title": f"{topic} | Inside Data",
        "meta_description": f"Análise especializada da Inside Data sobre {topic}. Diagnóstico técnico com exemplos reais de arquitetura de dados.",
        "hero_subtitle": f"Uma análise técnica sobre {topic} baseada em projetos reais de consultoria em dados.",
        "category": "Insight",
        "slug": slug,
        "read_time": "8",
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
        if st.button("DEPLOY FTP", key=f"{key_prefix}_ftp"):
            with st.spinner("Enviando para Locaweb..."):
                ok, result = deploy_ftp(html, idea_slug)
                if ok: st.success(f"✓ Publicado! [Ver artigo]({result})")
                else:  st.error(f"FTP: {result}")
    with col_mail:
        if st.button("ENVIAR E-MAIL", key=f"{key_prefix}_mail"):
            with st.spinner("Enviando..."):
                ok, result = send_email(html, f"[Inside Data SEO] {idea_title}")
                if ok: st.success(f"✓ Enviado para {result}")
                else:  st.error(f"SMTP: {result}")
    with col_both:
        if st.button("DEPLOY + E-MAIL", key=f"{key_prefix}_both"):
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
    "Visão Geral",
    "Concorrentes",
    "Pautas SEO",
    "Gerar Landing Page",
    "Brand Brief",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Tráfego Potencial",     "+14.260", "visitantes/mês")
    c2.metric("Pautas Identificadas",  "5",        "landing pages estratégicas")
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
        c1.markdown(f"<span style='font-family:Space Mono,monospace;color:#888888;font-size:12px'>#{str(i+1).zfill(2)}</span>", unsafe_allow_html=True)
        c2.markdown(f"<div style='font-weight:600;font-size:15px'>{c['name']}</div><div style='color:#888888;font-size:12px'>{c['domain']}</div>", unsafe_allow_html=True)
        c3.markdown(f"<div style='font-family:Space Mono,monospace;color:#21bae7;font-weight:700;font-size:18px;text-align:center'>{c['da']}</div><div style='color:#888888;font-size:10px;text-align:center'>Domain Auth.</div>", unsafe_allow_html=True)
        c4.markdown(threat_badge(c["threat"]), unsafe_allow_html=True)
        st.markdown("<hr style='border-color:rgba(33,186,231,0.08);margin:8px 0'>", unsafe_allow_html=True)
    st.markdown("""<div class="insight"><h4> Insight Estratégico</h4>
      <p style="font-size:14px;line-height:1.7">KPMG, Deloitte e Accenture dominam termos genéricos mas raramente produzem
      conteúdo técnico profundo em PT-BR sobre implementações reais. A Inside Data tem vantagem em
      <strong style="color:#21bae7">especificidade técnica + linguagem executiva BR</strong> — um gap que landing pages de autoridade devem explorar.</p>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PAUTAS SEO (hardcoded, editáveis)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<p style='color:#888888;font-size:14px;margin-bottom:20px'>Pautas mapeadas com potencial de tráfego orgânico. Gere landing pages de autoridade, visualize e publique.</p>", unsafe_allow_html=True)
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
            label = "↺ REGENERAR" if already else "✦ GERAR LANDING PAGE"
            if st.button(label, key=f"gen_{idea['id']}"):
                with st.spinner(f"Gerando '{idea['title']}'..."):
                    try:
                        html = generate_from_idea(idea)
                        st.session_state.generated[idea["id"]] = {"html": html, "slug": idea["slug"], "title": idea["title"]}
                        st.success("✓ Landing page gerada!")
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
    st.markdown("<p style='color:#888888;font-size:14px;margin-bottom:20px'>Solicite uma landing page de autoridade em linguagem natural. Ex: <em>\"data mesh para times de engenharia\"</em> ou <em>\"FinOps em ambientes multi-cloud\"</em></p>", unsafe_allow_html=True)

    # Histórico de artigos gerados via chat
    for i, entry in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(entry["topic"])
        with st.chat_message("assistant"):
            st.write(f"✓ Landing page gerada: **{entry['topic']}**")
            render_article_actions(f"chat_{i}", entry["topic"], entry["slug"], entry["html"])

    # Input
    topic = st.chat_input("Qual tema você quer abordar na landing page?")
    if topic:
        with st.chat_message("user"):
            st.write(topic)
        with st.chat_message("assistant"):
            with st.spinner("Gerando landing page..."):
                try:
                    html, slug = generate_from_chat(topic)
                    st.session_state.chat_history.append({"topic": topic, "html": html, "slug": slug})
                    st.write(f"✓ Landing page gerada: **{topic}**")
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
          <strong style="color:#21bae7">Arquitetura, Engenharia e Governança de Dados</strong>.
          Diferencial: posicionamento <strong style="color:#21bae7">agnóstico em cloud</strong> — AWS, Azure e GCP —
          com foco em clareza operacional, segurança, compliance e valor mensurável.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="id-card"><div class="sec-title">Tom & Voz</div>
          <p style="font-size:14px;line-height:1.7">Comunicação <strong>consultiva, técnica e executiva</strong>.
          Autoridade, objetividade e precisão — maturidade estratégica e profundidade de engenharia.
          Não escrevemos artigos de blog. Produzimos <strong style="color:#21bae7">landing pages de autoridade</strong>.</p>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""<div class="id-card"><div class="sec-title">Público-Alvo</div>
          <p style="font-size:14px;line-height:1.7"><strong>CIOs, CTOs, CDOs, Diretores de Dados, Heads de Engenharia e
          Arquitetos Corporativos</strong> em empresas com ambientes de dados complexos e alto volume.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="id-card"><div class="sec-title">Identidade Visual</div>', unsafe_allow_html=True)
        st.markdown("""<div class="swatch-row">
          <div class="swatch"><div class="swatch-box" style="background:#000000"></div><div class="swatch-name">Black</div><div class="swatch-hex">#000000</div></div>
          <div class="swatch"><div class="swatch-box" style="background:#21bae7"></div><div class="swatch-name">Blue</div><div class="swatch-hex">#21BAE7</div></div>
          <div class="swatch"><div class="swatch-box" style="background:#101010"></div><div class="swatch-name">Surface</div><div class="swatch-hex">#101010</div></div>
          <div class="swatch"><div class="swatch-box" style="background:#141414"></div><div class="swatch-name">Card</div><div class="swatch-hex">#141414</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="id-card"><div class="sec-title">Temas Estratégicos</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, theme in enumerate(THEMES):
        with cols[i % 2]:
            st.markdown(f'<div class="theme-item"><span class="theme-num">{str(i+1).zfill(2)}</span><span style="font-size:13px;line-height:1.5">{theme}</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
