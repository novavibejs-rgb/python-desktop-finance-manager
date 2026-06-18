import sqlite3
from datetime import datetime, timedelta


def conectar():
    return sqlite3.connect("financeiro.db")


# ==================== TABELAS ====================

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS socios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        servico TEXT NOT NULL,
        descricao TEXT,
        valor REAL NOT NULL,
        forma_pagamento TEXT,
        data TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_socio TEXT NOT NULL,
        valor REAL NOT NULL,
        descricao TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()


# ==================== SÓCIOS ====================

def cadastrar_socio(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO socios (nome)
    VALUES (?)
    """, (nome,))

    conn.commit()
    conn.close()


def listar_socios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM socios
    """)

    socios = cursor.fetchall()

    conn.close()

    return socios


def atualizar_socio(id_socio, novo_nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE socios
    SET nome = ?
    WHERE id = ?
    """, (novo_nome, id_socio))

    conn.commit()
    conn.close()


def excluir_socio(id_socio):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM socios
    WHERE id = ?
    """, (id_socio,))

    conn.commit()
    conn.close()


# ==================== SERVIÇOS ====================

def adicionar_servico(nome_cliente, servico, descricao, valor, forma_pagamento):
    conn = conectar()
    cursor = conn.cursor()

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO servicos
    (cliente, servico, descricao, valor, forma_pagamento, data)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nome_cliente,
        servico,
        descricao,
        valor,
        forma_pagamento,
        data
    ))

    conn.commit()
    conn.close()


def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM servicos
    """)

    servicos = cursor.fetchall()

    conn.close()

    return servicos


def buscar_servico_por_id(id_servico):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM servicos
    WHERE id = ?
    """, (id_servico,))

    servico = cursor.fetchone()

    conn.close()

    return servico


def excluir_servico(id_servico):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM servicos
    WHERE id = ?
    """, (id_servico,))

    conn.commit()
    conn.close()


# ==================== FATURAMENTO ====================

def faturamento_por_mes(mes_ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(valor)
    FROM servicos
    WHERE data LIKE ?
    """, (f"%{mes_ano}%",))

    total = cursor.fetchone()[0]

    conn.close()

    return total if total is not None else 0


def faturamento_semana():
    conn = conectar()
    cursor = conn.cursor()

    hoje = datetime.now()

    # segunda-feira da semana atual
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    inicio_semana = inicio_semana.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    cursor.execute("""
        SELECT SUM(valor)
        FROM servicos
        WHERE data >= ?
    """, (inicio_semana.strftime("%Y-%m-%d %H:%M:%S"),))

    total = cursor.fetchone()[0]

    conn.close()

    return total if total is not None else 0

def calcular_faturamento_total():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(valor)
    FROM servicos
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total if total is not None else 0


# ==================== VALES ====================

def adicionar_vale(nome_socio, valor, descricao):
    conn = conectar()
    cursor = conn.cursor()

    data = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")

    cursor.execute("""
    INSERT INTO vales
    (nome_socio, valor, descricao, data)
    VALUES (?, ?, ?, ?)
    """, (nome_socio, valor, descricao, data))

    conn.commit()
    conn.close()


def listar_vales():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM vales
    """)

    vales = cursor.fetchall()

    conn.close()

    return vales


def buscar_vale_por_id(id_vale):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM vales
    WHERE id = ?
    """, (id_vale,))

    vale = cursor.fetchone()

    conn.close()

    return vale


def atualizar_vale(id_vale, nome_socio, valor, descricao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE vales
    SET nome_socio = ?,
        valor = ?,
        descricao = ?
    WHERE id = ?
    """, (nome_socio, valor, descricao, id_vale))

    conn.commit()
    conn.close()


def excluir_vale(id_vale):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM vales
    WHERE id = ?
    """, (id_vale,))

    conn.commit()
    conn.close()


def calcular_total_vales():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(valor)
    FROM vales
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total if total is not None else 0