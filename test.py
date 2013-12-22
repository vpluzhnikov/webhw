from bupl.boc import BOC, EMPTY, IN_XLS, IN_DB, IN_SESSION
boc = BOC(type=EMPTY)
boc.data = [{'itemtype1' : 'Сервер приложения', 'cpucount' : '5', 'ostype' : 'Linux (RHEL)'}]
boc.calculate()
print boc.data
