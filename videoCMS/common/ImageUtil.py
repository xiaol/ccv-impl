import Image,StringIO

def imgconvert(instring,outstream,width2,height2,format='jpeg'):
    img = Image.open(StringIO.StringIO(instring))
    width1,height1 =img.size
    ratio1 = width1*1.0/height1
    ratio2 = width2*1.0/height2
    width_tmp = 0 
    height_tmp = 0 
    if ratio1 > ratio2:
        #height1 -> height2
        height_tmp = int(height2)
        width_tmp = int(height2*1.0/height1*width1)
        img2 = img.resize((width_tmp,height_tmp),Image.BILINEAR)
        box = ((width_tmp-width2)/2,0,(width_tmp-width2)/2+width2,height2)
        img = img2.crop(box)
        img.save(outstream,format)
    else:
        #width1 -> width2
        width_tmp = int(width2)
        height_tmp = int(width2*1.0/width1*height1)
        img2 = img.resize((width_tmp,height_tmp),Image.BILINEAR)
        box = (0,(height_tmp-height2)/2,width2,(height_tmp-height2)/2+height2)
        img = img2.crop(box)
        img.save(outstream,format)
        


