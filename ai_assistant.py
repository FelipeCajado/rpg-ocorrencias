def responder_pergunta(pergunta, dados):
    pergunta = pergunta.lower()

    if "base" in pergunta:
        resultado = (
            dados.groupby("BASE")["VALOR_DESCONTO"]
            .sum()
            .reset_index()
            .sort_values("VALOR_DESCONTO", ascending=False)
        )
        return resultado, "📌 Total de desconto por Base"

    elif "cidade" in pergunta:
        resultado = (
            dados.groupby("CIDADE")["VALOR_DESCONTO"]
            .sum()
            .reset_index()
            .sort_values("VALOR_DESCONTO", ascending=False)
        )
        return resultado, "📌 Total de desconto por Cidade"

    elif "distribuidora" in pergunta:
        resultado = (
            dados.groupby("DISTRIBUIDORA")["VALOR_DESCONTO"]
            .sum()
            .reset_index()
            .sort_values("VALOR_DESCONTO", ascending=False)
        )
        return resultado, "📌 Total de desconto por Distribuidora"

    elif "avaria" in pergunta or "extravio" in pergunta:
        resultado = (
            dados.groupby("OBSERVACAO")["VALOR_DESCONTO"]
            .sum()
            .reset_index()
        )
        return resultado, "📌 Descontos por Tipo (Avaria / Extravio)"

    else:
        return None, "❌ Não entendi a pergunta. Tente: base, cidade, distribuidora, avaria."
