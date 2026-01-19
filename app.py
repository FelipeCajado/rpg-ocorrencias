import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

from ai_assistant import responder_pergunta
from database import (
    criar_tabela,
    criar_tabela_uploads,
    criar_tabela_ocorrencias,
    inserir_ocorrencia,
    atualizar_ocorrencia,
    deletar_ocorrencia,
    carregar_ocorrencias,
    limpar_dados,
    inserir_dados,
    carregar_dados,
    registrar_upload,
    criar_tabela_pendencias,
    inserir_pendencia,
    carregar_pendencias,
    atualizar_pendencia,
    deletar_pendencia
)

# ---------- INIT ----------
st.set_page_config(
    page_title="RPG | Gestão de Ocorrências e Descontos",
    layout="wide"
)

criar_tabela()
criar_tabela_uploads()
criar_tabela_ocorrencias()
criar_tabela_pendencias()

st.title("📦 RPG | Sistema de Gestão de Ocorrências")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "🏠 Início",
        "📤 Upload de Planilhas",
        "📝 Cadastro de Ocorrências",
        "📊 Relatórios",
        "🤖 IA - Perguntas",
        "📄 Pendências de Comprovante"
    ]
)

# ---------- CIDADES X FILIAIS ----------
@st.cache_data
def carregar_cidades_filiais():
    return pd.read_excel("CIDADES X FILIAIS.xlsx")

df_cidades = carregar_cidades_filiais()

def buscar_filial_por_cidade(cidade):
    if not cidade:
        return ""
    cidade = cidade.strip().upper()
    df = df_cidades.copy()
    df["CIDADE"] = df["CIDADE"].astype(str).str.strip().str.upper()
    resultado = df.loc[df["CIDADE"] == cidade, "FILIAL"]
    return resultado.iloc[0] if not resultado.empty else ""

# ---------------- INÍCIO ----------------
if menu == "🏠 Início":
    st.subheader("Bem-vindo")
    st.write("Sistema de análise de descontos e ocorrências.")

