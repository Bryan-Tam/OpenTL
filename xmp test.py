from libxmp.utils import file_to_dict
xmp = file_to_dict("RAW images/IMG_0968.CR2")

for item in xmp:
	print(item)