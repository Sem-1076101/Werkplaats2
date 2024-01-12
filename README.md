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


Wat Hamza gedaan heeft + bronnen:
Header
notities aanmaken
notities bekijken
exporteren van notities
zoeken van notities (niet werkend gekregen)
categorieen aanmaken
categorieen bekijken


Wat Sem gedaan heeft + bronnen:
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