# ---------------- UPLOAD ----------------
elif menu == "📤 Upload de Planilhas":
    st.subheader("📤 Upload de Planilhas")

    if st.button("🗑 Limpar dados atuais"):
        limpar_dados()
        st.success("Dados removidos!")

    uploaded_file = st.file_uploader("Selecione a planilha", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        inserir_dados(df)
        registrar_upload(uploaded_file.name)
        st.success("Planilha carregada com sucesso!")
        st.dataframe(df, use_container_width=True)

# ---------------- RELATÓRIOS ----------------
elif menu == "📊 Relatórios":
    st.subheader("📊 Relatórios")
    dados = carregar_dados()

    if dados.empty:
        st.warning("Nenhum dado encontrado.")
    else:
        st.dataframe(dados, use_container_width=True)

# ---------------- IA ----------------
elif menu == "🤖 IA - Perguntas":
    st.subheader("🤖 Perguntas inteligentes")
    dados = carregar_dados()

    pergunta = st.text_input("Digite sua pergunta")

    if pergunta:
        resultado, titulo = responder_pergunta(pergunta, dados)
        st.write(titulo)
        if resultado is not None:
            st.dataframe(resultado, use_container_width=True)

# ---------- CADASTRO DE OCORRÊNCIAS ----------
elif menu == "📝 Cadastro de Ocorrências":

    # ---------- NOVA OCORRÊNCIA ----------
    st.subheader("➕ Nova Ocorrência")

    with st.form("nova_ocorrencia"):
        distribuidora = st.text_input("Distribuidora")
        pedido = st.text_input("Pedido")
        nota_fiscal = st.text_input("Nota Fiscal")
        emissao_nf = st.date_input("📅 Data de Emissão da NF", value=date.today())

        cidade_nf = st.text_input("Cidade da NF")
        filial = buscar_filial_por_cidade(cidade_nf)
        st.text_input("Filial (automática)", filial, disabled=True)

        ocorrencia = st.selectbox("Ocorrência", ["EXTRAVIO", "AVARIA", "SINISTRO"])
        vol_total_nf = st.number_input("Volume Total", min_value=0)
        volume_ocorrencia = st.number_input("Volume Ocorrência", min_value=0)

        valor_nf = st.number_input("💰 Valor da NF", min_value=0.0)
        valor_ocorrencia = st.number_input("💰 Valor da Ocorrência", min_value=0.0)

        status_atual = st.text_input("Status Atual")
        follow_up = st.text_area("Follow Up")
        status_rpg = st.text_input("Status RPG")

        salvar = st.form_submit_button("💾 Cadastrar")

        if salvar:
            inserir_ocorrencia(
                distribuidora,
                pedido,
                nota_fiscal,
                emissao_nf.strftime("%Y-%m-%d"),
                valor_nf,
                cidade_nf,
                filial,
                ocorrencia,
                vol_total_nf,
                volume_ocorrencia,
                status_atual,
                date.today().isoformat(),
                follow_up,
                status_rpg,
                valor_ocorrencia
            )
            st.success("Ocorrência cadastrada com sucesso!")
            st.rerun()

    # ---------- TABELA + FILTROS ----------
    st.divider()
    st.subheader("📊 Tabela Consolidada de Ocorrências")

    df = carregar_ocorrencias()

    if df.empty:
        st.info("Nenhuma ocorrência cadastrada.")
        st.stop()

    df["emissao_nf"] = pd.to_datetime(df["emissao_nf"], errors="coerce")

    st.markdown("### 🔎 Filtros")
    col1, col2, col3 = st.columns(3)

    with col1:
        f_distribuidora = st.multiselect("Distribuidora", sorted(df["distribuidora"].dropna().unique()))
        f_pedido = st.multiselect("Pedido", sorted(df["pedido"].dropna().unique()))
        f_nf = st.multiselect("Nota Fiscal", sorted(df["nota_fiscal"].dropna().unique()))

    with col2:
        f_cidade = st.multiselect("Cidade da NF", sorted(df["cidade_nf"].dropna().unique()))
        f_filial = st.multiselect("Filial", sorted(df["filial"].dropna().unique()))
        f_ocorrencia = st.multiselect("Ocorrência", sorted(df["ocorrencia"].dropna().unique()))

    with col3:
        f_status = st.multiselect("Status Atual", sorted(df["status_atual"].dropna().unique()))
        f_follow = st.multiselect("Follow Up", sorted(df["follow_up"].dropna().unique()))
        f_rpg = st.multiselect("Status RPG", sorted(df["status_rpg"].dropna().unique()))

    if f_distribuidora: df = df[df["distribuidora"].isin(f_distribuidora)]
    if f_pedido: df = df[df["pedido"].isin(f_pedido)]
    if f_nf: df = df[df["nota_fiscal"].isin(f_nf)]
    if f_cidade: df = df[df["cidade_nf"].isin(f_cidade)]
    if f_filial: df = df[df["filial"].isin(f_filial)]
    if f_ocorrencia: df = df[df["ocorrencia"].isin(f_ocorrencia)]
    if f_status: df = df[df["status_atual"].isin(f_status)]
    if f_follow: df = df[df["follow_up"].isin(f_follow)]
    if f_rpg: df = df[df["status_rpg"].isin(f_rpg)]

    st.dataframe(df, use_container_width=True)

    # ---------- EXPORTAÇÃO ----------
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    st.download_button(
        "📥 Exportar Ocorrências para Excel",
        data=output,
        file_name="ocorrencias_rpg.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ---------- EDIÇÃO ESPELHADA ----------
    st.divider()
    st.subheader("✏️ Editar / 🗑 Apagar Ocorrências")

    for _, row in df.iterrows():
        with st.expander(f"📄 NF {row['nota_fiscal']} | {row['distribuidora']}"):
            with st.form(f"edit_{row['id']}"):

                distribuidora = st.text_input("Distribuidora", row["distribuidora"])
                pedido = st.text_input("Pedido", row["pedido"])
                nota_fiscal = st.text_input("Nota Fiscal", row["nota_fiscal"])
                emissao_nf = st.date_input("Emissão NF", row["emissao_nf"].date())

                cidade_nf = st.text_input("Cidade NF", row["cidade_nf"])
                filial = st.text_input("Filial", row["filial"])

                ocorrencia = st.text_input("Ocorrência", row["ocorrencia"])
                vol_total_nf = st.number_input("Volume Total", value=int(row["vol_total_nf"]))
                volume_ocorrencia = st.number_input("Volume Ocorrência", value=int(row["volume_ocorrencia"]))

                valor_nf = st.number_input("Valor NF", value=float(row["valor_nf"]))
                valor_ocorrencia = st.number_input("Valor Ocorrência", value=float(row["valor_ocorrencia"]))

                status_atual = st.text_input("Status Atual", row["status_atual"])
                follow_up = st.text_area("Follow Up", row["follow_up"])
                status_rpg = st.text_input("Status RPG", row["status_rpg"])

                salvar = st.form_submit_button("💾 Salvar Alterações")

                if salvar:
                    atualizar_ocorrencia(
                        row["id"],
                        distribuidora,
                        pedido,
                        nota_fiscal,
                        emissao_nf.strftime("%Y-%m-%d"),
                        valor_nf,
                        cidade_nf,
                        filial,
                        ocorrencia,
                        vol_total_nf,
                        volume_ocorrencia,
                        status_atual,
                        date.today().isoformat(),
                        follow_up,
                        status_rpg,
                        valor_ocorrencia
                    )
                    st.success("Ocorrência atualizada!")
                    st.rerun()

            if st.button("🗑 Excluir", key=f"del_{row['id']}"):
                deletar_ocorrencia(row["id"])
                st.success("Ocorrência excluída!")
                st.rerun()

#---------- Pendências_de_comprovante --------

elif menu == "📄 Pendências de Comprovante":

    st.subheader("➕ Nova Pendência de Comprovante")

    with st.form("nova_pendencia"):
        motorista = st.text_input("Motorista")
        distribuidora = st.text_input("Distribuidora")
        nota_fiscal = st.text_input("Nota Fiscal")

        emissao = st.date_input("📅 Emissão")
        saida = st.date_input("🚚 Saída")

        manifesto = st.text_input("Manifesto")
        obs = st.text_area("Observações")
        status = st.selectbox("Status", ["PENDENTE", "ENVIADO", "REGULARIZADO"])

        salvar = st.form_submit_button("💾 Cadastrar")

        if salvar:
            inserir_pendencia(
                motorista,
                distribuidora,
                nota_fiscal,
                emissao.strftime("%Y-%m-%d"),
                saida.strftime("%Y-%m-%d"),
                manifesto,
                obs,
                status
            )
            st.success("Pendência cadastrada com sucesso!")
            st.rerun()

    st.divider()
    st.subheader("📊 Pendências de Comprovante")

    df = carregar_pendencias()

    if df.empty:
        st.info("Nenhuma pendência cadastrada.")
        st.stop()

    df["emissao"] = pd.to_datetime(df["emissao"], errors="coerce")
    df["saida"] = pd.to_datetime(df["saida"], errors="coerce")

    st.markdown("### 🔎 Filtros")

    col1, col2, col3 = st.columns(3)

    with col1:
        f_motorista = st.multiselect("Motorista", sorted(df["motorista"].dropna().unique()))
        f_dist = st.multiselect("Distribuidora", sorted(df["distribuidora"].dropna().unique()))

    with col2:
        f_nf = st.multiselect("Nota Fiscal", sorted(df["nota_fiscal"].dropna().unique()))
        f_manifesto = st.multiselect("Manifesto", sorted(df["manifesto"].dropna().unique()))

    with col3:
        f_status = st.multiselect("Status", sorted(df["status"].dropna().unique()))

    if f_motorista:
        df = df[df["motorista"].isin(f_motorista)]
    if f_dist:
        df = df[df["distribuidora"].isin(f_dist)]
    if f_nf:
        df = df[df["nota_fiscal"].isin(f_nf)]
    if f_manifesto:
        df = df[df["manifesto"].isin(f_manifesto)]
    if f_status:
        df = df[df["status"].isin(f_status)]

    st.dataframe(df, use_container_width=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Pendencias")
    output.seek(0)

    st.download_button(
        "📥 Exportar Pendências",
        data=output,
        file_name="pendencias_comprovante.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()
    st.subheader("✏️ Editar / 🗑 Excluir Pendências")

    for _, row in df.iterrows():
        with st.expander(f"📄 NF {row['nota_fiscal']} | {row['motorista']}"):
            with st.form(f"edit_pend_{row['id']}"):
                obs = st.text_area("Observações", row["obs"])
                status = st.selectbox(
                    "Status",
                    ["PENDENTE", "ENVIADO", "REGULARIZADO"],
                    index=["PENDENTE", "ENVIADO", "REGULARIZADO"].index(row["status"])
                )

                salvar = st.form_submit_button("💾 Atualizar")

                if salvar:
                    atualizar_pendencia(
                        row["id"],
                        row["motorista"],
                        row["distribuidora"],
                        row["nota_fiscal"],
                        row["emissao"].strftime("%Y-%m-%d"),
                        row["saida"].strftime("%Y-%m-%d"),
                        row["manifesto"],
                        obs,
                        status
                    )
                    st.success("Pendência atualizada!")
                    st.rerun()

            if st.button("🗑 Excluir", key=f"del_pend_{row['id']}"):
                deletar_pendencia(row["id"])
                st.success("Pendência excluída!")
                st.rerun()

