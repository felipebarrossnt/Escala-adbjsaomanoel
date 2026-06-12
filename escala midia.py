"""
Gerador de Escala de Mídia — Instagram (Com Painel de Edição/Administrador)
Requisitos: pip3 install streamlit
Executar via terminal: streamlit run "escala midia.py"
"""

import streamlit as st
import calendar
import json
import os
import random
from datetime import date

# Configuração da página Web
st.set_page_config(page_title="Escala de Mídia — Instagram", layout="wide")

# ── Configurações Gerais ───────────────────────────────────────────
EQUIPE = ["Helloysa", "Estphany", "Jhennifer", ]
ANO = 2025
MES = 7  # Julho
ARQUIVO_DADOS = "dados_escala_direta.json"
SENHA_ADMIN = "midia123"  # Defina a senha que quiser aqui

MESES_PT = [
    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

CORES = [
    {"bg": "#E8F4FD", "border": "#5BA4CF", "text": "#1A3A52"},  # Azul
    {"bg": "#FDE8F4", "border": "#CF5BA4", "text": "#521A3A"},  # Rosa
    {"bg": "#E8FDE8", "border": "#5BCF5B", "text": "#1A521A"},  # Verde
    {"bg": "#FEF3C7", "border": "#D97706", "text": "#78350F"},  # Dourado (Santa Ceia)
]


# ── Funções de Persistência ────────────────────────────────────────
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# Inicializa estados no Streamlit
if "escala_fixa" not in st.session_state:
    st.session_state.escala_fixa = carregar_dados()

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "formulario_salvo" not in st.session_state:
    st.session_state.formulario_salvo = False

# Mapeia os dias do mês
cal_mes = calendar.monthcalendar(ANO, MES)
lista_sabados = []
for semana in cal_mes:
    sab = semana[5]
    if sab:
        lista_sabados.append(sab)
lista_sabados.sort()

# Define o 2º sábado automaticamente
DIA_SANTA_CEIA = lista_sabados[1] if len(lista_sabados) > 1 else lista_sabados[0]

# Filtra cronologicamente apenas o 2º Sábado e os Domingos
dias_filtrados = []
for semana in cal_mes:
    sab = semana[5]
    dom = semana[6]
    if sab == DIA_SANTA_CEIA:
        dias_filtrados.append((sab, "Santa Ceia"))
    if dom:
        dias_filtrados.append((dom, "Domingo"))
dias_filtrados.sort(key=lambda x: x[0])

# ── Estilização CSS Geral ──────────────────────────────────────────
st.markdown("""
<style>
    body, .stApp { background-color: #0F0F14; }
    .login-container { max-width: 500px; margin: 80px auto; padding: 40px; background: #18181F; border: 1px solid #2A2A38; border-radius: 12px; text-align: center; }
    .login-title { color: #FFF; font-size: 1.8rem; font-weight: 700; margin-bottom: 8px; }
    .login-subtitle { color: #6B6480; font-size: .85rem; margin-bottom: 24px; }
    .custom-header { text-align: center; margin-bottom: 40px; }
    .custom-header .eyebrow { font-size: .65rem; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: #8B7FCC; margin-bottom: 10px; }
    .custom-header h1 { font-size: 2.3rem; font-weight: 700; letter-spacing: -.02em; color: #fff; line-height: 1.1; }
    .custom-header h1 span { color: #A78BFA; }
    .custom-header .sub { margin-top: 10px; font-size: .85rem; color: #6B6480; font-weight: 400; }
    .cal-wrap { background: #18181F; border: 1px solid #2A2A38; border-radius: 12px; overflow: hidden; margin-bottom: 32px; }
    .cal-grid { display: grid; grid-template-columns: 1fr; gap: 1px; background: #2A2A38; }
    .dia { background: #18181F; min-height: 90px; padding: 14px 16px; position: relative; display: flex; flex-direction: row; justify-content: space-between; align-items: center; border-bottom: 1px solid #2A2A38; }
    .dia.domingo .num { color: #F97316; }
    .dia.santa_ceia .num { color: #FEF3C7; }
    .dia .num { font-size: .95rem; font-weight: 700; color: #555; min-width: 180px; }
    .dia.tem-escala { background: #1C1C28; }
    .badge { border: 1px solid; border-radius: 6px; padding: 8px 14px; font-size: .75rem; line-height: 1.4; text-align: left; min-width: 250px;}
    .badge-nome { display: block; font-weight: 700; }
    .badge-tarefas { display: block; opacity: .75; font-size: .65rem; margin-top: 2px; }
    .resumo-titulo { font-size: .65rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: #555; margin-bottom: 16px; margin-top: 20px; }
    .pessoa-card { background: #18181F; border-radius: 8px; padding: 16px 18px; margin-bottom: 10px; border: 1px solid #2A2A38; height: 100%; }
    .pessoa-nome { font-size: .95rem; font-weight: 700; margin-bottom: 10px; }
    .pessoa-lista { list-style: none; padding-left: 0; display: flex; flex-direction: column; gap: 6px; }
    .pessoa-lista li { font-size: .78rem; color: #9990B0; }
    .parceiro { font-size: .72rem; color: #6B6480; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ── FLUXO 1: SELEÇÃO DE INTEGRANTE ───────────────────────────────────
if st.session_state.usuario_logado is None:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">👋 Quem está acessando?</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Escolha seu nome para informar seus dias livres</div>',
                unsafe_allow_html=True)

    usuario_input = st.selectbox("Escolha seu perfil:", ["Selecione..."] + EQUIPE, label_visibility="collapsed")

    if usuario_input != "Selecione...":
        if st.button(f"✨ Avançar", use_container_width=True):
            st.session_state.usuario_logado = usuario_input
            st.session_state.formulario_salvo = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── FLUXO 2: FORMULÁRIO DE DISPONIBILIDADE ───────────────────────────
elif not st.session_state.formulario_salvo:
    usuario_atual = st.session_state.usuario_logado

    st.markdown('<div class="login-container" style="max-width: 600px; text-align: left;">', unsafe_allow_html=True)
    st.markdown(f'<div class="login-title" style="text-align: center;">📅 Seus dias livres, {usuario_atual}?</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<p style="color: #6B6480; font-size: .9rem; text-align: center; margin-bottom: 30px;">Marque os dias em que você está livre. O sistema ajustará as duplas automaticamente:</p>',
        unsafe_allow_html=True)

    respostas = {}
    for d, tipo in dias_filtrados:
        texto_dia = f"Dia {d:02d} — Sábado 🍞 (Santa Ceia)" if tipo == "Santa Ceia" else f"Dia {d:02d} — Domingo"

        chave_d = str(d)
        valor_padrao = True
        if chave_d in st.session_state.escala_fixa:
            valor_padrao = usuario_atual in st.session_state.escala_fixa[chave_d].get("disponiveis", [])

        respostas[d] = st.checkbox(texto_dia, value=valor_padrao, key=f"form_{d}")

    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("💾 Salvar e Ver Calendário", use_container_width=True):
        for d, livre in respostas.items():
            chave_d = str(d)
            tipo_dia = "Santa Ceia" if d == DIA_SANTA_CEIA else "Domingo"

            if chave_d not in st.session_state.escala_fixa:
                st.session_state.escala_fixa[chave_d] = {"disponiveis": [], "tipo": tipo_dia, "forcado": []}

            lista_disp = st.session_state.escala_fixa[chave_d].get("disponiveis", [])

            if livre and (usuario_atual not in lista_disp):
                lista_disp.append(usuario_atual)
            elif not livre and (usuario_atual in lista_disp):
                lista_disp.remove(usuario_atual)

            st.session_state.escala_fixa[chave_d]["disponiveis"] = [p for p in lista_disp if p in EQUIPE]

        salvar_dados(st.session_state.escala_fixa)
        st.session_state.formulario_salvo = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ── FLUXO 3: CALENDÁRIO COM PAINEL DE EDIÇÃO MANUAL ─────────────────
else:
    usuario_atual = st.session_state.usuario_logado

    # ---- CONFIGURAÇÃO DA BARRA LATERAL ----
    st.sidebar.title("⚙️ Opções")
    st.sidebar.write(f"👤 Integrante: **{usuario_atual}**")

    if st.sidebar.button("🔄 Alterar meus dias livres", use_container_width=True):
        st.session_state.formulario_salvo = False
        st.rerun()

    if st.sidebar.button("🚪 Sair", use_container_width=True):
        st.session_state.usuario_logado = None
        st.session_state.formulario_salvo = False
        st.rerun()

    st.sidebar.markdown("---")

    # ---- PAINEL DE CONTROLE / EDITAR DIAS ----
    st.sidebar.subheader("🔒 Painel do Administrador")
    senha_inserida = st.sidebar.text_input("Digite a senha para liberar edições:", type="password")

    if senha_inserida == SENHA_ADMIN:
        st.sidebar.success("🔑 Modo de Edição Ativado!")
        st.sidebar.markdown("---")

        opcoes_adm = [d for d, _ in dias_filtrados]
        dia_adm = st.sidebar.selectbox(
            "Escolha o dia para Editar/Remover:",
            options=opcoes_adm,
            format_func=lambda x: f"Dia {x:02d} — Sábado 🍞" if x == DIA_SANTA_CEIA else f"Dia {x:02d} — Domingo"
        )

        ch_adm = str(dia_adm)
        dados_adm_dia = st.session_state.escala_fixa.get(ch_adm, {"disponiveis": [], "tipo": "", "forcado": []})
        valores_padrao_adm = dados_adm_dia.get("forcado", dados_adm_dia.get("disponiveis", []))
        valores_padrao_adm = [p for p in valores_padrao_adm if p in EQUIPE][:2]

        nova_equipe_manual = st.sidebar.multiselect(
            f"Defina quem VAI trabalhar no Dia {dia_adm:02d} (Máx 2):",
            options=EQUIPE,
            default=valores_padrao_adm,
            max_selections=2
        )

        if st.sidebar.button("🛑 Forçar/Editar este Dia Manualmente", use_container_width=True):
            tipo_dia = "Santa Ceia" if dia_adm == DIA_SANTA_CEIA else "Domingo"
            st.session_state.escala_fixa[ch_adm] = {
                "disponiveis": nova_equipe_manual,
                "forcado": nova_equipe_manual,
                "tipo": tipo_dia
            }
            salvar_dados(st.session_state.escala_fixa)
            st.sidebar.success(f"Dia {dia_adm} alterado com sucesso!")
            st.rerun()

        if st.sidebar.button("🗑️ Limpar Equipe do Dia (Deixar Vazio)", use_container_width=True):
            tipo_dia = "Santa Ceia" if dia_adm == DIA_SANTA_CEIA else "Domingo"
            st.session_state.escala_fixa[ch_adm] = {
                "disponiveis": [],
                "forcado": ["VAZIO"],
                "tipo": tipo_dia
            }
            salvar_dados(st.session_state.escala_fixa)
            st.sidebar.warning(f"Dia {dia_adm} limpo e esvaziado!")
            st.rerun()

        if st.sidebar.button("🔄 Resetar tudo para Sorteio Automático", use_container_width=True):
            if ch_adm in st.session_state.escala_fixa:
                st.session_state.escala_fixa[ch_adm]["forcado"] = []
            salvar_dados(st.session_state.escala_fixa)
            st.sidebar.info(f"Dia {dia_adm} devolvido ao sorteio inteligente!")
            st.rerun()
    else:
        if senha_inserida != "":
            st.sidebar.error("Senha Incorreta!")

    # ── PROCESSAMENTO DINÂMICO DA ESCALA COM REPETIÇÕES EVITADAS ──
    st.markdown(f'''
    <div class="custom-header">
        <p class="eyebrow">Equipe de Mídia · Instagram</p>
        <h1>Escala de <span>{MESES_PT[MES]}</span> {ANO}</h1>
        <p class="sub">📸 Calendário de Atividades Gerado automaticamente</p>
    </div>
    ''', unsafe_allow_html=True)

    escala_finalizada = {}
    historico_trabalho = {p: 0 for p in EQUIPE}
    ultima_dupla = set()

    for d, tipo in dias_filtrados:
        chave_d = str(d)
        dados_dia = st.session_state.escala_fixa.get(chave_d, {"disponiveis": [], "tipo": tipo, "forcado": []})
        forcado = dados_dia.get("forcado", [])
        disponiveis = dados_dia.get("disponiveis", [])

        if len(forcado) > 0:
            if forcado == ["VAZIO"]:
                escala_finalizada[d] = {"pessoas": [], "tipo": tipo}
            else:
                escala_finalizada[d] = {"pessoas": forcado.copy(), "tipo": tipo}
                for p in forcado:
                    if p in historico_trabalho:
                        historico_trabalho[p] += 1
                ultima_dupla = set(forcado)
            continue

        if not disponiveis:
            escala_finalizada[d] = {"pessoas": [], "tipo": tipo}
            continue

        if len(disponiveis) <= 2:
            escala_finalizada[d] = {"pessoas": disponiveis.copy(), "tipo": tipo}
            for p in disponiveis:
                historico_trabalho[p] += 1
            if len(disponiveis) == 2:
                ultima_dupla = set(disponiveis)
        else:
            random.seed(int(chave_d) + ANO + MES)

            combinacoes_validas = []
            for i in range(len(disponiveis)):
                for j in range(i + 1, len(disponiveis)):
                    combinacoes_validas.append([disponiveis[i], disponiveis[j]])

            combinacoes_filtradas = [c for c in combinacoes_validas if set(c) != ultima_dupla]
            lista_escolha = combinacoes_filtradas if combinacoes_filtradas else combinacoes_validas

            lista_escolha.sort(key=lambda c: (historico_trabalho[c[0]] + historico_trabalho[c[1]]))

            dupla_sorteada = lista_escolha[0]
            escala_finalizada[d] = {"pessoas": dupla_sorteada, "tipo": tipo}
            for p in dupla_sorteada:
                historico_trabalho[p] += 1
            ultima_dupla = set(dupla_sorteada)

    # ── RENDERIZAR CALENDÁRIO NA TELA ────────────────────────────────
    dias_html = ""
    for d, tipo in dias_filtrados:
        chave_d = str(d)
        is_manual = len(st.session_state.escala_fixa.get(chave_d, {}).get("forcado", [])) > 0

        if tipo == "Santa Ceia":
            classe_dia = "dia santa_ceia"
            cont_d = f'<span class="num">🗓️ Dia {d:02d} — Sábado (Santa Ceia)</span>'
        else:
            classe_dia = "dia domingo"
            cont_d = f'<span class="num">🗓️ Dia {d:02d} — Domingo</span>'

        if d in escala_finalizada and escala_finalizada[d]["pessoas"]:
            pessoas = escala_finalizada[d]["pessoas"]
            tag_manual = " <span style='font-size:10px; padding:2px 4px; background:#4c1d95; color:#c084fc; border-radius:4px;'>Fixado</span>" if is_manual else ""
            nomes = " &amp; ".join(pessoas) + tag_manual

            if tipo == "Santa Ceia":
                cor = CORES[3]
                cont_d += f'<div class="badge" style="background:{cor["bg"]};border-color:{cor["border"]};color:{cor["text"]}"><span class="badge-nome">✨ {nomes}</span><span class="badge-tarefas">🍞🍷 Culto de Santa Ceia</span></div>'
            else:
                cor = CORES[d % 4]
                cont_d += f'<div class="badge" style="background:{cor["bg"]};border-color:{cor["border"]};color:{cor["text"]}"><span class="badge-nome">👥 {nomes}</span><span class="badge-tarefas">📸 Foto &amp; Stories</span></div>'
            classe_dia += " tem-escala"
        else:
            cont_d += '<span style="color:#444; font-size:.75rem; font-style:italic;">Ninguém escalado neste dia</span>'

        dias_html += f'<div class="{classe_dia}">{cont_d}</div>'

    st.markdown(f'''
    <div class="cal-wrap">
        <div class="cal-grid">
            {dias_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Resumo embaixo por integrante
    st.markdown('<p class="resumo-titulo">Resumo de Atividades por Integrante (Contagem Justa)</p>', unsafe_allow_html=True)
    cols = st.columns(len(EQUIPE))

    for i in range(len(EQUIPE)):
        pessoa = EQUIPE[i]
        with cols[i]:
            cor = CORES[i % 4]
            itens = ""
            for d_orig, tipo_orig in dias_filtrados:
                if d_orig in escala_finalizada:
                    dados_ch = escala_finalizada[d_orig]
                    if p in dados_ch["pessoas"]:  # Consertado escopo da checagem
                        if pessoa in dados_ch["pessoas"]:
                            parceiros = [p for p in dados_ch["pessoas"] if p != pessoa]
                            parceiros_nome = ", ".join(parceiros) if parceiros else "Sozinha"

                            if d_orig == DIA_SANTA_CEIA:
                                itens += f'<li>🍷 Dia <strong>{d_orig}</strong> (Santa Ceia) <br><span class="parceiro">🤝 Juntas: {parceiros_nome}</span></li>'
                            else:
                                itens += f'<li>🌅 Dia <strong>{d_orig}</strong> (Domingo) <br><span class="parceiro">🤝 c/ {parceiros_nome}</span></li>'

            st.markdown(f'''
            <div class="pessoa-card" style="border-left: 4px solid {cor["border"]};">
                <div class="pessoa-nome" style="color:{cor["border"]}">{pessoa} ({historico_trabalho[pessoa]} Cultos)</div>
                <ul class="pessoa-lista">{itens if itens else "<li>Nenhum dia alocado</li>"}</ul>
            </div>
            ''', unsafe_allow_html=True)