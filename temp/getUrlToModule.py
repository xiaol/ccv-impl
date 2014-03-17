#coding=utf-8
__author__ = 'ding'



def main():
    with open('../videoSearch/url_to_module.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not  line.startswith('http://'):
                print  "#",line
                continue
            url,module = line.split(' ')
            url = url.replace('\\','\\\\')
            print "(r'%s','search.%s'),"%(url,module)


if __name__ == '__main__':
    main()