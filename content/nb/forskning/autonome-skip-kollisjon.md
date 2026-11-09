---
title: "Hvordan unngår autonome skip kollisjoner? En oversikt over forskningen"
date: 2026-11-09
description: "En oversiktsartikkel fra 2021 gjennomgår 48 studier av automatisk kollisjonsunngåelse og spør hvor godt metodene dekker sjøveisreglene."
translationKey: "forskning-burmeister-2021"
kilde: "Burmeister og Constapel (2021), CC BY"
---
*Sammendrag av en åpen artikkel. Skrevet av Captain PhD, 9. november 2026.*

## Kort fortalt
Hvis skip skal styres helt eller delvis av datamaskiner, må de kunne følge sjøveisreglene (COLREG). To forskere ved Fraunhofer-senteret for maritim logistikk i Hamburg har gått gjennom forskningen på området. Konklusjonen er at mange metoder fungerer i enkle møtesituasjoner, men at ingen av dem dekker reglene fullt ut, og at det mangler felles måter å teste dem på.

## Spørsmålet
Artikkelen stiller i praksis tre spørsmål. Hvilke metoder for kollisjonsunngåelse og ruteplanlegging er utviklet de siste årene? Hvor godt dekker de sjøveisreglene, særlig del B (styring og seilas)? Og hvor nær er de å kunne brukes i industrien?

## Slik ble det gjort
Dette er en litteraturstudie, ikke et nytt forsøk. Forfatterne søkte i Google Scholar og ResearchGate og fulgte henvisninger fra lovende artikler. De så bare på engelskspråklige, fritt tilgjengelige arbeider fra 2015 til 2020 som handler om selve beslutningen om hva skipet skal gjøre. Rundt 150 arbeider ble vurdert (artikler og masteroppgaver). Etter å ha lest sammendrag og konklusjoner beholdt de 48. Hvert arbeid ble gjennomgått av én forfatter og kontrollert av den andre, og resultatene ble sortert etter faste kategorier: algoritme, testing, område, hva systemet gir som utdata, hvilke sensorer det trenger og hvor mye av reglene det dekker.

## Hva fant de?
- **Metoder.** Nærmeste passeringsavstand (CPA) brukes oftest som utløser for å unngå et annet fartøy. Prediktiv regulering (model predictive control) går igjen i de fleste arbeidene. Dyp forsterkende læring er på vei opp, men fortsatt sjelden. Kunstige potensialfelt er en annen metodeklasse som brukes ofte.
- **Testing.** Det finnes ingen felles, internasjonalt avtalt måte å teste på. De fleste testet i sine egne simulatorer. Få brukte kommersielle skipssimulatorer eller prøvde metoden til sjøs.
- **Hvor de virker.** De fleste metodene er laget for åpent hav og kystfarvann. Få tar for seg trafikkseparasjonssystemer eller trange leder.
- **Data.** AIS og radar er de vanligste datakildene. Vær og sjøgang er med i færre enn én av fem arbeider. Sikten, som avgjør hvilke regler som gjelder, tas sjelden hensyn til.
- **Regler.** De fleste arbeidene behandler bare forbikjøring, møte på motsatt kurs og kryssende kurs, med tilhørende vikeplikt og kursholdsplikt. Bare ett av arbeidene (Kufoalor og medforfattere, 2020) dekker nesten hele del B. Ifølge forfatterne spilte del C (lanterner og signalfigurer) og del D (lyd- og lyssignaler) ingen rolle i metodene de gjennomgikk.

## Begrensninger
Forfatterne peker selv på flere. Søket dekker bare to søkemotorer og bare åpne, engelskspråklige arbeider fra 2015 til 2020. Pressemeldinger fra bransjen ble utelatt fordi de sjelden viser hvordan algoritmene virker. Mange av arbeidene hadde ingen grundig evaluering, så forfatterne kan ikke anbefale en bestemt algoritme. De fleste arbeidene forutsetter også perfekte inndata, og sensorfeil blir stort sett ikke håndtert.

## Hva betyr det for sjøfolk?
Dette er vår egen lesning, ikke artikkelens.
- Reglene som en automatikk har vanskeligst for, er de som krever skjønn: nedsatt sikt (regel 19), trange leder og trafikkseparasjon. Der er sjøfolkenes vurdering fortsatt avgjørende.
- At del C og D ikke spilte noen rolle i metodene, viser hvor mye et menneske leser ut av lanterner, signalfigurer og lydsignaler. Du kan øve på akkurat dette i spillene [Lanterner og dagsignaler](/lanterner/) og [Lydsignaler](/lydsignaler/).
- Skal du bedømme et system som lover «COLREG-kompatibel» kollisjonsunngåelse, er første spørsmål hvilke regler det faktisk er testet mot, i hvilket farvann og i hvilken sikt.

## Kilde
Burmeister, H.-C. og Constapel, M. (2021). Autonomous Collision Avoidance at Sea: A Survey. *Frontiers in Robotics and AI*, 8, artikkel 739013. DOI: [10.3389/frobt.2021.739013](https://doi.org/10.3389/frobt.2021.739013). Åpen tilgang under lisensen [CC BY](https://creativecommons.org/licenses/by/4.0/). Artikkelen er også tilgjengelig på [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC8481591).

*Dette sammendraget er en kilde til orientering og erstatter ikke å lese artikkelen. Alle påstander om innholdet er hentet fra artikkelen; avsnittet «Hva betyr det for sjøfolk?» er vår egen vurdering.*
