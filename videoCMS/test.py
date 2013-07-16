import Image
import StringIO



with open('3.jpg','rb') as f:
    s = f.read()
    print s
    print type(s)
    print len(s)
    
    img = Image.open(StringIO.StringIO(s))

print img.size