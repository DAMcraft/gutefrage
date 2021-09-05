from gutefrage import gutefrage



gfuser = input('Gutefrage Benutzername: ')
gfpass = input('Gutefrage Passwort: ')

gf = gutefrage(gfuser, gfpass)

print(gf.user)

frage_id = gf.convert_to_id("muss-mir-mein-bruder-was-ausbezahlen")

print(frage_id)

frage_url = gf.convert_to_url(frage_id)

print(frage_url)

frage = gf.question(frage_id)

print(frage.info())

frage.like()