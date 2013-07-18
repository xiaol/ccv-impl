from telnetlib import Telnet

host = '60.28.29.38'
port = 4000

def startEd2k(url):
    t = Telnet(host,port)
    print t.read_until('command-line:')
    t.write('dllink %s\r\n'%url)
    print t.read_until('command-line:')

def startBT(url):
    t = Telnet(host,port)
    print t.read_until('command-line:')
    t.write('vd\r\n')
    print t.read_until('command-line:')
    t.write('startbt %s\r\n'%url)
    print t.read_until('command-line:')

if __name__ == '__main__':
    #startEd2k('ed2k://|file|%E6%9D%83%E5%8A%9B%E7%9A%84%E6%B8%B8%E6%88%8F.Game.of.Thrones.S03E01.Chi_Eng.WEBrip.720X400-YYeTs%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|286491609|3b99fe9be27bf3ba5f59a664df9c03bb|h=b7jvl7ztsj2imefmf4z5ydmfo2g6iem6|/')
    startBT('22')