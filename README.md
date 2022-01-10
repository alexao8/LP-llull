# Pràctica de Python i Compiladors - LP Q1 2021-2022

Aquesta pràctica tracta sobre el desenvolupament amb ANTLR4 i Python d'un llenguatge anomenat Llull i el seu interpret a més d'un beatificador pel codi.

Llull és un llenguatge inspirat en Ramon Llull, que té com objectiu ensenyar a als infidels i profans una lògica que no és pogués refutar sobre l'existència de Déu. En aquest sentit el llenguatge és una simplificació del llenguatge C.

Per aquest treball s'han desenvolupat els següents fitxers:

## llull.g4 (ANTLR4)

Aquest fitxer conté la gràmatica sense context del llenguatge i amb ell generarem el parser i el lexer i els tokens per poder interpretar el llenguatge.

Per generar-ho utilitzarem aqusta comanda per consola:

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor llull.g4
```

Això generarà els arxius: llull.tokens, llullLexer.py, llullLexer.tokens, llullParser.py i llullVisitor.py.

## visitor.py (Python)

Una vegada tenim una gramàtica construida, falta donar-li context i significat a les instruccions que hem creat a llull.g. Per això crearem el visitor.py que heredarà de llullVisitor.py per implenetar les seves funcionalitats.

Aquí trobarem l'especfiació del llenguatge, on consultarà la funcionalitat de cada crida. Les assignacions, consultes, operacions, procediments... estan  definits al visitor. La seva funció és, una vegada generat l'arbre de sintaxis, visitar-lo amb l'ordre correcte per interpretar les crides del llenguatge mentre es llegeix i després fer l'acció indicada.

Per això, tenim una funció per cada cas indicat al llull.g.

## llull.py (Python)

A aquest arxiu tenim un scrpit que processa l'arribada per consola de l'arxiu amb el nostre programa en llull i que utilitza el nostre visitor per, com ja hem dit, visitar l'arbre generat amb ANTLR4 anteriorment i poder realitzar el que especifica el programa i donar una sortida si així es demana en el mateix.

## generació de l'interpret

Una vegada tenim tots els fitxers, només necessitem utilitzar la següent comanda per consola per iniciar l'interpret tot passant un arxiu .llull que contindrà el codi del nostre llenguatge llull.

```bash
python3 llull.py programa.llull
```

Per definició, el primer procediment a executar-se és el main, si volem executar-ne un altre, haurem d'especificar-lo amb els seus paràmetres de la següent manera:

```bash
python3 llull.py programa.llull converteix_infidels 10 20
```
## pretty-printer

Com hem dit, també haurem de fer un programa que donat un codi, ens el retorni amb unes unes regles d'estil concretes i uns colors agradables.

Per fer aquest beatificador, s'han fet els dos arxius següents:

### beat.py (Python)

A aquest arxiu tenim un scrpit pràcitament igual al llull.py que processa l'arribada per consola de l'arxiu amb el nostre programa en llull i que utilitza el nostre visitor per, visitar l'arbre generat amb ANTLR4 anteriorment i poder retornar el codi especificat beatificat

### beatVisitor.py (Python)

Al igual que amb el visitor.py, l'objectiu d'aquest beatVisitor és donar-li context i significat a les instruccions que hem creat a llull.g. Per això crearem el beatVisitor.py que heredarà de llullVisitor.py per implenetar les seves funcionalitats.

La diferència prinicpal és que enlloc d'estar implementant les funcionalitats del codi .llull, el que volem és anar imprimint per pantalla, segons com visitem l'arbre de sintaxi, el nostre codi beatificat. Pel que bàsicament és un codi que printa per pantalla i beatifica correctament el nostre codi.

## Llibreries
Les llibreries utilitzades han estat:

- `ANTLR` per escriure la gramàtica i l'intèrpret.

- `sys` per llegir l'entrada per consola al logo3d.py.

- `queue` per utilitzar una pila amb LifoQueue al visitor.py.

- `color` per a la sortida en color per consola del baetificador

Al fitxer `requeriments.txt` es poden trobar les llibreries necessaries per aquesta pràctica i la manera d'instal·lar-ho.

```bash
pip install -r requirements.txt
```

## Autor
Alexandre Alemany Orfila

[alexao8](https://github.com/alexao8)