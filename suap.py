# -*- coding: utf-8 -*-
from texttable import Texttable
import requests
from bs4 import BeautifulSoup
import base64

login = 'SEU LOGIN'
password = 'SUA SENHA' # (IN BASE64)

url = 'https://suap.ifsp.edu.br/accounts/login/'
boletim = 'https://suap.ifsp.edu.br/edu/aluno/'+login+'/?tab=boletim'
req = requests.session()
csrf = req.get(url).cookies['csrftoken']
#LOGIN
req.post(url, data = {'username': login , 'password': base64.b64decode(password), 'csrfmiddlewaretoken': csrf})
#GET BOLETIM TABLE
resBoletim = req.get(boletim).text
soup = BeautifulSoup(resBoletim,'lxml')
table = soup.find('table', attrs={'class':'borda'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')
#CREATE OUTPUT TABLE
table = Texttable()
table.set_cols_align(['l', 'r', 'r', 'r'])
table.add_row(['Matéria', 'T.Faltas', 'Freq.', 'Média'])

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    line = []
    line.append(cols[1].split('- ')[1]) # MATERIAS
    line.append(cols[5]) # T. FALTAS
    line.append(cols[6]) # FREQ.
    line.append(cols[8]) # MEDIA
    table.add_row(line)

print(table.draw())
