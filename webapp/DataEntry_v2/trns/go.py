# -*- coding: utf-8 -*-

from campaigns.models import Properties

en=[
u"ByPass by Value: Jump depending on list value (YES)",
u"ByPass by Value: Jump depending on list value (NO)",
u"ByPass : Jump always",
u"ByPass Blank: Jump if field is not in blank",
u"ByPass Screen: Jump to another page",
u"Alpha Adjust: Alphanumeric adjust.",
u"identifier Select: Written code selects text in another field",
u"identifier Select: Text selects code",
u"identifier Select: Automatic selection from dropdown.",
u"identifier Select: List mode. If value dont exist, its created in list.",
u"OCR: Number or Text.",
u"OCR: BarCode.",
u"Image: Selected Image Area on screen for data entry.",
u"Alphanumeric Mask: Alphanumeric Mask.",
u"Numeric Mask: Numeric Mask.",
u"Alphanumeric Mask sprintf: C sprintf texts and numeric transformation.",
u"To Be verified: Field to VERIFY N times.",
u"Required: Required field.",
u"FillAll: FILL FIELD completely.",
u"ListShowText: Grabs code, show text in LIST.",
u"MinValue: Integer MINimum value accepted.",
u"MaxValue: Integer MAXimum value accepted.",
u"FillOR: Fill field or the selected field.",
u"ImgPath: Image Path in field"
]

fr=[
u"ByPass en fonction de la valeur : Sauter en fonction de la valeur de la liste (OUI) ",
u"ByPass par valeur : Sauter en fonction de la valeur de la liste (NON) ",
u"ByPass : Sauter toujours",
u"ByPass vierge : Sauter si le champ n'est pas en blanc",
u"ByPass Ecran : Sauter à une autre page",
u"Alpha Adjust : Ajustement alphanumérique",
u"Identifiant Select : Le code écrit sélectionne le texte dans un autre champ",
u"identifiant Select : Le texte sélectionne le code",
u"identificateur Select : Sélection automatique à partir d'une liste déroulante",
u"identificateur Select : Mode liste. Si la valeur n'existe pas, elle est créée dans la liste.",
u"OCR : Nombre ou Texte.",
u"OCR : Code barre.",
u"Image : Image sélectionnée Zone de l'écran pour la saisie de données.",
u"Masque Alphanumérique : Masque alphanumérique.",
u"Masque Numérique : Masque Numérique.",
u"Masque alphanumérique sprintf : Textes sprintf en C et transformation numérique.",
u"To Be Verified : Champ à VERIFIER N fois.",
u"Obligatoire : Champ obligatoire.",
u"FillAll : Remplir entièrement le champ.",
u"ListShowText : Saisit le code, affiche le texte dans la LISTE.",
u"MinValue : Integer MINimum value accepted.",
u"MaxValue : Integer MAXimum value accepted.",
u"FillOR : Remplir le champ ou le champ sélectionné.",
u"ImgPath : Chemin de l'image dans le champ"
]

de=[
u"ByPass by Value: Springen in Abhängigkeit vom Listenwert (YES)",
u"ByPass by Value: Abhängig vom Listenwert springen (NEIN)",
u"ByPass: Springen immer",
u"ByPass Blank: Springen, wenn das Feld nicht leer ist",
u"ByPass Bildschirm: Zu einer anderen Seite springen",
u"Alpha-Anpassung: Alphanumerische Anpassung",
u"Kennung auswählen: Schriftlicher Code wählt Text in einem anderen Feld aus",
u"Bezeichner auswählen: Text wählt Code aus",
u"Bezeichner Auswählen: Automatische Auswahl aus Dropdown",
u"Bezeichner Auswählen: Listenmodus. Wenn der Wert nicht existiert, wird er in der Liste erstellt.",
u"OCR: Zahl oder Text.",
u"OCR: BarCode.",
u"Bild: Ausgewählter Bildbereich auf dem Bildschirm für die Dateneingabe.",
u"Alphanumerische Maske: Alphanumerische Maske.",
u"Numerische Maske: Numerische Maske.",
u"Alphanumerische Maske: sprintf: C sprintf Texte und numerische Transformation.",
u"To Be verified: N-mal zu VERIFYendes Feld.",
u"Erforderlich: Erforderliches Feld.",
u"FillAll: FILL FIELD vollständig ausfüllen.",
u"ListShowText: Greift Code, zeigt Text in LISTE.",
u"MinValue: Ganzzahliger MINIMALER akzeptierter Wert.",
u"MaxValue: Ganzzahliger MAXimalwert, der akzeptiert wird.",
u"FillOR: Füllt das Feld oder das ausgewählte Feld.",
u"ImgPath: Bildpfad im Feld"
]

es=[
u"ByPass por valor: Saltar en función del valor de la lista (SÍ)",
u"ByPass por valor: Saltar según valor en lista (NO)",
u"ByPass: Saltar siempre",
u"ByPass en Blanco: Salta si el campo no está en blanco",
u"ByPass Pantalla: Saltar a otra página",
u"Ajuste alfanumérico: Ajuste alfanumérico",
u"Identificador Seleccionar: El código escrito selecciona el texto en otro campo",
u"identificador Seleccionar: El texto selecciona el código",
u"identificador Seleccionar: Selección automática desde el desplegable",
u"identificador Seleccionar: Modo lista. Si el valor no existe, se crea en la lista",
u"OCR: Número o Texto",
u"OCR: Código de barras",
u"Imagen: Área de imagen seleccionada en la pantalla para la entrada de datos",
u"Máscara alfanumérica: Máscara alfanumérica",
u"Máscara numérica: Máscara numérica",
u"Máscara alfanumérica sprintf: C sprintf textos y transformación numérica",
u"A verificar: Campo a VERIFICAR N veces",
u"Requerido: Campo obligatorio",
u"FillAll: Rellenar completamente el campo",
u"ListShowText: Agarra el código, muestra el texto en la LISTA",
u"MinValue: Valor mínimo entero aceptado",
u"MaxValue: Valor maximo entero aceptado.",
u"FillOR: Rellena el campo o el campo seleccionado",
u"ImgPath: Ruta de la imagen en el campo"]

ids=[
u"B1",
u"B2",
u"B3",
u"B4",
u"B5",
u"A1",
u"C1",
u"C2",
u"C3",
u"C4",
u"O1",
u"O2",
u"I1",
u"M1",
u"M2",
u"M3",
u"V1",
u"R1",
u"F1",
u"C5",
u"L1",
u"L2",
u"O3",
u"I2"
]


def goload():
	n=0
	for id in ids:
		object=Properties(identifier=id)
		for lang in "en,fr,de,es".split(","):
			object.set_current_language(lang)
			object.description=eval(lang+"[n]")
			object.save()
		n+=1
		print object.description
    

