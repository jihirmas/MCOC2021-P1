from secciones import SeccionICHA

sec1 = SeccionICHA("H1100x350x369.",base_datos="Perfiles ICHA.xlsx")
print(sec1)

sec2 = SeccionICHA("[]400x200x45.6",base_datos="Perfiles ICHA.xlsx")
print(sec2)

sec3 = SeccionICHA("[]350×200×41.7",base_datos="Perfiles ICHA.xlsx")
print(sec3)

sec3 = SeccionICHA("[]80×40×8.0",base_datos="Perfiles ICHA.xlsx")
print(sec3)

sec3 = SeccionICHA("HR1108×402×430.0",base_datos="Perfiles ICHA.xlsx")
print(sec3)
