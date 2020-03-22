# URL onde está localizada a tabela: https://www.worldometers.info/coronavirus/#countries

import pandas as pd
import requests
from bs4 import BeautifulSoup

def covid19_brazil(web_page):
  print ("\nFazendo requisição à página %s" %web_page)
  req = requests.get(web_page)

  if req.status_code != 200:
      print ("Falha na requisição. [Error core: %i]\n" %req.status_code)
  else:
      print ("Sucesso na requisição.\n")
      content = req.content

      soup = BeautifulSoup(content, "html.parser")
      table = str(soup.find(name="table", attrs={"id":"main_table_countries_today"}))
      df = pd.read_html(table)[0]

      df_brazil = df[df["Country,Other"].isin(["Brazil", "Total:"])]
      ranking = df_brazil.index[0]+1
      df_brazil.columns = ["Fonte", "TotalDecasos", "NovosCasos", "TotalDeÓbitos", "NovosÓbitos",
                          "Recuperações", "CasosAtivos", "CasosGraves", "DELETAR"]
      df_brazil = df_brazil.drop(["DELETAR"], axis=1)
      df_brazil.loc[df_brazil.Fonte == "Brazil", "Fonte"] = "Brasil"
      df_brazil.loc[df_brazil.Fonte == "Total:", "Fonte"] = "Mundo"
      df_brazil = df_brazil.set_index("Fonte")
      df_brazil["TotalDeÓbitos"] = df_brazil.TotalDeÓbitos.astype('int')
      df_brazil["NovosÓbitos"] = df_brazil.NovosÓbitos.astype('int')
      df_brazil["Recuperações"] = df_brazil.Recuperações.astype('int')
      df_brazil["CasosGraves"] = df_brazil.CasosGraves.astype('int')

      print ("COVID-19: dados do Brasil comparados aos totais mundiais\n")
      print ("Posição no ranking mundial: %i\n" %ranking)

      return df_brazil

def main():
    print(covid19_brazil("https://www.worldometers.info/coronavirus/#countries"))

if __name__ == "__main__":
    main()