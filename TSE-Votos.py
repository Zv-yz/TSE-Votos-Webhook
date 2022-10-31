import httpx
import time
import math
REFRESH_TIME = 60
WEBHOOK_LINK = ''
ID_MESSAGE = ''
def ConvertPercentage(_str, pur=False):
	if _str != '0,00':
		if pur:
			_str = '0' + _str
		if _str[0] == '0':
			_str = _str[1:]
	if _str == '100,00':
		_str = _str[:len(_str)-3]
	elif _str == '0,00':
		_str = _str[:len(_str)-3]
	else:
		_str = _str[:len(_str)-1]
	return _str

def GetCand(data):
	new_str = ''
	for i in data:
		new_str = new_str + f'> **{i["nm"]}:** {ConvertPercentage(i["pvap"])}% (**{ConvertVotos(i["vap"])}**)\n'
	return new_str

def TotalVotos(data):
	n = 0
	for i in data:
		n += int(i["vap"])
	return n

def ConvertVotos(num):
	num = f'{int(num):_.2f}'.replace('_',',')
	return num[:len(num)-3]

while True:
	req = httpx.get('https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r.json')
	if req.status_code == 200 and 'cand' in req.json():
		data = req.json()["cand"]
		purados = req.json()["pst"]
		_req = httpx.patch(f'{WEBHOOK_LINK}/messages/{ID_MESSAGE}', json={'content': f'**[Resultados das eleições]**\n{GetCand(data)}\n> **Total de Votos:** {TotalVotos(data)}\n> **Urnas Apuradas:** {ConvertPercentage(purados, True)}%\n\nAtualizando <t:{math.floor(time.time())+REFRESH_TIME}:R>'})
		if _req.status_code == 200:
			print('[V] Sucesso ao alterar mensagem do webhook.')
		else:
			print('[ERROR]: Falha ao alterar mensagem do webhook. | {} / {}'.format(_req.status_code, _req.content))
	else:
		print('[ERROR]: Diferente status code, houve algum erro na API. | {} / {}'.format(req.status_code, req.content))
	time.sleep(REFRESH_TIME)
