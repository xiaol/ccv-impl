import re
from setting import clct_channel

p = re.compile('startSearch\((.*?)\)[^:]')

def handle(filename,modulename,channelIdIndex = -1):
    with open(filename) as f:
        data = f.read()
        matchs = p.findall(data)
        for match in matchs:
            args = match
            channelId = int(args.split(',')[channelIdIndex])
            print channelId
            args = '[' + args.replace('\'','"') + ']'
            print args
            
            clct_channel.update({'channelId':channelId},{'$set':{'handleName':modulename,'handleArgs':args,'processed':True}})
        
def main():
#    handle('search_domestic_teleplay')
#    handle('search_dongman')
#    handle('search_HongKongTaiwan_teleplay')
#    handle('search_hot')
#    handle('search_JapanKorea_teleplay')
#    handle('search_jilupian')
#    handle('search_sport_game')
#    handle('search_teleplay')
#    handle('search_welfare')
#    handle('search_zongyi')
    
    #handle('searchYyetsEd2k_teleplay',1)
    #handle('searchYyetsEd2k',1)
    handle('auto_handle_input.txt','search_teleplay')



if __name__ == '__main__':
    main()