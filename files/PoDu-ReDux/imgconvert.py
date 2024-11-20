import os, imgkit

config = imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')
imgkit.from_file('test.html', 'test.png', config=config)
