from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import context.context
from src.prova import Prova

def scrap():
    driver = webdriver.Chrome()
    driver.get(context.context.site)
    #assert "Python" in driver.title
    elem = driver.find_element_by_id("usuario")
    elem.clear()
    elem.send_keys(context.context.login)
    elem = driver.find_element_by_id("senha")
    elem.clear()
    elem.send_keys(context.context.senha)
    elem.submit()
    driver.get(context.context.site+"programas/login/alunos_2004/calendarioAvaliacoes/default.asp?titulo_secao=Calendário%20de%20Avaliações")
    driver.execute_script("javascript: fAbre(163, '4SIR', 2018);")
    driver.implicitly_wait(10)
    elementos = driver.find_elements_by_class_name("i-calendario-row")
    provas = []
    for item in elementos:
        #TODO as vezes vem o NÃO HAVERÁ PROVA e quebra
        data, diaSemana, materia, professor = item.text.split("\n")
        provas.append(Prova(data, diaSemana, materia, professor))
    driver.close()
    return provas


provas = scrap()
for i in provas:
    print(i)