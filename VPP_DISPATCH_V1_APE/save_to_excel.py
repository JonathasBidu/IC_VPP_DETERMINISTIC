import pandas as pd

def save_simulation_to_excel(
    data,
    lucro,
    energia_gerada,
    energia_demandada,
    res,
    cap_pv,
    cap_wt,
    cap_load,
    delta,
    season,
    Nt,
    idx,
    ga_params=None,
    output_path="resultado_simulacao_cenario_1_verao.xlsx"
):
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:

        # -------- Aba 1: RESUMO --------
        resumo_dict = {
            "Lucro (R$)": lucro,
            "Energia Gerada (MWh)": energia_gerada,
            "Energia Demandada (MWh)": energia_demandada,
            "Capacidade PV (p.u.)": cap_pv,
            "Capacidade WT (p.u.)": cap_wt,
            "Capacidade Carga (p.u.)": cap_load,
            "Delta de Corte (%)": delta,
            "Estação": season,
            "Horas de Simulação (Nt)": Nt,
            "ID do Cenário": idx,
            "Violações de Restrições": res.CV[0] if hasattr(res, "CV") else 0
        }
        df_resumo = pd.DataFrame(resumo_dict.items(), columns=["Variável", "Valor"])
        df_resumo.to_excel(writer, sheet_name="Resumo", index=False)

        # -------- Aba 2: VARIÁVEIS MATRIZES --------
        variaveis_matrizes = [
            'p_bm', 'p_chg', 'p_dch', 'soc', 'p_dl',
            'u_bm', 'u_chg', 'u_dch', 'u_dl',
            'p_l', 'p_pv', 'p_wt', 'p_dl_ref',
            'tau_pld', 'tau_dist', 'tau_dl'
        ]

        worksheet = writer.book.add_worksheet("Variaveis_Matrizes")
        writer.sheets["Variaveis_Matrizes"] = worksheet

        row = 0
        for key in variaveis_matrizes:
            if key in data:
                val = data[key]

                # Converte para DataFrame
                if isinstance(val, (list, tuple)):
                    val = pd.DataFrame(val)
                elif not isinstance(val, pd.DataFrame):
                    val = pd.DataFrame(val)

                # Ajuste para que os taus virem vetores linha (1 linha, N colunas)
                if key in ['tau_pld', 'tau_dist', 'tau_dl']:
                    if val.shape[0] > val.shape[1]:
                        val = val.T  # só transpõe se estiver como vetor coluna
                    val.index = [0]  # força o índice para garantir linha única

                # Título da variável
                worksheet.write(row, 0, key)
                row += 1

                # Escreve os valores
                for i in range(val.shape[0]):
                    for j in range(val.shape[1]):
                        worksheet.write(row + i, j, float(val.iat[i, j]))
                row += val.shape[0] + 2
            else:
                print(f"Aviso: '{key}' não encontrado em data.")

        # -------- Aba 3: PARÂMETROS --------
        parametros = {}
        for k, v in data.items():
            if k not in variaveis_matrizes:
                if isinstance(v, (list, tuple)):
                    v = list(v)
                elif hasattr(v, 'tolist'):
                    v = v.tolist()
                parametros[k] = v

        df_parametros = pd.DataFrame([
            {"Parâmetro": k, "Valor": str(v)} for k, v in parametros.items()
        ])
        df_parametros.to_excel(writer, sheet_name="Parametros", index=False)

        # -------- Aba 4: PARÂMETROS DO GA --------
        if ga_params is not None:
            df_ga = pd.DataFrame([
                {"Parâmetro GA": k, "Valor": str(v)} for k, v in ga_params.items()
            ])
            df_ga.to_excel(writer, sheet_name="Parametros_GA", index=False)
