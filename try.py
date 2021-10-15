import os 
#os.mkdir('uploads') #to make dir
#os.rmdir('uploads') #to remove dir
#path= 'static'
#filename=
#os.path.abspath('{}/{}'.format(path, filename)) #to get file path

items=[{'id': '1srtAtR52s0g8xnMrkmuMzqs-en_L2M5n', 'name': 'cam18May2021151632.png'},
    {'id': '1GGSF-zvXfWHs5Kcvgth31zirPcIf9VEE', 'name': 'Flask_Web_Development_Developing_Web_Applications_With_Python_by_Miguel_Grinberg_z-lib.org.pdf'}, 
    {'id': '18XnZNpMIbaYdMDEPfnnA32RnDuxpkd0u', 'name': 'gweb.py'}, 
    {'id': '1sRsS3-Is3lyBM3d6guANoTKF_lQB8JK3', 'name': 'drive-app.py'}, 
    {'id': '1TffJSWw2sLlPMuCKJWcAWDPlyaNHIj1E', 'name': 'download-upload-drive.py'}, 
    {'id': '1idAzrd7u0k-cq-Q60JoWcw-dV4aoGxpp', 'name': 'Copy of Welcome To Colaboratory'}, 
    {'id': '1atsG_EyQSbney1d2hXW5j2KqN1X-Vk3nFuYNKOdI5Wk', 'name': 'COBWEB Manual'}, 
    {'id': '14-aM0cUj7006GqzSxsKpq2Blv8o9MuDYk0iooWk9c28', 'name': 'Copy of COBWEB Manual'}, 
    {'id': '1161YKuTmcMfvjxWBF74IQ6JWg_rAtqBN', 'name': 'COBWEB-Literature review'}, 
    {'id': '1zA6Kj4Cx_oYAT1EycCqNow7gHYMdFLYg', 'name': 'me.jpg'}]


for i in items:
    b =[]
    for n, l in i.items():
        b.append(l)
for i in range(0,len(b)):
    print(b[i])