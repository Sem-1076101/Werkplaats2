# wp2-2023-starter
Starter template voor WP2 2023

Helaas is het niet gelukt om de zoekfunctie werkend te krijgen en de vragen pagina's mooi te maken, we hebben het wel geprobeerd maar kwamen er net niet uit.

We hebben een applicatie gemaakt waarbij de admin accounts kan beheren en aanmaken (waaronder admin accounts), De admin kan alle notities en categroien bekijken. Hij kan ook categorien verwijderen. Daarnaast kan hij accounts beheren (zoals verwijderen, aanpassen en nieuwe accounts aanmaken). Daarnaast heb je een docenten account, je kan zelf een account aanmaken en inloggen. De inlog en registratie zijn beveiligd, net als grotendeel van de pagina's. Het wachtwoord is hashed opgeslagen en wordt daarop gecontroleerd wanneer je wilt inloggen. 

Als leraar kan je nieuwe notities aanmaken en bekijken. Daarnaast kan je nieuwe categorien toevoegen. Die kan je ophalen bij het maken van notities. Daarnaast kan je met chatgpt vragen genereren. Je eigen vragen kan je aanpassen en verwijderen. Ook kan je de vragen van andere leraar's bekijken. Je ziet een examen vraag en een gegenereerde vraag door chatgpt, als ze hetzelfde zijn betekent dat de lereaar de vraag niet veranderd heeft.



Docent login:
gebruikersnaam: test
wachtwoord: test

admin login:
gebruikersnaam: admin
wachtwoord: admin


Login Scherm:
je kan zelf een account aanmaken en inloggen. De inlog en registratie zijn beveiligd, net als grotendeel van de pagina's. Het wachtwoord is hashed opgeslagen en wordt daarop gecontroleerd wanneer je wilt inloggen.


Docent experience:
Als je de "main.py" opent kom je in de login scherm. hier kan je inloggen met de docent login. Wanneer je inlogt kom je direct bij de notitie pagina. 
Hier kan je nieuwe notities aanmaken, notities bekijken, bewerken en verwijderen. bij het aanmaken van een notitie moet je de titel, bron, openbaar/niet openbaar, de categorie en de notitie zelf invullen. Bij de notities zijn de bronnen klikbaar en opent het de URL. Je kan de notities exporteren naar een CSV bestand. De zoekfunctie die je hier ziet is helaas niet volledig werkend. Verder kan je ook op deze pagina vragen genereren, bewerken en verwijderen.

Als je rechtboven op "categorieen" drukt kom je op de categorieen pagina. Hier kan je nieuw categorieen aanmaken en bekijken. Rechtboven heb je ook een "uitloggen" knop. Als je hier op drukt kom je weer op de login scherm.


Admin experience:
Het meeste werkt hier hetzelfde als bij de docenten. Een admin kan alleen de notities van docenten bekijken. Een admin account heeft een extra tablad "admin". Hier kan je nieuwe docenten toevoegen en deze ook admin rechten geven. in deze tablad kan je ook docenten verwijderen en toevoegen. Verder kan je ook catergorieen verwijderen en bewerken.


# Opstarten
Om het programma op te starten heb je een open ai code nodig, je moet een file genaamd secret.py aanmaken en dan onder de naam: OPENAI_LICENSE de code invullen. In het mapje uitleg_opstart staat een voorbeeld.

Opstarten via terminal:
Je kan in de terminal naar het mapje gaan van dit project en daar python3 main.py in typen. Dan start het project op, voor een voorbeeld kan je in het mapje uitleg_opstart kijken.

Als je in Vscode werkt, kan je ook met de python extensie hem gelijk opstarten. Wel via de main.py


# Wat Hamza gedaan heeft + bronnen:
Header - https://www.w3schools.com/howto/howto_css_responsive_header.asp
notities aanmaken - workshop van sietze en mark + hulp van sem + https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
notities bekijken - workshop van sietze en mark + hulp van sem + https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
exporteren van notities - https://www.geeksforgeeks.org/how-to-create-csv-output-in-flask/ // https://www.youtube.com/watch?v=BP8ulGbu1fc
zoeken van notities (niet werkend gekregen) 
categorieen aanmaken - workshop van sietze en mark + hulp van sem + https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
categorieen bekijken - workshop van sietze en mark + hulp van sem + https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application


# Wat Sem gedaan heeft + bronnen:
Registratie,
Login + beveiligd
Admin pagina overzicht 
Toevoegen van nieuwe accounts admin
Verwijderen van accounts admin
Aanpassen van accounts admin
Styling van admin
Uitloggen
Bekijken van notities admin
Bekijken van categorieën admin
Verwijderen en aanpassen categorieën 
Mooi maken van alles op admin
Routes beheert van admin op index (als admin zie je andere dingen dan leraren )
De vragen genereren met Chatgpt
Gegenereerde vragen veranderen
Gegenereerde vragen verwijderen
Gegenereerde vragen bekijken
Vragen kunnen aanpassen

# Bron:
De grootste hulp die ik gehad heb was het gebruik maken van de tutorials op school,
bijvoorbeeld de flask workshop. Daar haalde ik grotendeels uit, vooral voor de inlog.
Ook voor de routings en etc, uiteindelijk als je de eerste keer iets hebt toegevoegd, veranderd, verwijderd en hebt laten zien. Alles bijna hetzelfde is. 

Verder hieronder youtube videos en sites.

# Videos
Ik had een probleem met import flask, deze video had geholpen (grotendeels)
https://www.youtube.com/watch?v=LjXxTvhilOM&t=7s&ab_channel=ProblemSolvingPoint

Deze video heb ik gebruikt voor het verwijderen, niet letterlijk overgenomen maar wel veel info uitgehaald
https://www.youtube.com/watch?v=7jKsHOZk-IE&t=263s&ab_channel=Codemy.com

Voor de login en registatie dit gekeken.
https://www.youtube.com/watch?v=lAY7nXh83fI&t=676s&ab_channel=TheCodeCity
https://www.youtube.com/watch?v=71EU8gnZqZQ&t=1000s&ab_channel=ArpanNeupane

<!-- Algemene Flask tutorials -->
https://www.youtube.com/watch?v=29JAOgUfDkQ&t=747s&ab_channel=ProgrammingKnowledge
https://www.youtube.com/watch?v=XTpLbBJTOM4&t=827s&ab_channel=ParwizForogh
https://www.youtube.com/watch?v=wO7a7R5GGA8&ab_channel=SandeepSudhakaran
https://www.youtube.com/watch?v=DbAKzi0kR80&t=75s&ab_channel=SandeepSudhakaran (deze niet helemaal gekeken)
https://www.youtube.com/watch?v=xkduX5AaibQ&t=737s&ab_channel=Cairocoders
https://www.youtube.com/watch?v=cYWiDiIUxQc&t=1007s&ab_channel=CoreySchafer

# Sites
https://thepythoncode.com/article/front-end-of-crud-flask-app-using-jinja-and-bootstrap
https://www.w3schools.com/
https://www.codementor.io/@garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
https://dev.to/__junaidshah/creating-a-crud-app-using-flask-and-sqlalchemy-2m5k
https://stackoverflow.com