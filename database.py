import sqlite3
import pandas as pd
from datetime import datetime

# =========================
# CONEXÃO
# =========================
def conectar():
    return sqlite3.connect("dados.db")


# =========================
# TABELA PRINCIPAL (DESCONTOS)
# =========================
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS descontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            DISTRIBUIDORA TEXT,
            FECHAMENTO TEXT,
            NF TEXT,
            DATA_EMISSAO TEXT,
            CIDADE TEXT,
            BASE TEXT,
            VALOR_DESCONTO REAL,
            OBSERVACAO TEXT,
            MOTIVO TEXT
        )
    """)

    conn.commit()
    conn.close()


def inserir_dados(df):
    conn = conectar()
    df.to_sql("descontos", conn, if_exists="append", index=False)
    conn.close()


def carregar_dados():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM descontos", conn)
    conn.close()
    return df


def limpar_dados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM descontos")
    conn.commit()
    conn.close()


# =========================
# HISTÓRICO DE UPLOADS
# =========================
def criar_tabela_uploads():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT,
            data_upload TEXT
        )
    """)

    conn.commit()
    conn.close()


def registrar_upload(nome_arquivo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO uploads (nome_arquivo, data_upload)
        VALUES (?, ?)
    """, (nome_arquivo, datetime.now().strftime("%d/%m/%Y %H:%M")))

    conn.commit()
    conn.close()


def carregar_uploads():
    conn = conectar()
    df = pd.read_sql(
        "SELECT nome_arquivo, data_upload FROM uploads ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


# =========================
# OCORRÊNCIAS
# =========================
def criar_tabela_ocorrencias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distribuidora TEXT,
            pedido TEXT,
            nota_fiscal TEXT,
            emissao_nf TEXT,
            valor_nf REAL,
            valor_ocorrencia REAL,
            cidade_nf TEXT,
            filial TEXT,
            ocorrencia TEXT,
            vol_total_nf INTEGER,
            volume_ocorrencia INTEGER,
            status_atual TEXT,
            data_ultimo_status TEXT,
            follow_up TEXT,
            status_rpg TEXT
        )
    """)

    conn.commit()
    conn.close()


def inserir_ocorrencia(
    distribuidora,
    pedido,
    nota_fiscal,
    emissao_nf,
    valor_nf,
    cidade_nf,
    filial,
    ocorrencia,
    vol_total_nf,
    volume_ocorrencia,
    status_atual,
    data_ultimo_status,
    follow_up,
    status_rpg,
    valor_ocorrencia
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ocorrencias (
            distribuidora,
            pedido,
            nota_fiscal,
            emissao_nf,
            valor_nf,
            valor_ocorrencia,
            cidade_nf,
            filial,
            ocorrencia,
            vol_total_nf,
            volume_ocorrencia,
            status_atual,
            data_ultimo_status,
            follow_up,
            status_rpg
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        distribuidora,
        pedido,
        nota_fiscal,
        emissao_nf,
        valor_nf,
        valor_ocorrencia,
        cidade_nf,
        filial,
        ocorrencia,
        vol_total_nf,
        volume_ocorrencia,
        status_atual,
        data_ultimo_status,
        follow_up,
        status_rpg
    ))

    conn.commit()
    conn.close()


def carregar_ocorrencias():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM ocorrencias ORDER BY id DESC", conn)
    conn.close()
    return df


def deletar_ocorrencia(id_ocorrencia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM ocorrencias WHERE id = ?",
        (id_ocorrencia,)
    )

    conn.commit()
    conn.close()


def atualizar_ocorrencia(
    id_ocorrencia,
    distribuidora,
    pedido,
    nota_fiscal,
    emissao_nf,
    valor_nf,
    cidade_nf,
    filial,
    ocorrencia,
    vol_total_nf,
    volume_ocorrencia,
    status_atual,
    data_ultimo_status,
    follow_up,
    status_rpg,
    valor_ocorrencia
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ocorrencias SET
            distribuidora = ?,
            pedido = ?,
            nota_fiscal = ?,
            emissao_nf = ?,
            valor_nf = ?,
            valor_ocorrencia = ?,
            cidade_nf = ?,
            filial = ?,
            ocorrencia = ?,
            vol_total_nf = ?,
            volume_ocorrencia = ?,
            status_atual = ?,
            data_ultimo_status = ?,
            follow_up = ?,
            status_rpg = ?
        WHERE id = ?
    """, (
        distribuidora,
        pedido,
        nota_fiscal,
        emissao_nf,
        valor_nf,
        valor_ocorrencia,
        cidade_nf,
        filial,
        ocorrencia,
        vol_total_nf,
        volume_ocorrencia,
        status_atual,
        data_ultimo_status,
        follow_up,
        status_rpg,
        id_ocorrencia
    ))

    conn.commit()
    conn.close()


def criar_tabela_pendencias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pendencias_comprovante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            motorista TEXT,
            distribuidora TEXT,
            nota_fiscal TEXT,
            emissao TEXT,
            saida TEXT,
            manifesto TEXT,
            obs TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def inserir_pendencia(motorista, distribuidora, nota_fiscal, emissao, saida, manifesto, obs, status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pendencias_comprovante (
            motorista, distribuidora, nota_fiscal, emissao, saida, manifesto, obs, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (motorista, distribuidora, nota_fiscal, emissao, saida, manifesto, obs, status))

    conn.commit()
    conn.close()


def carregar_pendencias():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM pendencias_comprovante", conn)
    conn.close()
    return df


def atualizar_pendencia(id_pendencia, motorista, distribuidora, nota_fiscal, emissao, saida, manifesto, obs, status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pendencias_comprovante
        SET motorista=?, distribuidora=?, nota_fiscal=?, emissao=?, saida=?, manifesto=?, obs=?, status=?
        WHERE id=?
    """, (motorista, distribuidora, nota_fiscal, emissao, saida, manifesto, obs, status, id_pendencia))

    conn.commit()
    conn.close()


def deletar_pendencia(id_pendencia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pendencias_comprovante WHERE id=?", (id_pendencia,))

    conn.commit()
    conn.close()

# Alias para manter compatibilidade com o app.py
listar_ocorrencias = carregar_ocorrencias


