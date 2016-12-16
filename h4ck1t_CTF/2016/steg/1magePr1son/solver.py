from PIL import Image

def main():
    img = Image.open("./planet.png")
    rgb_img = img.convert("RGB")
    print img

    size = rgb_img.size

    rgb_img2 = Image.new("RGB",size)

    for x in xrange(size[0]):
        for y in xrange(size[1]):
            # get pixel
            r,g,b = rgb_img.getpixel((x,y))

            if x%24==0 and y%24==0:
                if r-g >90 and b-g>90:
                    r = 255
                    g = 255
                    b = 255
                else:
                    r = 0
                    g = 0
                    b = 0
            else:
                r = 0
                g = 0
                b = 0
            rgb_img2.putpixel((x,y),(r,g,b))
    print rgb_img2
    rgb_img2.save("./ans.png")

    img3 = Image.new("RGB",size)

    for x in xrange(size[0]):
        for y in xrange(size[1]):
            # get pixel
            r,g,b = rgb_img2.getpixel((x,y))

            if r==255 and g ==255 and b==255:
                r = 254
                for i in xrange(-2,3):
                    for j in xrange(-2,3):
                        img3.putpixel((x+i,y+j),(r,g,b))
    print img3
    img3.save("./ans_modified.png")

if __name__ == '__main__':
    main()