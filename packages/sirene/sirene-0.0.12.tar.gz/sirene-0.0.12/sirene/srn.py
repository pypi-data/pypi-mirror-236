import pandas as pd
import numpy as np

from iotbr import io_system as ios

from importlib import resources
import io


import warnings
warnings.simplefilter('always', DeprecationWarning)
warnings.warn("The srn module is deprecated and will be discontinued due to mistakes. Please refrain from using it. Instead import module coef.", DeprecationWarning)


def read(sector='agropecuaria',gas='CO2'):
  #File Path
  file_path = '/content/drive/MyDrive/projetos/Bacen/variaveis_ambientais/dicionario/dados_GHG_MCTI/sexta_edicao/estim_6a_ed_1990-2020_'
  #number of subsector
  if sector == "agropecuaria":
    n = 78
  elif sector == "energia":
    n = 32
  elif sector == "ippu":
    n = 28
  elif sector == "lulucf":
    n = 8
  elif sector == "residuos":
    n = 10
  elif sector == "total-brasil-1":
    n = 7
  else:
    n = None

  #select sheet
  #'CO2e_GWP_SAR'
  #'CO2e_GWP_AR5'
  #'CO2e_GTP_AR5'
  #'CO2'
  #'CH4'
  #'N2O'
  with resources.open_binary('sirene.MCTI.sexta_edicao', 'estim_6a_ed_1990-2020_'+sector+'.xlsx') as f:
    data = f.read()
    bytes_io = io.BytesIO(data)
  df = pd.read_excel(bytes_io, sheet_name=gas)
  df = df.loc[4:4+n,:]
  #set columns names
  new_columns = df.iloc[0]
  df = df[1:]
  df.columns = new_columns
  df.set_index(df.columns[0], inplace=True)
  df.rename_axis("setor_nfr", inplace=True)
  return df
  

class nfr_to_cnae: 
    def __init__(self,ghg,year):
        self.ghg = ghg
        self.year = year
        self.group_()
    def group_(self):
        resi =f_residuo(self.ghg,self.year)
        resi['setor_nfr_0'] = 'residuo'
        ippu = f_ippu(self.ghg,self.year)
        ippu['setor_nfr_0'] = 'ippu'
        lulucf = f_lulucf(self.ghg,self.year)
        lulucf['setor_nfr_0'] = 'lulucf'
        lulucf['coeficiente'] = lulucf['coeficiente'].round(3)
        energia = f_energia(self.ghg,self.year)
        energia['setor_nfr_0'] = 'energia'
        agro = f_agropecuaria(self.ghg,self.year)
        agro['setor_nfr_0'] = 'agropecuaria'
        db = pd.concat([resi,ippu, lulucf, energia,agro], axis=0)
        db = db.reset_index(drop=True)
        #db = db.groupby(['setor_nfr_0', 'setor_nfr','emission'])['coeficiente'].sum().reset_index()
        self.dictionary = db.groupby(['setor_nfr_0', 'setor_nfr']).agg({'emission': 'first',
                                                                      'setor_cnae': lambda x: np.array(x),
                                                                      'coeficiente': lambda x: np.array(x)}).reset_index()
        db_ = db.copy()
        db_['total_emission'] = db_['emission'] * db_['coeficiente']
        db_ = db_.groupby(['setor_cnae','setor_nfr_0'])['total_emission'].sum().reset_index()
        pivot_df = db_.pivot(index='setor_cnae', columns='setor_nfr_0', values='total_emission')
        pivot_df = pivot_df.fillna(0)
        pivot_df['total'] = pivot_df['agropecuaria'] + pivot_df['energia'] + pivot_df['ippu'] + pivot_df['lulucf'] + pivot_df['residuo']
        self.emission = pivot_df
        
        

def f_residuo(ghg,year):
  res_m = read('residuos',ghg)
  res_m = res_m.filter(like='5. Resíduos', axis=0)
  res_m = res_m.filter(like=year, axis=1)
  #melt
  res_m = res_m.reset_index()
  res_m = res_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
  #corrigir coluna 'year'
  res_m['year'] = res_m['year'].astype(int).astype(str)
  #atribuir toda emissão ao setor 3680
  res_m['coeficiente'] = 1
  res_m['setor_cnae'] = '3680'
  return res_m

