import exifread
import math
import os

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

print("Enter Timelapse folder directory")
path = input()
# look through directory
#path = "/home/bryan/Documents/RAW images/"
for image in os.listdir(path):


    # open each file
    f = open(path+image, 'rb')
    print("Opening " + image + "...")
    tags = exifread.process_file(f)

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
    print("Light Value: " + str(lv))
    print("EV: " + str(math.log(fnumber*fnumber/shutter_internal,2)))

# write to new file
#imageio.imwrite('canon no process.tiff',raw)

'''
root = tk.Tk()
root.title("Open LRTL")
app = Application(master = root)
app.mainloop()
'''
