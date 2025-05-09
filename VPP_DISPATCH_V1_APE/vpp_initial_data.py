from pathlib import Path
import pandas as pd
import numpy as np
# Script com os dados gerais da VPP 1
# Adaptado de zhou2016_Optimal scheduling of virtual power plant with
# battery degradation cost

path = Path(__file__).parent / 'VPPDATA.csv'

def vpp_data():

    vpp_data = {}

    #  dados usina biomassa
    vpp_data['Nbm'] = 3
    vpp_data['p_bm_min'] = np.array([0.1, 0.1, 0.1]) # Potência mínima (MW)
    vpp_data['p_bm_max'] = np.array([0.5, 0.5, 0.5]) # Potência máxima (MW)
    vpp_data['p_bm_rup'] = np.array([0.5 , 0.5, 0.5]) # Potência de ramp-up (MW)
    vpp_data['p_bm_rdown']  = np.array([0.5, 0.5, 0.5]) # Potência de ramp-down (MW)
    vpp_data['kappa_bm'] = np.array([0.025, 0.025, 0.025]) # Custo de operação (R$/kWh)		
    vpp_data['kappa_bm_start'] = np.array([10.14, 10.14, 10.14]) # Custo de partida(R$/kWh)

    # dados usina FV
    vpp_data['Npv'] = 4
    vpp_data['kappa_pv'] = np.array([0.022, 0.022, 0.022, 0.022])

    # dados usina Eolica
    vpp_data['Nwt'] = 2
    vpp_data['kappa_wt'] = np.array([0.027, 0.027])

    # dados sistema de armazenamento
    vpp_data['Nbat'] = 2
    vpp_data['eta_chg'] = np.array([0.914, 0.914]) # Eficiência da bateria no carregamento (%)
    vpp_data['eta_dch'] = np.array([0.914, 0.914]) # Eficiência da bateria na descarga (%)
    vpp_data['soc_min'] = np.array([0.50, 0.50]) # Nível de carga mínima (MW)
    vpp_data['soc_max'] = np.array([0.75, 0.75]) # Nível de carga máximo (MW)
    vpp_data['p_bat_max']  = np.array([0.1, 0.1]) # Potência máxima da bateria (MW)
    vpp_data['kappa_bat']  = np.array([0.038, 0.038]) # Custo de operação (R$/kWh)
    # OBS: custos da eólica, FV e bateria arbitrados

    # dados cargas despachaveis
    vpp_data['Ndl'] = 2
    
    # dados cargas nao despachaveis
    vpp_data['Nl'] = 3
    
    keys = [ i for i in vpp_data.keys()] # Uso de List Comprehesion para criação de um vetor chaves
    values = [i for i in vpp_data.values()] # Uso de List Comprehesion para a criaçõa de um vetor valores
    VPP_DATA = list(zip(keys, values)) # Utilizando a função zip para unir as duas listas
    VPP_DATA_df = pd.DataFrame(VPP_DATA, columns = ['keys', 'values']) # Transformando as lista em DataFrame
    vpp_data_csv = VPP_DATA_df.to_csv(path, sep = ';', index = False)

   
    return vpp_data

if __name__ == '__main__':

    vpp_data()