def f_lulucf(ghg,year):
  #passo1: dados sirene
  #emissões por desmatamento dos biomas (exclui-se 'Produtos florestais madeireiros')
  lulucf_m = read('lulucf',ghg)
  lulucf_m = lulucf_m[lulucf_m.index.isin(['Amazônia','Cerrado','Mata Atlântica','Caatinga','Pampa','Pantanal'])]
  #melt data
  lulucf_m = lulucf_m.reset_index()
  lulucf_m = lulucf_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
  #corrigir coluna 'year'
  lulucf_m['year'] = lulucf_m['year'].astype(int).astype(str)
  #passo2: dados desmatamento para criar coeficientes
  #veja o código: criar_tabela_de_coeficientes
  with resources.open_binary('sirene.mapbiomas', 'coeficiente_desmatamento_por_bioma_atividade.csv') as f:
    data = f.read()
    bytes_io = io.BytesIO(data)
  coef = pd.read_csv(bytes_io, sep=',')
  #Criar coluna 'year'
  coef[['start_year', 'end_year']] = coef['year'].str.split('-', expand=True)
  coef['end_year'] = coef['end_year'].astype(int).astype(str)
  #compatibilizar tabelas
  coef['biome'] = coef['biome'].str.title()
  #Concatenate matrix
  #coeficientes da agricultura
  coef_agri = coef[coef['to_level_2'].str.contains('Agriculture')]
  coef_agri = coef_agri[['biome', 'end_year', 'coeficiente']]
  lulucf_agri_m = pd.merge(lulucf_m, coef_agri, left_on=['setor_nfr', 'year'], right_on=['biome', 'end_year'])
  lulucf_agri_m = lulucf_agri_m[['setor_nfr','year','emission','coeficiente']]
  lulucf_agri_m['setor_cnae'] = '0191'
  #coeficientes da pecuária
  coef_pec = coef[coef['to_level_2'].str.contains('Pasture')]
  coef_pec = coef_pec[['biome', 'end_year', 'coeficiente']]
  lulucf_pec_m = pd.merge(lulucf_m, coef_pec, left_on=['setor_nfr', 'year'], right_on=['biome', 'end_year'])
  lulucf_pec_m = lulucf_pec_m[['setor_nfr','year','emission','coeficiente']]
  lulucf_pec_m['setor_cnae'] = '0192'
  #coeficientes da silvicultura
  coef_sil = coef[coef['to_level_2'].str.contains('Forest Plantation')]
  coef_sil = coef_sil[['biome', 'end_year', 'coeficiente']]
  lulucf_sil_m = pd.merge(lulucf_m, coef_sil, left_on=['setor_nfr', 'year'], right_on=['biome', 'end_year'])
  lulucf_sil_m = lulucf_sil_m[['setor_nfr','year','emission','coeficiente']]
  lulucf_sil_m['setor_cnae'] = '0280'
  #distribuimos o coeficiente 'Land Use Mosaic' entre agricultura e pecuária apenas
  coef_mos = coef[coef['to_level_2'].str.contains('Land Use Mosaic')]
  coef_mos = coef_mos[['biome', 'end_year', 'coeficiente']]
  lulucf_mos_agri_m = pd.merge(lulucf_m, coef_mos, left_on=['setor_nfr', 'year'], right_on=['biome', 'end_year'])
  lulucf_mos_agri_m = lulucf_mos_agri_m[['setor_nfr','year','emission','coeficiente']]
  lulucf_mos_agri_m['coeficiente'] = lulucf_mos_agri_m['coeficiente'] /2
  lulucf_mos_agri_m['setor_cnae'] = '0191'

  lulucf_mos_pec_m = pd.merge(lulucf_m, coef_mos, left_on=['setor_nfr', 'year'], right_on=['biome', 'end_year'])
  lulucf_mos_pec_m = lulucf_mos_pec_m[['setor_nfr','year','emission','coeficiente']]
  lulucf_mos_pec_m['coeficiente'] = lulucf_mos_pec_m['coeficiente'] /2
  lulucf_mos_pec_m['setor_cnae'] = '0192'
  #atribuir as emmissões do setor 'Produtos florestais madeireiros' apenas à silvicultura
  lulucf_madeira = read('lulucf',ghg)
  lulucf_madeira = lulucf_madeira.filter(like='Produtos florestais madeireiros', axis=0)
  lulucf_madeira = lulucf_madeira.reset_index()
  lulucf_madeira = lulucf_madeira.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
  lulucf_madeira['year'] = lulucf_madeira['year'].astype(int).astype(str)
  #atribuir toda emissão ao setor 3680
  lulucf_madeira['coeficiente'] = 1
  lulucf_madeira['setor_cnae'] = '0280'
  #Passo 3: agregar dados
  #aggrgar todos os dados sobre lulucf
  lulucf_m = pd.concat([lulucf_agri_m, lulucf_pec_m, lulucf_sil_m,lulucf_mos_agri_m,lulucf_mos_pec_m, lulucf_madeira], axis=0)
  lulucf_m = lulucf_m[lulucf_m['year'].str.contains(year)]
  return lulucf_m


