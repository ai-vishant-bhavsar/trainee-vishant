def search(Diractory, sr_fname, prepath = []):
	for key, value in Diractory.items():
		path = prepath + ["/"] + [key]
		if key == sr_fname or value == sr_fname:
			return path
		elif hasattr(value, 'items'):
			p = search(value, sr_fname, path)
			if p is not None:
				return p
	
	

Diractory = {
	'Documents': {
					'work': {'report.docx': None, 'file.exe': None, 'python.py': None},
					'personal': {'Vacation.png': None, 'birthday.png': None, 'folder.zip': None} 
					},
	'Downloads': {'wallpaper.png': None, 'Xender.exe': None, "song.mp3": None},
	'Songs': {
				'Favourite songs': {'mashup2016.mp3': None, 'Tum_Hi_Hona.mp4': None, 'Galliyan.mp4': None, 'Ranjha.mp4': None},
				'All time Favourite': {'Bahara.mp4': None, 'Main_agar_kahu.mp4': None, 'Rattan_Lambiyan.mp4': None, 'Pee_Loon.mp4': None}}
}

sr_fname = str(input("Enter a file name that you want to search : "))
print(f"File {sr_fname} is found on this location : ",end='')
try:
	print(*search(Diractory, sr_fname))
except TypeError:
	print("File not found!!!")
