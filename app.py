import streamlit as st
from google import genai
import PyPDF2
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import io
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="AutoMail.ai - Inteligência Financeira", page_icon="📧", layout="wide")

# 2. CSS CUSTOMIZADO
st.markdown("""
    <style>
    .status-card {
        padding: 25px; border-radius: 15px; 
        background-color: rgba(79, 70, 229, 0.05); 
        border: 1px solid rgba(79, 70, 229, 0.2);
        border-left: 5px solid #4F46E5;
        margin-bottom: 25px;
        color: inherit;
    }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.8em;
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white; font-weight: bold; border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BACKEND 
API_KEY = "AIzaSyBjxTaWPICs8KLnPNLdgzZ2hUiQCImv3-s"
client = genai.Client(api_key=API_KEY)

def realizar_triagem_avancada(conteudo):
    #CAPTURA DE HORARIO
    # Captura o horário atual para a saudação inteligente
    hora_atual = datetime.now().hour
    if hora_atual < 12:
        saudacao_padrao = "Bom dia"
    elif hora_atual < 18:
        saudacao_padrao = "Boa tarde"
    else:
        saudacao_padrao = "Boa noite"

    # Prompt para catogrização e resposta profissional, com regras claras para evitar formatações indesejadas. O modelo deve seguir estritamente as instruções para garantir a consistência dos dados extraídos.
    prompt = f"""
    Atue como Assistente de Operações Financeiras Sênior responsável por triagem de e-mails corporativos.

    TAREFA:
    1. Classificar o e-mail (Produtivo ou Improdutivo).
    2. Gerar uma resposta corporativa curta e pronta para envio.

    REGRAS DE CLASSIFICAÇÃO:
    CATEGORIA: Produtivo ou Improdutivo
    PRIORIDADE: Alta, Média ou Baixa
    ASSUNTO: até 3 palavras

    REGRAS DE RESPOSTA:
    - Tom corporativo, objetivo e educado.
    - Máximo 5 linhas de corpo de texto.
    - Iniciar com: {saudacao_padrao}.
    - Finalizar com: Atenciosamente, Equipe do Financeiro.
    - PROIBIDO usar asteriscos (**) ou negritos no corpo da resposta.

    ESTRUTURA DO CAMPO 'RESPOSTA' (Layout Obrigatório):
    STATUS: [Categoria]
    RESUMO: [Resumo do e-mail em 1 ou 2 linhas]
    ---
    {saudacao_padrao},

    [Corpo da resposta aqui]

    Atenciosamente, 
    Equipe do Financeiro

    FORMATO DE SAÍDA PARA O SISTEMA (Rigoroso):
    CATEGORIA: [Aqui]
    PRIORIDADE: [Aqui]
    ASSUNTO: [Aqui]
    RESPOSTA: [Coloque aqui o Status, Resumo, a linha divisória '---' e o e-mail redigido]

    EMAIL RECEBIDO:
    "{conteudo}"
    """
    for tentativa in range(3):
        try:
            response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
            return response.text
        except:
            time.sleep(2)
            continue
    return "Erro na conexão."

# 4. ESTADO DA SESSÃO
if 'historico_full' not in st.session_state:
    st.session_state.historico_full = []
if 'resultado_exibido' not in st.session_state:
    st.session_state.resultado_exibido = None

# 5. INTERFACE PRINCIPAL
st.markdown("<h1>📧 AutoMail<span style='color:#4F46E5'>.ai</span></h1>", unsafe_allow_html=True)
st.markdown("---")

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.subheader("📥 Entrada de E-mails")
    uploaded_file = st.file_uploader("📂 Carregar Documento (PDF/TXT)", type=["pdf", "txt"])
    
    corpo_email = ""
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            corpo_email = "".join([page.extract_text() for page in pdf_reader.pages])
        else:
            corpo_email = str(uploaded_file.read(), "utf-8")
    
    texto_input = st.text_area("Conteúdo para análise:", value=corpo_email, height=200)
    
    if st.button("🚀 EXECUTAR TRIAGEM"):
        if texto_input:
            with st.spinner("IA Analisando..."):
                res = realizar_triagem_avancada(texto_input)
                st.session_state.resultado_exibido = res
                try:
                    # Limpeza de caracteres especiais e espaços
                    cat = res.split("CATEGORIA:")[1].split("\n")[0].strip().replace("*", "")
                    prio = res.split("PRIORIDADE:")[1].split("\n")[0].strip().replace("*", "")
                    assunto = res.split("ASSUNTO:")[1].split("\n")[0].strip().replace("*", "")
                    
                    # Garantia de padronização
                    cat = "Produtivo" if "Produtivo" in cat else "Improdutivo"
                except:
                    cat, prio, assunto = "Improdutivo", "Média", "Triagem Geral"
                
                st.session_state.historico_full.append({
                    "Data/Hora": datetime.now(),
                    "Categoria": cat,
                    "Prioridade": prio,
                    "Assunto": assunto
                })
                st.rerun()

with col_out:
    st.subheader("🚀 Resposta Sugerida")
    if st.session_state.resultado_exibido:
        try:
            texto_bruto = st.session_state.resultado_exibido
            
            conteudo = texto_bruto.split("RESPOSTA:")[1].strip() if "RESPOSTA:" in texto_bruto else texto_bruto.strip()
            
            if "---" in conteudo:
                partes = conteudo.split("---")
                area_analise = partes[0].strip()
                area_email = partes[1].strip()
            else:
                import re
                divisor = re.search(r'(Bom dia|Boa tarde|Boa noite|Olá)', conteudo)
                if divisor:
                    idx = divisor.start()
                    area_analise = conteudo[:idx].strip()
                    area_email = conteudo[idx:].strip()
                else:
                    area_analise = "STATUS: Produtivo\nRESUMO: Documento processado com sucesso."
                    area_email = conteudo

            cor_status = "#22c55e" if "Produtivo" in area_analise else "#ef4444"
            area_analise = area_analise.replace("STATUS:", "<b>STATUS:</b>").replace("RESUMO:", "<br><br><b>RESUMO:</b>")
            area_analise = area_analise.replace("Produtivo", f'<span style="color:{cor_status}">Produtivo</span>')
            area_analise = area_analise.replace("Improdutivo", f'<span style="color:{cor_status}">Improdutivo</span>')

            # Bloco 1: Análise (Fundo adaptável)
            st.markdown(f"""
                <div style="border-left: 5px solid #D1D5DB; background-color: rgba(150, 150, 150, 0.1); padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                    {area_analise}
                </div>
            """, unsafe_allow_html=True)

            # Bloco 2: Resposta (Fundo adaptável com tom roxo)
            email_html = area_email.replace("\n", "<br>")
            st.markdown(f"""
                <div style="border-left: 5px solid #4F46E5; background-color: rgba(79, 70, 229, 0.1); padding: 20px; border-radius: 5px; text-align: justify;">
                    {email_html}
                </div>
            """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Erro na formatação: {e}")

# --- 6. ANÁLISE DA SESSÃO ---
if len(st.session_state.historico_full) > 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("Análise da Sessão") # Emoji 🥧 removido aqui
    
    df_real = pd.DataFrame(st.session_state.historico_full)
    total_emails = len(df_real)

    # Bloco de Progressão (Eixo X: 0, 1, 2...)
    with st.container(border=True):
        st.markdown("#### 📈 Progressão de Atendimentos")
        eixo_x = list(range(total_emails + 1))
        eixo_y = list(range(total_emails + 1))
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=eixo_x, y=eixo_y, mode='lines+markers', 
                                     line=dict(color='#4F46E5', width=4, shape='hv'),
                                     fill='tozeroy', fillcolor='rgba(79, 70, 229, 0.1)'))
        fig_line.update_layout(height=250, margin=dict(l=20, r=20, t=10, b=10),
                              xaxis=dict(title="Eventos", dtick=1), 
                              yaxis=dict(title="Total", dtick=1),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)

    # Métricas Lado a Lado
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.markdown("<p style='text-align:center; font-weight:bold;'>Taxa de Produtividade</p>", unsafe_allow_html=True)
            prod_count = len(df_real[df_real['Categoria'] == 'Produtivo'])
            percent = int((prod_count/total_emails)*100)
            fig_donut = go.Figure(data=[go.Pie(labels=['Produtivos', 'Outros'], values=[prod_count, total_emails-prod_count], 
                                              hole=.75, marker_colors=['#10b981', '#334155'], textinfo='none')])
            fig_donut.update_layout(showlegend=False, height=180, margin=dict(l=0, r=0, t=0, b=0),
                                   annotations=[dict(text=f'{percent}%', x=0.5, y=0.5, font_size=24, font_color='#10b981', showarrow=False)])
            st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        with st.container(border=True):
            st.markdown("<p style='text-align:center; font-weight:bold;'>📊 Prioridade</p>", unsafe_allow_html=True)
            p_counts = df_real['Prioridade'].value_counts().reindex(['Alta', 'Média', 'Baixa'], fill_value=0)
            fig_prio = go.Figure(go.Bar(x=p_counts.values, y=p_counts.index, orientation='h', 
                                       marker_color=['#991b1b', '#d97706', '#0284c7'], width=0.6))
            fig_prio.update_layout(height=180, margin=dict(l=10, r=10, t=0, b=0),
                                  xaxis=dict(dtick=1), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_prio, use_container_width=True)

    with c3:
        with st.container(border=True):
            st.markdown("<p style='text-align:center; font-weight:bold;'>🏷️ Top Assuntos</p>", unsafe_allow_html=True)
            tag_counts = df_real['Assunto'].value_counts().head(3)
            for tag, count in tag_counts.items():
                st.markdown(f"<div style='background:rgba(79, 70, 229, 0.08); padding:8px; border-radius:8px; margin-bottom:8px; display:flex; justify-content:space-between; border: 1px solid rgba(79, 70, 229, 0.15);'><span style='font-size:0.85em; font-weight:bold;'>{tag}</span><span style='background:#4F46E5; padding:2px 8px; border-radius:10px; color:white; font-size:0.75em;'>{count}</span></div>", unsafe_allow_html=True)

    # Relatório Detalhado e Download
    st.markdown("#### 📜 Relatório Detalhado")
    df_exibir = df_real.copy()
    df_exibir['Data/Hora'] = df_exibir['Data/Hora'].dt.strftime('%H:%M:%S')
    st.dataframe(df_exibir, use_container_width=True, hide_index=True)
    
    csv = df_exibir.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(label="📥 Baixar Planilha para Excel", data=csv, file_name="automail_gestao.csv", mime="text/csv")

st.markdown("---")
st.caption(f"Desenvolvido por Claudio Paulino Arruda | Mato Grosso - {datetime.now().year}")