def f_ippu(ghg,year):
  #passo 1): dados de emissões
  #ippu emission
  ippu_m = read('ippu',ghg)
  ippu_m = ippu_m.reset_index()
  #passo 2) distribuicoes faceis, 1 para 1
  #2.A.   Indústria Mineral
  nfr_1 = ['2.A.1.', '2.A.2.', '2.A.3.','2.A.4.']
  cnae_1 = ['2300','2091','2300','2300']
  #2.B.   Indústria Química
  nfr_2 = ['2.B.   ']
  cnae_2 = ['2091']
  #2.C.   Indústria Metalúrgica
  nfr_3 = ['2.C.1.', '2.C.2.', '2.C.3.','2.C.4.','2.C.7.']
  cnae_3 = ['2491','2491','2492','2491','2492']
  #2.D.   Produtos Não Energéticos de Combustíveis e Solventes
  nfr_4 = ['2.D.']
  cnae_4 = ['1991']
  #2.F.   Usos de Produtos como Substitutos para Substâncias Destruidoras da Camada de Ozônio
  nfr_5 = ['2.F.']
  cnae_5 = ['2091']
  #2.G.   Fabricação e Uso de Outros Produtos
  nfr_6 = ['2.G.']
  cnae_6 = ['2600']
  setores_nfr = nfr_1 + nfr_2 + nfr_3 + nfr_4 + nfr_5 + nfr_6
  setores_cnae = cnae_1 + cnae_2 + cnae_3 + cnae_4 + cnae_5 + cnae_6
  ippu_m_1 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  #criar coeficientes
  for i in range(0,len(setores_nfr)):
    ippu_i_m = ippu_m[ippu_m.iloc[:,0].str.contains(setores_nfr[i])]
    #met data
    ippu_i_m = ippu_i_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
    #corrigir coluna 'year'
    ippu_i_m['year'] = ippu_i_m['year'].astype(int).astype(str)
    #atribuir emissão aos setores cnae
    ippu_i_m['coeficiente'] = 1
    ippu_i_m['setor_cnae'] = setores_cnae[i]
    ippu_m_1 = pd.concat([ippu_m_1,ippu_i_m], axis=0)
  #passo 4) coeficientes para a  2.E.   Indústria Eletrônica
  #distribuir entre os códigos knae: 2600 + 2700 (acho que não deve considerar (2800) nessa distribuição pois são bens mecânicos e não eletrônicos.
  #peso: nível de produção de cada cnae por ano
  #! pip install iotbr==0.0.11
  #from iotbr import io_system as ios
  setores_nfr = ['2.E.']
  setores_cnae = ['2600','2700']
  coeficientes = [0.6,1-0.6]
  ippu_m_2 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for i in range(0,len(setores_cnae)):
    ippu_i_m = ippu_m[ippu_m.iloc[:,0].str.contains(setores_nfr[0])]
    #rename column
    #ippu_i_m.rename(columns={ippu_i_m.columns.tolist()[0]: 'setor_nfr'}, inplace=True)
    #ippu_i_m.rename(columns={ippu_i_m.columns[0]: 'setor_nfr'}, inplace=True)
    #met data
    ippu_i_m = ippu_i_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
    #corrigir coluna 'year'
    ippu_i_m['year'] = ippu_i_m['year'].astype(int).astype(str)
    #atribuir emissão aos setores cnae
    ippu_i_m['coeficiente'] = coeficientes[i]
    ippu_i_m['setor_cnae'] = setores_cnae[i]
    ippu_m_2 = pd.concat([ippu_m_2,ippu_i_m], axis=0)
  #passo 5) agregar dados
  #aggrgar todos os dados sobre ippu
  ippu_m = pd.concat([ippu_m_1, ippu_m_2], axis=0)
  ippu_m = ippu_m[ippu_m['year'].str.contains(year)]
  return ippu_m


