import exifread
import math
import os
import matplotlib.pyplot as plt

#from rawkit.raw import Raw

#import imageio
import tkinter as tk

class Application (tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.open = tk.Button(self)
        self.open["text"] = "Open Folder"
        self.open["command"] = self.load_folder
        self.open.pack(side="top")
        self.open.pack(side="left")

        self.quit = tk.Button(self, text = "QUIT", fg = "red", command = self.master.destroy)
        self.quit.pack(side = "bottom")

    def load_folder(self):
        print("Heyyy")

# test cr2 compatibility with rawpy
#raw = rawpy.imread('RAW images/IMG_0968.CR2')
#rgb = raw.postprocess()

print("Enter Timelapse folder directory ~~HARD CODE FOR TESTS")
#path = input()
path = 'RAW images'

x=[]
evl=[]
lvl=[]

#search through directory
for image in os.listdir(path):

    #exclude xmp's if edited
    if (image[-3:] == 'xmp'):
        continue

    # open each file
    f = open(path+"/"+image, 'rb')
    print("Opening " + image + "...")
    tags = exifread.process_file(f)

    x.append(image)
    #out = open(image+".txt", "w")
    # go through all exif tags in single photo
    iso = 0.0
    shutter = 0.0
    shutter_internal = 0.0
    fnumber = 0.0
    for tag in tags.keys():
        if tag == "EXIF ISOSpeedRatings":
            iso = int(str(tags[tag]))
        if tag == "EXIF ExposureTime":
            temp = str(tags[tag])
            if "/" in temp:                
                temp = temp.split("/")
                shutter_internal = float(temp[0])/float(temp[1])
                shutter = tags[tag]
            else: shutter_internal = float(temp)
        if tag == "EXIF FNumber":
            string = str(tags[tag])
            if "/" in string:
                string = string.split("/")
                fnumber = float(string[0])/float(string[1])
            else: fnumber = float(string)
        #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            #out.write("Key: " + str(tag) + " , value: " + str(tags[tag]) +"\n")
    
    print( str(iso) + " " + str(shutter) + " f/" + str(fnumber))
    lv = (2 * math.log(fnumber,2)) - math.log(shutter_internal,2) - math.log(iso/100,2)
    lvl.append(lv)
    print("Light Value: " + str(lv))
    ev = math.log(fnumber*fnumber/shutter_internal,2)
    evl.append(ev)
    print("EV: " + str(ev))


plt.plot(x,evl, label = "ev")
plt.plot(x,lvl, label = "lv")
# naming the x axis 
plt.xlabel('image') 
# naming the y axis 
plt.ylabel('value')
plt.legend()

plt.show()

# write to new file
#imageio.imwrite('canon no process.tiff',raw)

'''
root = tk.Tk()
root.title("Open TL")
app = Application(master = root)
app.mainloop()
'''
