<!-- keywords: Nederlands, Dutch, CBS Data, Dutch Housing Crisis  -->
# De Nederlandse Woningmarkt

Nadat ik was afgestudeerd aan de Tilburg Universiteit met een bacheloropleiding 
in AI en vervolgens (via een traineeship) een baan had gescoord binnen Stedin 
als SAP developer begon mijn zoektocht naar een betaalbare (koop)woning officieel.

Ik had natuurlijk vele slechte verhalen gehoord tijdens mijn studententijd over 
het vinden van accommodatie voor internationale studenten en dat het super lastig 
was, waardoor sommige internationals in andere steden moesten huren. Ik kon nooit 
voorzien dat dit probleem zich nog verder had gemanifesteerd in de woningmarkt 
voor starters…

Met een (degelijk) goed junior salaris kun je tegenwoordig als alleenstaande geen 
koopwoning vinden, zonder misschien miljoenen aan assets in bezit te hebben al.

Ik heb meerdere lidmaatschappen afgesloten bij verschillende woningplatforms om 
zo mijn kansen te vergroten op het bemachtigen van een woning. Honderden reacties. 
Mooi opgestelde berichtjes erbij toegevoegd. Maar met 200+ andere reacties raakt 
jouw mooie berichtje toch snel kwijt.

Hoe kan het zo ver komen?

Met deze vraag in mijn achterhoofd had ik uiteindelijk besloten om zelf de 
CBS-data in te duiken om te zien waar het mis is gegaan en waar eventuele 
verbeterpunten zouden kunnen liggen.

## Het Proces

Om deze vraag te beantwoorden bouwde ik een volledig data-analyseproject 
van scratch. Ik haalde CBS-data op via de OData API, transformeerde die naar 
een SQLite-database met een galaxy-schema, en voerde statistische analyses 
uit in Python — waaronder lineaire regressie, Kruskal-Wallis toetsen en 
STL-tijdreeksdecompositie. De resultaten vertaalde ik naar een interactief 
Power BI dashboard en een wetenschappelijk rapport.

De volledige code en het rapport zijn te vinden op GitHub:
- 👉 [GitHub Repository](https://github.com/Arashi20/Dutch_Housing_Analytics)
- 👉 [Rapport (PDF)](https://github.com/Arashi20/Dutch_Housing_Analytics/blob/main/EINDRAPPORT_De_Nederlandse_Woningcrisis.pdf)

Een korte walkthrough van het dashboard is te bekijken via YouTube:
- 👉 [YouTube Video](https://www.youtube.com/watch?v=Ol4p18ho1Nc)

## Geen Bouwcrisis, Wel een Procescrisis

De data vertellen een duidelijk verhaal: Nederland heeft geen gebrek aan 
bouwplannen, maar een systeem dat die plannen structureel vertraagt.

De gemiddelde doorlooptijd — van vergunningverlening tot oplevering — steeg 
van 16 maanden in 2015 naar ruim 23 maanden in 2025. Een toename van 43% 
in tien jaar. En dat is het gemiddelde: de langzaamste projecten zitten 
inmiddels bijna vier jaar in het bouwproces.

Wat me het meest verraste: van alle woningen die momenteel in de planning 
zitten bevindt meer dan de helft zich nog in de vergunningsfase. Ze zijn 
dus nog niet eens begonnen met bouwen. In de gemeentes waar het het slechtst 
gaat loopt bij twee op de drie projecten de vergunningsprocedure al meer dan 
twee jaar. Niet de bouwsector, maar de papierwinkel is het grootste knelpunt.

Daarnaast zijn de regionale verschillen enorm. Een woning in Noord-Holland 
duurt gemiddeld 74% langer dan in Overijssel. Hetzelfde land, compleet 
andere realiteit. Dit maaktmeteen duidelijk dat een nationale 
one-size-fits-all oplossing niet werkt, het probleem moet opgelost worden door de lokale overheden.

Op basis van de bevindingen doe ik vijf concrete aanbevelingen aan de 
Rijksoverheid: versnel vergunningsprocedures (inclusief automatische 
verlening bij termijnoverschrijding), beperk late bezwaarmogelijkheden, 
stimuleer houtbouw en prefabricage, versterk gemeentelijke capaciteit in 
de zwaarst getroffen regio's, en investeer in opleidingen in de bouwsector.

De conclusie is simpel: de vraag naar woningen is er. Het systeem moet 
die vraag alleen nog omzetten in daadwerkelijk opgeleverde woningen.