def f_agropecuaria(ghg,year):
  #Passo 1 ) dados agricultura emission
  agro_m = read('agropecuaria',ghg)
  agro_m = agro_m.reset_index()
  #Passo 2) vamos começar com as distribuições fáceis
  setores_nfr = ['3.A. ','3.B. ','3.C. ','3.D.1.c. ','3.D.1.d. ','3.D.2.a.iii. ','3.D.2.b.iii. ','3.D.2.b.iv. ', '3.F. ']
  setores_cnae = ['0192','0192','0191','0192','0191','0192','0192','0192','0191']
  agro_m_1 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for i in range(0,len(setores_nfr)):
    agro_i_m = agro_m[agro_m.iloc[:,0].str.contains(setores_nfr[i])]
    #met data
    agro_i_m = agro_i_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
    #corrigir coluna 'year'
    agro_i_m['year'] = agro_i_m['year'].astype(int).astype(str)
    #atribuir emissão aos setores cnae
    agro_i_m['coeficiente'] = 1
    agro_i_m['setor_cnae'] = setores_cnae[i]
    agro_m_1 = pd.concat([agro_m_1,agro_i_m], axis=0)
  #Passo 3) primeira deistribuicao dificil
  #3.D.2.b.v.         Mineralização de N associada a perda de C do solo
  #Lagacherie et al. (2016). This study found that the C:N ratio of crop residues is a good predictor of the rate of N mineralization
  #Dristribuir o item (3.D.2.b.v. ) entre 0191, 0192 e 0193.
  #A distribuição deve mevar em consideração o ratio C:N aproximado para agricultura (8:1), pecuária (20:1) e silvicultura (15:1)
  #A distribuição também deve lecar em consideração a área média de agricultura, pecuária e silvicultura.
  #a proporção de áreaplantada não é fixa ao longo dos anos, mas, por simplificação, vamos considerar que ela seja: agricultura (26), pecuária (72) e silvicultura (2)
  #Para melhorar essa distribuição basta ampliar o número de culturas consideradas (amgodão, citrus,..) e a área plantada anualmente.
  #finalmente distribuir as emissões  3.D.2.b.v. Mineralização de N associada a perda de C do solo
  setores_nfr = ['3.D.2.b.v. ']
  setores_cnae = ['0191','0192', '0280']
  coeficientes = [0.465416,0.515538,0.019094] #[0.26/8/0.06983,0.72/20/0.06983,0.02/15/0.06983]
  agro_m_2 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for i in range(0,len(setores_cnae)):
    agro_i_m = agro_m[agro_m.iloc[:,0].str.contains(setores_nfr[0])]
    #met data
    agro_i_m = agro_i_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
    #corrigir coluna 'year'
    agro_i_m['year'] = agro_i_m['year'].astype(int).astype(str)
    #atribuir emissão aos setores cnae
    agro_i_m['coeficiente'] = coeficientes[i]
    agro_i_m['setor_cnae'] = setores_cnae[i]
    agro_m_2 = pd.concat([agro_m_2,agro_i_m], axis=0)
  #Passo 4) segunda distribuição dificil
  # 3.D.1.e.       Mineralização de N associada a perda de C do solo
  setores_nfr = ['3.D.1.e. ']
  setores_cnae = ['0191','0192', '0280']
  coeficientes = [0.465416,0.515538,0.019094]
  agro_m_3 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for i in range(0,len(setores_cnae)):
    agro_i_m = agro_m[agro_m.iloc[:,0].str.contains(setores_nfr[0])]
    #met data
    agro_i_m = agro_i_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
    #corrigir coluna 'year'
    agro_i_m['year'] = agro_i_m['year'].astype(int).astype(str)
    #atribuir emissão aos setores cnae
    agro_i_m['coeficiente'] = coeficientes[i]
    agro_i_m['setor_cnae'] = setores_cnae[i]
    agro_m_3 = pd.concat([agro_m_3,agro_i_m], axis=0)
  #Passo 5) tereceira distribuicao dificil
  #emissões relacionadas ao uso de fertilizantes
  # Os três setores (0191, 0192, e 0280) consomem fertilizantes
  #não sabemos exatamente quanto esses setores consomem de fertilizantes
  #podemos estimar essa proporção através do consumo de produtos uímicos (2091) de cada setor
  #emissões relacionadas ao uso de fertilizantes
  setores_nfr = ['3.D.1.a. ' , '3.D.1.b. ' , '3.D.1.f. ' , '3.D.2.a.i. ', '3.D.2.a.ii. ', '3.D.2.b.i. ' , '3.D.2.b.ii. ' , '3.G. ', '3.H. ', '3.I. ']
  setores_cnae = ['0191','0192','0280']
  coeficientes = [0.89,0.09,0.01]
  agro_m_4 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for m in range(0,len(setores_nfr)):
    for i in range(0,len(setores_cnae)):
      agro_i_m = agro_m[agro_m.iloc[:,0].str.contains(setores_nfr[m])]
      #met data
      agro_i_m = agro_i_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
      #corrigir coluna 'year'
      agro_i_m['year'] = agro_i_m['year'].astype(int).astype(str)
      #atribuir emissão aos setores cnae
      agro_i_m['coeficiente'] = coeficientes[i]
      agro_i_m['setor_cnae'] = setores_cnae[i]
      agro_m_4 = pd.concat([agro_m_4,agro_i_m], axis=0)
  #Passo 6) aggrgar todos os dados sobre agricultura
  agro_m = pd.concat([agro_m_1, agro_m_2,agro_m_3,agro_m_4], axis=0)
  agro_m = agro_m[agro_m['year'].str.contains(year)]
  return agro_m

