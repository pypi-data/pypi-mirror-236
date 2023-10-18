# Installation
    pip install tdf.labnum.tdfAnonymizer

**Importation de la librairie**
```
from tdfAnonymizer import anonymizer
```
**Initialisation**
```
anonymizer.initialiser()
```
**Anonymisation et configuration**
```
#Mettre à True les catégories à anonymiser
config = anonymizer.Configuration(ville=True,chaine=True,nom=True,date=True,heure=True,nombre=True,pays=True,entreprise=True,lien=True)

texte_anonymiser = anonymizer.anonymiser_paragraphe("Votre texte",config)
```
**Désanonymisation**
```
texte_desanonymiser = anonymizer.desanonymiser_paragraphe(texte_anonymiser)
```