def f_energia(ghg,year):
  #passo 1) dados sobre emissao
  ener_m = read('energia','CO2e_GWP_SAR')
  ener_m = ener_m.reset_index()
  #passo 2) dictionary dicionario setor_nfr para setor_cnae
  ener_dict = {
      '1.A.1.a. ': {
          'setor_cnae': ['3500'],
          'coeficiente': [1],
      },
      '1.A.1.b. ': {
          'setor_cnae': ['1991'],
          'coeficiente': [1],
      },
      '1.A.1.c. ': {
          'setor_cnae': ['1991'],
          'coeficiente': [1],
      },
      '1.A.2.a. ': {
          'setor_cnae': ['2491'],
          'coeficiente': [1],
      },
      '1.A.2.b. ': {
          'setor_cnae': ['2492'],
          'coeficiente': [1],
      },
      '1.A.2.c. ': {
          'setor_cnae': ['2091','2092','2093','2100','2200'],
          'coeficiente': [0,0,0,0,0],
      },
      '1.A.2.d. ': {
          'setor_cnae': ['1700'],
          'coeficiente': [1],
      },
      '1.A.2.e. ': {
          'setor_cnae': ['1100','1200','1092','1093','1091'],
          'coeficiente': [0,0,0,0,0],
      },
      '1.A.2.f. ': {
          'setor_cnae': ['2300'],
          'coeficiente': [1],
      },
      '1.A.2.g. ': {
          'setor_cnae': ['2991','2992','3000'],
          'coeficiente': [0,0,0],
      },
      '1.A.2.i. ': {
          'setor_cnae': ['0580','0791','0792'],
          'coeficiente': [0,0,0],
      },
      '1.A.2.l. ': {
          'setor_cnae': ['1300'],
          'coeficiente': [1],
      },
      '1.A.3.a.ii. ': {
          'setor_cnae': ['5100'],
          'coeficiente': [1],
      },
      '1.A.3.b. ': {
          'setor_cnae': ['4900'],
          'coeficiente': [1],
      },
      '1.A.3.c. ': {
          'setor_cnae': ['4900'],
          'coeficiente': [1],
      },
      '1.A.3.d.ii. ': {
          'setor_cnae': ['5000'],
          'coeficiente': [1],
      },
      '1.A.4.a. ': {#4580 => 4680
          'setor_cnae': ['4500','4680','3680','5280','5500','5600','6100','6480','6800','6980',\
                        '7180','7380','7880','8592','8591','8691','9080','9480','9700',\
                        '8692','2500','2600','2700','2800','3180','3300','4180','5800',\
                        '5980','6280','7700','8000','8400','1800','1400','1500','1600'],
          'coeficiente': [0,0,0,0,0,0,0,0,0,0,\
                          0,0,0,0,0,0,0,0,0,\
                          0,0,0,0,0,0,0,0,0],
      },
      '1.A.4.b. ': {
          'setor_cnae': ['residencial'],
          'coeficiente': [1],
      },
      '1.A.4.c. ': {
          'setor_cnae': ['0191','0280','0192'],
          'coeficiente': [0,0,0],
      },
      '1.B.1. ': {
          'setor_cnae': ['1991'],
          'coeficiente': [1],
      },
      '1.B.2. ': {
          'setor_cnae': ['0680','1992'],
          'coeficiente': [1],
      }
  }
  #passo 3) criar coeficientes
  #Ajustar coeficientes de acordo com o consumo de energia de cada setor
  sys = ios.system(year,'68','t')
  mZ = sys.mZ
  for j in ener_dict.keys():
    #demanda intermediária dos setores (j) por produtos de petróleo (bem: 3500)
    mZ_j = mZ.loc[:,mZ.columns.str.contains('|'.join(ener_dict[j]['setor_cnae']))]
    mZ_1991_j = mZ_j.loc[mZ_j.index.str.contains('1991'),:]
    #consumo total de (1991) por esses setores
    nZ_1991_j = mZ_1991_j.values.sum()
    #coeficientes por setor
    coeficientes = (mZ_1991_j / nZ_1991_j).values.flatten().tolist()
    #reduzir casas decimais
    coeficientes = [round(x, 3) for x in coeficientes]
    ener_dict[j]['coeficiente'] = [coeficientes]
  #passo 4)atribuir coeficientes
  #distribuir emissões segundo os setores_cnae e os coeficientes criados
  #agropecuaria emission
  ener_m = read('energia',ghg)
  ener_m_1 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for j in ener_dict.keys():
    x_j_m = ener_m.filter(like=j, axis=0)
    x_j_m = x_j_m.filter(like=year, axis=1)
    #met data
    x_j_m = x_j_m.reset_index()
    x_j_m = x_j_m.melt(id_vars=['setor_nfr'], var_name='year', value_name='emission')
    #corrigir coluna 'year'
    x_j_m['year'] = x_j_m['year'].astype(int).astype(str)
    #atribuir emissão aos setores cnae
    x_j_m['coeficiente'] = ener_dict[j]['coeficiente']
    x_j_m['setor_cnae'] = [ener_dict[j]['setor_cnae']]
    #agrupar
    ener_m_1 = pd.concat([ener_m_1,x_j_m], axis=0)
  ener_m_1 = ener_m_1.reset_index(drop=True)
  ener_m_1
  #1.A.4.b. Residencial não está na matriz
  ener_m_1.loc[17,'coeficiente'] = [1]
  #passo 5) converter em dataframe
  ener_m_2 = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
  for j in range(0,len(ener_m_1)):
    ener_m_x = pd.DataFrame(columns=['setor_nfr', 'year', 'emission','coeficiente','setor_cnae'])
    ener_m_x['setor_cnae'] = ener_m_1.loc[j,'setor_cnae']
    ener_m_x['coeficiente'] = ener_m_1.loc[j,'coeficiente']
    ener_m_x['setor_nfr'] = ener_m_1.loc[j,'setor_nfr']
    ener_m_x['year'] = ener_m_1.loc[j,'year']
    ener_m_x['emission'] = ener_m_1.loc[j,'emission']
    ener_m_2 = pd.concat([ener_m_2,ener_m_x], axis=0)
  ener_m_2 = ener_m_2.reset_index(drop=True)
  return ener_m_2
        




