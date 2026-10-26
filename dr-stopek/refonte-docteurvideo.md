# Refonte de docteurvideo.com — proposition d'organisation

> **Mise à jour :** la logique du bouton de rendez-vous a changé. Voir `refonte-docteurvideo.html` : chaque page répond d'abord à « pourquoi moi / pourquoi maintenant / pourquoi le Dr Stopek », puis propose **un seul** rendez-vous en fin de page. Dans ce fichier, les mentions « bouton RDV en haut, à la fin et fixe sur téléphone » sont à ignorer.

*Proposition pour le Dr Dan Stopek. Analyse faite le 26 octobre 2026 sur le site en ligne (code HTML de chaque page).*

**Comment lire les balises**

- `[ORIGINAL : /url]` : texte repris tel quel.
- `[ADAPTÉ : /url]` : texte légèrement modifié. La version d'origine est juste en dessous.
- `[NOUVEAU]` : texte écrit pour cette proposition. Il est court.
- `[À COMPLÉTER PAR LE DR STOPEK : ...]` : information absente du site.
- `[ORIGINAL : /url — § « titre »]` : toute la section est reprise sans changement. Le texte exact se trouve dans l'Inventaire (section 1.4). Il n'est pas recopié une seconde fois, pour éviter les erreurs de copie.

---

# 1. Inventaire

## 1.1 Méthode et limites

- Les 14 pages ci-dessous ont été lues dans le code HTML publié. Toutes répondent (code 200).
- Les liens du menu et du pied de page ont été relevés sur chaque page.
- Je n'ai pas pu voir le rendu à l'écran (couleurs, taille des caractères, affichage mobile). Ces points restent à vérifier.
- Je n'ai pas vu le contenu des vidéos. Les titres sont ceux indiqués par YouTube.
- Quatre adresses de votre liste de départ répondent « 404 » aujourd'hui : `/les-cataractes`, `/les-dmla-humides`, `/les-chalazions-cxxo`, `/copie-de-accueil-dr-video`. Elles n'existent plus ou ont été renommées. Il faut quand même prévoir leur redirection (voir section 5).
- Six pages absentes de votre liste existent : `/les-lasers`, `/chalazion-soins-blepharite-massage`, `/corps-flottants-yeux-dpv`, `/diabete`, `/lentilles-de-contact`, `/smile-simulator`.
- Je n'ai pas pu consulter un plan du site (sitemap). Il peut exister d'autres pages non liées.

## 1.2 Menu et pied de page (identiques sur toutes les pages)

- En-tête : « Dr STOPEK — OPHTALMOLOGUE - CHIRURGIEN » (lien vers l'accueil). Une icône nommée « Settings » mène à `/smile-simulator`.
- Menu (9 entrées + « More ») : LES LASERS · CATARACTE · CHALAZION · CORPS FLOTTANTS · MYOPIE · CHARLES BONNET · DIABETE · DMLA · LENTILLES · More
- Pied de page : « DOCTEUR DAN STOPEK / OPHTALMOLOGUE - CHIRURGIEN / 67 BOULEVARD DE PICPUS / 75012 PARIS » puis « 2011-2026 © docteurvideo.com - Tous droits réservés. »
- Lien Doctolib présent dans le code de chaque page : `https://www.doctolib.fr/ophtalmologue/paris/dan-stopek` (boutons) et une variante « booking/motives » (en-tête ou pied de page).
- Aucun numéro de téléphone, aucun plan d'accès, aucune mention légale trouvés dans les 14 pages.

## 1.3 Tableau des pages

| URL | Titre de l'onglet (balise title) | Résumé en une ligne | Vidéos intégrées |
|---|---|---|---|
| `/` | Site du Docteur Stopek - ophtalmologue et chirurgien | Grille de 9 vignettes vers les sujets vidéo. | Aucune (« + de 1.000.000 vues », « 5 vidéos sélectionnées ») |
| `/histoire` | HISTOIRE \| docteurvideo | Pourquoi et comment le Dr Stopek a créé DocteurVideo (thèse 2009). | Aucune |
| `/dans-les-congres` | DANS LES CONGRES \| docteurvideo | Liste des congrès qui ont sélectionné les vidéos (2009 à 2017). | Aucune |
| `/les-lasers` | L'opération de la vue au Laser | Présente la chirurgie réfractive au laser et le déroulement. | Aucune (l'accueil annonce « 3 techniques » ; je n'ai pas trouvé cette vidéo) |
| `/cataracte-operation` | L'opération de la cataracte par Dr Stopek | Page complète : cataracte, implants, intervention, cliniques, FAQ, RDV. | `Tx14OYcf8r8` « LA CATARACTE – Comprendre et traiter l'opacification du cristallin » |
| `/dmla-humide-exsudative` | La DMLA exsudative ou "humide" | Traitements de la DMLA humide, aides, famille, recherche. | `EIVU3JwlNPg` « DMLA – Comprendre la Dégénérescence Maculaire Liée à l'âge et son traitement » |
| `/diabete-retinopathie` | Le diabète peut toucher vos yeux | Le diabète en résumé, stades au fond d'œil, surveillance. | `_0Aw6SX_6rI` « DIABÈTE & RÉTINOPATHIE DIABÉTIQUE – Protéger sa vue quand on est diabétique » |
| `/diabete` | Le diabète expliqué | Page voisine de la précédente, avec des stades de 0 à 4. | Même vidéo `_0Aw6SX_6rI` |
| `/chalazion-soins-blepharite-massage` | Le chalazion expliqué par DocteurVideo | Deux vidéos de soins de paupières. Très peu de texte. | `vji5gGRZfSo` « CHALAZION & BLÉPHARITE – Soins et conseils pratiques (1/2) » ; `t0M6agT6r74` « Le chalazion (2/2) » |
| `/corps-flottants-yeux-dpv` | Les corps flottants expliqués par Dr Stopek | Explique le décollement postérieur du vitré et les signes d'alerte. | `Q0FfCOjziH8` « CORPS FLOTTANTS & DÉCOLLEMENT POSTÉRIEUR DU VITRÉ (DPV) – Ce qu'il faut savoir » |
| `/syndrome-de-charles-bonnet` | Qu'est ce que le syndrome de Charles Bonnet | Une vidéo, presque pas de texte. | `mgyyDiu4qiI` « SYNDROME DE CHARLES BONNET – Hallucinations visuelles et basse vision » |
| `/myopie` | verres de lunettes qui freinent la myopie | Verres pour freiner la myopie de l'enfant. | `yrXCdsMVR7Y` « Freiner la myopie : ce que changent ces nouveaux verres » |
| `/lentilles-de-contact` | Comment poser une lentille de contact? | Deux vidéos : poser les lentilles, précautions et suivi. | `s0D7AnPFWRg` « lentille DV 1 » ; `pKeU0nq5JPY` « lentille DV 2 » |
| `/smile-simulator` | SMILE CALCULATOR \| docteurvideo | Page « SMILE CALCULATOR ». Le contenu (un outil ?) n'apparaît pas dans le texte. | Aucune |

Descriptions (balise meta) relevées. Elles servent de texte d'origine :

- `/` : « Spécialisé dans les corrections laser de la vision et la chirurgie de la cataracte. Le cabinet vous reçoit pour tout bilan visuel, prescription de corrections optiques,  suivi de pathologies (dmla , glaucome, diabète...), 2ème avis... »
- `/les-lasers` : « Le Docteur Stopek maitrise toutes les techniques de chirurgie réfractive au laser. Il effectue votre bilan à son cabinet, vous poropose les techniques possibles et vous guide dans votre choix. Il effectue le Laser dans les centres parisiens équipés des technologies les plus avancées et sécurisées. »
- `/cataracte-operation` : « Le Dr Stopek opère ses patients de la cataracte dans deux cliniques à Paris : la clinique Mont-Louis et la clinique Saint-Jean de Dieu. Le bilan pré-opératoire et le suivi s'effectuent à son cabinet. »
- `/dmla-humide-exsudative` : « Le Dr Stopek vous explique la DMLA "humide" et son traitement »
- `/diabete-retinopathie` : « Le Dr Stopek vous explique comment protéger vos yeux du diabète. »
- `/diabete` : « Le diabète peut altérer votre rétine et votre vision. Voici comment protéger vos yeux... »
- `/chalazion-soins-blepharite-massage` : « Les soins de paupières en vidéo pour se débarrasser du chalazion... »
- `/corps-flottants-yeux-dpv` : « Le décollement postérieur du vitré est la cause la plus fréquent et classique de l 'apparition de corps flottants devant un oeil. Le Dr Stopek vous explique ce phénomène et les précautions à suivre. »
- `/syndrome-de-charles-bonnet` : « "Mamie a des hallucinations alors qu'elle est malvoyante ?!" Rassurez-vous, c'est peut-être un syndrome de Charles Bonnet. Le Dr Stopek vous explique... »
- `/myopie` : « Dr Stopek explique comment fonctionnent les verres qui freinent la myopie chez les enfants et les adolescents »
- `/lentilles-de-contact` : « Le Dr Stopek vous montre comment manipuler les lentilles, et les précautions à respecter pour éviter les infections de la cornée »
- `/histoire`, `/dans-les-congres`, `/smile-simulator` : description vide.

## 1.4 Texte intégral de chaque page

Sont retirés de ce relevé : le menu, le pied de page, et un bloc sur le diabète (« LE PROBLEME / LES CONSEQUENCES / BUT DU TRAITEMENT / L'OBJECTIF / COMMENT Y ARRIVER / LE DEFI »). Ce bloc est présent dans le code de **toutes** les pages, même celles qui ne parlent pas de diabète. Il est repris une fois, au point 1.5.

Sur plusieurs pages (chalazion, lentilles, Charles Bonnet), le texte du code est très court. Le contenu doit être surtout dans les vidéos. Sur `/diabete-retinopathie`, les stades 3 et 4 ne figurent pas dans le texte du code (probablement dans des images) : voir `/diabete`.

##### Texte intégral de /

```text
#### CATARACTE
Comprendre
la cataracte et son traitement
#### LASER DE LA MYOPIE
Présentation des 3 techniques de correction de la myopie au Laser
#### CHALAZION
Conseils pratiques
pour traiter un chalazion
#### CORPS FLOTTANTS
#### LIES A UN DPV
Comprendre le DPV
et prévenir ses risques
#### SYNDROME DE
#### CHARLES BONNET
Créations visuelles
#### DIABETE
Comprendre le diabète
et protéger sa vue
#### MYOPIE
Des lunettes pour
freiner la myopie
#### DMLA
Comprendre la DMLA,
son traitement et son suivi
#### LENTILLES
Conseils pratiques
pour manipuler vos lentilles
```

##### Texte intégral de /histoire

```text
#### L'histoire deDocteurVideo
     Internet a étalé au grand jour les interrogations et les inquiétudes des patients en matière de santé. En témoignent les nombreux émetteurs d'information qui ont fleuri sur la toile, avant de faire irruption dans la relation médecin-patient.
Observant ces changements, le docteur Dan STOPEK* s'intéresse à l'information des patients en matière de chirurgie de la cataracte. Son travail de thèse** étudie les apports et les limites de ces nouvelles sources d'information.
Fort de ses observations, il conçoit un nouvel outil d'information. Il s'agit de vidéos qui répètent et complètent les messages délivrés en consultation. Elles ont le double avantage d'être ciblées donc adaptées au patient, et didactiques grâce à l'utilisation des outils actuels de communication.
La satisfaction des patients l'a amené à concevoir d'autres vidéos. Aujourd'hui, elles sont accessibles à tous sur docteurvideo.com.
* Dr Dan STOPEK, ophtalmologue spécialisé en lasers de la myopie et en chirurgie de la cataracte, est installé à Paris et attaché à l'Hôpital des Quinze-Vingts.
** L'information du patient opéré de la cataracte: analyse, évaluation et optimisation, thèse de médecine présentée publiquement le 6 octobre 2009
DANS LES CONGRES MEDICAUX
```

##### Texte intégral de /dans-les-congres

```text
#### DANS LES CONGRES MEDICAUX
Les vidéos d'information DocteurVideo destinées au patient ont été sélectionnées dans plusieurs congrès médicaux :
Information du patient sur la cataracte:
- 2009: Festival du film d'Ophtalmologie de Deauville
- 2011: Congrès de la Société Française d'Ophtalmologie (SFO)
- 2013: Congrès de la Société de l'Association Française des Implants et de la chirurgie Réfractive (SAFIR)
Information du patient sur le chalazion:
- 2012: Congrès de la Société Française d'Ophtalmologie (SFO)
Information du patient sur la DMLA:
- 2013: Congrès de la Société Française d'Ophtalmologie (SFO)
Information du patient sur le diabète et la rétine:
- 2015: Congrès de la Société Française d'Ophtalmologie (SFO)
Information du patient sur le décollement postérieur du vitré:
- 2017: Congrès de la Société Française d'Ophtalmologie (SFO)
```

##### Texte intégral de /les-lasers

```text
#### LES LASERS DE LA VISION
Le Docteur STOPEK est spécialisé dans les opérations de chirurgie réfractive au laser qu'il pratique depuis 15 ans.
Le bilan préopératoire est effectué au cabinet. Le Docteur STOPEK vous précisera les techniques auxquelles vous êtes éligibles, et vous guidera dans votre choix.
Ses assistantes du Cabinet vous organiseront l'intervention, et resteront à votre disposition pour toute interrogation.
Le Docteur STOPEK pratique les interventions au laser dans deux centres laser à Paris :
  - le Centre Laser Victor Hugo
  - le Centre Laser Vision 15-20
Le suivi sera assuré par le Docteur STOPEK à son cabinet.
 PRENDRE RENDEZ-VOUS
```

##### Texte intégral de /cataracte-operation

```text
#### LA CATARACTE
Vidéo sélectionnée au Festival
du film d'Ophtalmologie du Deauville en 2009
Vidéo sélectionnée au congrès
de la Société Française d'Ophtalmologie en 2011
Vidéo sélectionnée au congrès
de la Société de l'Association Française
des Implants et de chirurgie Réfractive en 2013
Chirurgie de la cataracte à Paris – Dr Dan Stopek
Information patient, stratégie personnalisée et choix des implants
##
#### Qu’est-ce que la cataracte ?
La cataracte correspond à l’opacification progressive du cristallin, la lentille naturelle de l’œil. Elle entraîne une diminution progressive de la qualité de vision.
Les symptômes les plus fréquents sont :
vision floue ou voilée
baisse des contrastes
gêne à la conduite nocturne
éblouissement (phares, soleil)
fatigue visuelle
difficulté à lire
Il s’agit le plus souvent d’une évolution naturelle liée à l’âge.
#### Quand faut-il envisager une opération ?
Il n’existe pas de traitement médical pour faire disparaître la cataracte.
L’intervention est proposée lorsque la gêne visuelle devient significative dans la vie quotidienne :
conduite automobile
lecture
travail sur écran
autonomie générale
activités de loisirs
La décision ne dépend pas uniquement de l’examen de l’œil, mais surtout de la gêne ressentie par le patient.
#### Bilan préopératoire au cabinet du Dr Dan Stopek à Paris
Le bilan préopératoire est réalisé au cabinet :
Dr Dan Stopek – Ophtalmologie
67 boulevard du Picpus
75012 Paris
Cette consultation est une étape essentielle car elle permet :
d’évaluer précisément la cataracte
de mesurer l’œil pour calculer l’implant
de vérifier la rétine et la cornée
de définir les objectifs visuels après chirurgie
#### L’enjeu principal aujourd’hui : choisir sa vision après la chirurgie
La chirurgie de la cataracte ne consiste plus uniquement à remplacer un cristallin opacifié.
Aujourd’hui, la question centrale est :
Quelle vision souhaitez-vous obtenir après l’intervention ?
Grâce aux implants modernes, il est possible de personnaliser le résultat visuel.
Cependant, il est important de comprendre un point fondamental :
 Il n’existe pas d’implant permettant une vision parfaite simultanée de loin, de près et à toutes les distances sans compromis.
Il existe toujours un équilibre à trouver entre :
vision de loin
vision intermédiaire (écran, cuisine…)
vision de près (lecture)
dépendance aux lunettes
confort visuel global
qualité de vision nocturne
sensibilité aux halos
#### Le rôle du chirurgien : accompagner et guider le choix
Pour moi, la valeur principale du chirurgien aujourd’hui n’est pas seulement technique.
Elle consiste à guider le patient dans son choix.
Cela implique :
maîtriser tous les types d’implants disponibles
comprendre leurs avantages et limites
analyser les attentes du patient
évaluer son mode de vie
comprendre ses besoins visuels réels
mesurer son désir d’indépendance aux lunettes
Chaque patient a un profil visuel différent.
La chirurgie devient donc un projet personnalisé construit ensemble.
#### Comment se déroule l’intervention ?
L’opération est réalisée en ambulatoire sous anesthésie locale.
Elle consiste à :
retirer le cristallin opacifié
remplacer par un implant intraoculaire transparent
L’intervention dure environ 10 à 20 minutes.
Le patient rentre à domicile le jour même.
#### Où sont réalisées les interventions ?
Les consultations et bilans préopératoires ont lieu au cabinet :
67 boulevard du Picpus – 75012 Paris
Les interventions chirurgicales sont réalisées dans deux établissements :
Clinique Mont Louis – Paris 11e
Clinique Saint-Jean-de-Dieu – Paris 7e
Ces cliniques disposent d’un plateau technique spécialisé en chirurgie ophtalmologique.
#### Résultats attendus
L’objectif de la chirurgie est d’améliorer la qualité visuelle :
vision plus nette
amélioration des contrastes
réduction de l’éblouissement
amélioration du confort quotidien
Le résultat dépend du type d’implant choisi et de la santé oculaire globale.
####
####
####
#### Questions fréquentes sur la cataracte
### L’intervention est-elle douloureuse ?
Non. Elle est réalisée sous anesthésie locale et est généralement indolore.
### Combien de temps dure l’opération ?
Environ 10 à 20 minutes.
### Quand la vision s’améliore-t-elle ?
Souvent dès les premiers jours, avec une stabilisation progressive sur quelques semaines.
### Peut-on opérer les deux yeux en même temps ?
Non, dans la majorité des cas, les deux yeux sont opérés séparément.
### Vais-je encore porter des lunettes ?
Cela dépend du type d’implant et du projet visuel défini avec le chirurgien.
### La cataracte peut-elle revenir ?
Non. Le cristallin retiré ne repousse pas. Une opacification secondaire peut parfois survenir et se traite facilement au laser.
### Quel est le meilleur implant ?
Il n’existe pas de meilleur implant universel.
Le choix dépend de votre œil, de votre mode de vie et de vos attentes.
### Peut-on conduire après l’opération ?
La reprise de la conduite dépend de la récupération visuelle et est validée lors du suivi post-opératoire.
### À partir de quel âge se fait l’opération ?
Il n’y a pas d’âge précis. La décision dépend de la gêne fonctionnelle.
### L’opération est-elle sûre ?
Oui, c’est une chirurgie très fréquente et très sécurisée.
### Cataracte avancée : est-ce opérable ?
Oui, mais une prise en charge plus précoce facilite souvent la chirurgie.
### Cataracte et DMLA ?
Les deux pathologies peuvent coexister. Le bilan permet d’adapter la stratégie.
### Cataracte et diabète ?
Oui, avec une surveillance adaptée.
### Quand reprendre une activité normale ?
Les activités quotidiennes peuvent souvent être reprises rapidement selon l’évolution.
#### Conclusion
La chirurgie de la cataracte est aujourd’hui une chirurgie personnalisée.
L’enjeu principal n’est plus seulement d’enlever une cataracte, mais de définir un projet visuel adapté à chaque patient.
Cette personnalisation est la clé d’un résultat satisfaisant et durable.
#### Prendre rendez-vous
Une consultation au cabinet du Dr Dan Stopek à Paris permet d’évaluer la cataracte et de définir la meilleure stratégie chirurgicale adaptée à vos besoins visuels
 PRENDRE RENDEZ-VOUS
 PRENDRE RENDEZ-VOUS
```

##### Texte intégral de /chalazion-soins-blepharite-massage

```text
#### LE CHALAZION
## COMMENT LE TRAITER
## PARFOIS UNE CHIRURGIE S'IMPOSE
## EN CAS DE CHALAZIONS A REPETITION:
Consultez votre ophtalmologue
Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2012
```

##### Texte intégral de /corps-flottants-yeux-dpv

```text
#### CORPS FLOTTANTS liés à un DPV
Video sélectionnée au congrès de la Société Française d'Ophtalmologie en 2017
## LE DECOLLEMENT POSTERIEUR DU VITRE (DPV)
Le DPV est un phénomène quasiment normal.  Il est lié au vieillissement du vitré : le gel transparent qui remplit la majorité du volume de l'oeil.  Le vitré est entouré d'une enveloppe (appelée hyaloïde) qui est accolée à la rétine qui constitue la paroi interne de l'oeil à son pôle postérieur.
Avec le temps, le vitré va se liquéfier puis se rétracter au centre de l'oeil. Ceci aboutit au détachement de son enveloppe par rapport à la rétine, c'est ce qu'on appelle le décollement postérieur du vitré ou DPV.
Le DPV se manifeste le plus souvent par l'apparition de corps flottants +/- des flash fugaces. Il faut consulter rapidement votre ophtalmologue qui effectuera un contrôle complet du fond d'oeil, pour s'assurer que le vitré et son enveloppe se sont détachés de la rétine sans la déchirer!
## LES SIGNES D'ALERTE
En cas d'éclairs lumineux, d'apparition de multiples points noirs flottants "pluie de poivre" ou d'un voile noir persistant amputant une partie de la vue d'un oeil => consultez votre ophtalmologue en urgence pour contrôler votre fond d'oeil.
## SI LE FOND D'OEIL REVELE UNE DECHIRURE DE LA RETINE
Le Dr Stopek effectuera du laser Argon sur la déchirure rétinienne pour éviter le risque plus embêtant d'un décollement de rétine.
```

##### Texte intégral de /myopie

```text
#### FREINER LA MYOPIE
## DES VERRES DE LUNETTES POUR FREINER LA MYOPIE
CHEZ LES ENFANTS ET LES ADOLESCENTS
La myopie se développe au cours de l'enfance et de l'adolescence.
Des verres, incorporant des cellules optiques de défocalisation periphérique, visent à limiter le développement de la myopie sont arrivés en France en 2001.
Aujourd'hui la majorité des verriers proposent dans leurs gammes des verres à effet frénateur de myopie.
```

##### Texte intégral de /syndrome-de-charles-bonnet

```text
#### Le syndrome de Charles Bonnet
Conception Dr Dan STOPEK
```

##### Texte intégral de /diabete-retinopathie

```text
#### LE DIABETE
EN RESUME
LE PROBLEME
Trop de sucre dans le sang
LE RISQUE
Atteintes des organes : yeux, coeur, reins, pieds...
LE BUT DU TRATEMENT
Equilibre le taux de sucre dans le sang
L'OBJECTIF
Hémoglobine glyquée <7%
LES MOYENS
Régime alimentaire et activité physique
Observance du traitement
LE DEFI
Equilibre à long terme
EN VIDEO
Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2015
AU FOND D'OEIL
Tout va bien
votre vue : 🙂
fond d'oeil : normal
La rétinopathie s'installe
votre vue : 🙂
fond d'oeil : signes débutants
EN PRATIQUE
## LA SURVEILLANCE
En cas de diabète, effectuez un contrôle ophtalmologique tous les ans
LE TRAITEMENT OCULAIRE
Les traitements oculaires sont adaptés à chaque cas et au stade de l'atteinte ophtalmologique :
* Laser rétinien
* Injection intra-vitréeenne
* Chirurgie oculaire
```

##### Texte intégral de /diabete

```text
#### LE DIABETE
EN RESUME...
## LE PROBLEME
trop de sucre dans le sang circulant
LES CONSEQUENCES
altération des organes: yeux, coeur, reins...
BUT DU TRAITEMENT
équilibrer le sucre dans le sang
L'OBJECTIF
Hb glyquée <7%
COMMENT Y ARRIVER
régime alimentaire,
activité physique
et suivi du traitement
LE DEFI
équilibre à vie
EN VIDEO...
Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2015
AU FOND D'OEIL...
TOUT VA BIEN
controle annuel
LA MALADIE S'INSTALLE
controle rapproché
! équilibre glycémie
LA MALADIE MENACE
+laser
+injections
LA MALADIE SE MANIFESTE
+laser
+injections
+/- Chirurgie
Stade 1
Stade 3
Stade 4
vue normale
vue normale
vue normale +/-
baisse de vue
atteinte débutante
saignements
atteinte sévère
fond d'oeil normal
Stade 0
EN PRATIQUE...
#### Faites un contrôle avec votre ophtalmologue tous les ans.
```

##### Texte intégral de /dmla-humide-exsudative

```text
#### LA DMLA HUMIDE
Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2013
L'INJECTION INTRA-VITREENNE (dite IVT)
Elle est réalisée par votre ophtalmologiste dans une salle dédiée ou un bloc opératoire.
L'oeil concerné est anesthésié avec des gouttes. L'intervention est rapide et n'est pas douloureuse (la sensation équivaut à la piqûre d'une prise de sang).
Vous repartez sans pansement.
LE MEDICAMENT INJECTE
Il appartient au groupe des anti-VEGF, qui luttent contre les vaisseaux anormaux.
En pratique, le médicament ne modifie pas le vaisseau anormal, mais il retire le liquide qu'il a déversé dans la macula (oedème maculaire).
Le coût du médicament est pris en charge à 100% par l'assurance maladie.
LES AUTRES TRAITEMENTS
Ils sont plus anciens et moins efficaces que les injections.
Seule la photothérapie dynamique (dite "PDT") reste utilisée, le plus souvent en deuxième intention. Il s'agit d'un laser qui vise à colmater le vaisseau anormal.
LES COMPLEMENTS ALIMENTAIRES
Ils ont pour objectif de protéger les cellules de la macula qui sont fragilisées par l'oedème maculaire.
Ils sont composés d'antioxydants, d'omégas 3 et de pigments maculaires.
Ils tentent de freiner la maladie.
LA REEDUCATION VISUELLE
Elle permet de "contourner" une gêne dans la vision centrale (comme une tâche masquant des lettres à la lecture).
En cas de perte de la vision centrale, elle permet de développer la vision périphérique.
Elle est réalisée par un orthoptiste spécialisé en "basse vision".
LES EQUIPEMENTS OPTIQUES
Ils comprennent des "lunettes-loupes", des systèmes grossissants et éclairants variés. Le choix d'un équipement optique sera adapté à vos besoins. Ces équipements vous seront proposés par un opticien spécialisé en "basse vision".
A noter que les tablettes numériques peuvent aussi être des outils très utiles.
ERGOTHERAPEUTES, PSYCHOLOGUES
Un ergothérapeute peut vous aider dans les tâches de la vie quotidienne (ex: apprendre à identifier des pièces de monnaie à l'aide du toucher, organisation du domicile).
Un psychologue peut vous aider à accepter le handicap visuel, et ainsi éviter l'isolement social.
LA CONDUITE AUTOMOBILE
Il existe des critères légaux d'aptitude à la conduite automobile.
Demandez à votre ophtalmologiste.LA FAMILLE
L'origine de la DMLA est en partie génétique. Donc si vous êtes atteint, les membres de votre famille ont un risque plus élevé que la moyenne de la population d'être atteint. Informez votre famille afin qu'ils aient un suivi adapté par leur ophtalmologiste.
LA RECHERCHE MEDICALE
Voici quelques axes de recherche actuels, du plus réalisable au plus ambitieux:
- allonger la durée d'action des médicaments pour diminuer le nombre d'injections et de contrôles;
- connaitre les facteurs favorisants génétiques et environnementaux  pour mieux prévenir la maladie (ex: études des habitudes alimentaires);
- remplacer les cellules de la macula pour restaurer une vision centrale: soit par un implant rétinien, soit par des cellules souches...
```

##### Texte intégral de /lentilles-de-contact

```text
#### LES LENTILLES DE CONTACT
LES MANIPULATIONS
LES PRECAUTIONS ET LE SUIVI
```

##### Texte intégral de /smile-simulator

```text
## SMILE CALCULATOR
```

## 1.5 Bloc « diabète » présent dans toutes les pages

```text
LE PROBLEME : trop de sucre dans le sang circulant
LES CONSEQUENCES : altération des organes: yeux, coeur, reins...
BUT DU TRAITEMENT : équilibrer le sucre dans le sang
L'OBJECTIF : Hb glyquée <7%
COMMENT Y ARRIVER : régime alimentaire, activité physique et suivi du traitement
LE DEFI : équilibre à vie
```

Ce bloc n'a de sens que sur les pages diabète. Il faut vérifier s'il s'affiche à l'écran sur les autres pages. Dans la proposition, il ne reste que sur la page diabète.

## 1.6 Autres informations relevées

- Adresse du cabinet : « 67 BOULEVARD DE PICPUS » (pied de page) mais « 67 boulevard du Picpus » (page cataracte).
- Lieux d'intervention cités : Clinique Mont Louis (Paris 11e), Clinique Saint-Jean-de-Dieu (Paris 7e), Centre Laser Victor Hugo, Centre Laser Vision 15-20.
- Aucune page ne mentionne « Cabinet Stopek & Roman » ni un second praticien.
- Pages sans lien depuis le menu : `/histoire` (aucune autre page n'y renvoie) et `/smile-simulator` (icône « Settings »).

---

# 2. Diagnostic

**Ce qui marche**

1. **Les vidéos et leur crédibilité.** « + de 1.000.000 vues » annoncées. Des vidéos sélectionnées dans des congrès de 2009 à 2017. C'est l'actif le plus fort du site.
2. **La page cataracte.** C'est la mieux construite : questions claires, déroulé de l'intervention, lieux, FAQ, deux boutons « Prendre rendez-vous ». Elle sert de modèle aux autres.
3. **Le ton.** Phrases courtes, mots simples. C'est adapté à des patients âgés.

**Ce qui manque ou gêne**

4. **Aucune balise H1.** Aucune des 14 pages n'en contient dans le code publié. Les titres sont en niveau 2 ou 4. Les moteurs de recherche ont peu d'indications sur le sujet de chaque page.
5. **L'accueil ne dit pas ce que fait le Dr Stopek.** Il montre 9 vignettes de sujets vidéo. Le visiteur ne voit pas qu'il opère la cataracte et pratique les lasers, ni où il consulte. Il n'y a pas de phrase d'accroche.
6. **Le rendez-vous est difficile à trouver.** Un lien Doctolib est dans le code de chaque page. Un bouton « PRENDRE RENDEZ-VOUS » n'existe que sur `/cataracte-operation` et `/les-lasers`. Aucun téléphone, aucun plan d'accès.
7. **Une navigation par sujets, sans parcours.** Le menu mélange chirurgie (lasers, cataracte) et information (lentilles, chalazion). Il a 9 entrées plus « More ». Il n'y a pas d'entrée « Le Dr Stopek », « Contact » ou « Rendez-vous ». `/histoire` n'est lié depuis aucune page.
8. **Doublons et restes.** `/diabete` et `/diabete-retinopathie` se recoupent. Le bloc diabète est dans le code de toutes les pages. Quatre anciennes adresses donnent « 404 ». Une icône « Settings » mène à `/smile-simulator`.
9. **Pages presque vides pour Google et pour les malentendants.** Charles Bonnet, lentilles et chalazion : une vidéo, très peu de texte, pas de transcription. Les titres d'onglet de `/histoire`, `/dans-les-congres` et `/smile-simulator` sont peu parlants, avec une description vide. La description de `/les-lasers` contient une faute (« poropose »).
10. **Lisibilité sur téléphone et pour les seniors : à tester.** Taille des caractères, contraste, taille des boutons. Je ne les ai pas vus à l'écran.

---

# 3. Nouvelle arborescence

Principe : l'accueil présente le chirurgien et mène vers trois entrées (cataracte, chirurgie au laser, maladies en vidéo). Chaque page se termine par le bouton de rendez-vous. Les anciennes adresses sont gardées quand c'est possible, pour limiter les redirections.

```text
Accueil                                   /
├─ Le Dr Stopek                           /le-dr-stopek
├─ Chirurgie de la cataracte              /cataracte-operation
├─ Chirurgie réfractive                   /chirurgie-refractive
│   └─ Freiner la myopie de l'enfant      /myopie
├─ Maladies de l'œil en vidéo             /maladies-de-l-oeil-en-video
│   ├─ DMLA humide                        /dmla-humide-exsudative
│   ├─ Diabète et rétinopathie            /diabete-retinopathie
│   ├─ Chalazion                          /chalazion-soins-blepharite-massage
│   ├─ Corps flottants (DPV)              /corps-flottants-yeux-dpv
│   ├─ Syndrome de Charles Bonnet         /syndrome-de-charles-bonnet
│   └─ Lentilles de contact (conseils)    /lentilles-de-contact
├─ Votre parcours au cabinet              /parcours-patient
└─ Infos pratiques et RDV                 /rendez-vous-contact
(à décider : /smile-simulator)
```

**Menu proposé** (6 entrées et un bouton) : Le Dr Stopek · Cataracte · Chirurgie au laser · Maladies de l'œil en vidéo · Votre parcours · Infos pratiques. Plus un bouton fixe **Prendre rendez-vous**, visible aussi sur téléphone.

| Nouvelle page | Reprend (anciennes pages ou blocs) |
|---|---|
| Accueil | Vignettes de `/` ; description de `/` ; compteurs « 1.000.000 vues / 5 vidéos » ; présentation du Dr Stopek de `/histoire` |
| Le Dr Stopek | `/histoire` (entier) ; `/dans-les-congres` (entier) |
| Chirurgie de la cataracte | `/cataracte-operation` (entier, ordre presque inchangé) |
| Chirurgie réfractive | `/les-lasers` ; vignette « Laser de la myopie » de `/` ; `/smile-simulator` (à décider) |
| Freiner la myopie de l'enfant | `/myopie` |
| Maladies de l'œil en vidéo (page d'entrée) | Vignettes de `/` ; entrées du menu |
| DMLA humide | `/dmla-humide-exsudative` |
| Diabète et rétinopathie | `/diabete-retinopathie` + stades de `/diabete` |
| Chalazion | `/chalazion-soins-blepharite-massage` |
| Corps flottants (DPV) | `/corps-flottants-yeux-dpv` |
| Syndrome de Charles Bonnet | `/syndrome-de-charles-bonnet` |
| Lentilles de contact | `/lentilles-de-contact` |
| Votre parcours au cabinet | Blocs « bilan préopératoire », « comment se déroule l'intervention », « où », « résultats » de `/cataracte-operation` ; texte de `/les-lasers` ; description de `/` |
| Infos pratiques et RDV | Pied de page ; bloc « Où sont réalisées les interventions ? » (cataracte) ; centres laser (`/les-lasers`) ; lien Doctolib |

---

# 4. Contenu par page

**Règles communes**

- Les titres écrits en capitales sur le site actuel passent en minuscules normales. Je ne le signale pas comme « adapté ».
- Les fautes d'orthographe évidentes sont corrigées et signalées en `[ADAPTÉ]`.
- Chaque page n'a qu'un seul H1. Les sections sont en H2, les sous-sections en H3.
- **Bouton RDV** : libellé `PRENDRE RENDEZ-VOUS` `[ORIGINAL : /cataracte-operation]`. Lien : `https://www.doctolib.fr/ophtalmologue/paris/dan-stopek`. Il est placé en haut de la page, à la fin, et dans le menu (fixe sur téléphone).
- **Pied de page** (toutes pages) : `[ORIGINAL : /]` « DOCTEUR DAN STOPEK / OPHTALMOLOGUE - CHIRURGIEN / 67 BOULEVARD DE PICPUS / 75012 PARIS » puis « 2011-2026 © docteurvideo.com - Tous droits réservés. » Ajouter le lien vers « Infos pratiques » et les mentions légales `[À COMPLÉTER PAR LE DR STOPEK : mentions légales]`.
- Le bloc « diabète » (point 1.5) est retiré de toutes les pages, sauf la page diabète.

**Trois blocs de fin de page, réutilisés ci-dessous**

- **RDV-A (cataracte)** : `[ORIGINAL : /cataracte-operation — § « Prendre rendez-vous »]`
- **RDV-B (laser)** : `[NOUVEAU]` « Pour savoir si une chirurgie au laser est possible pour vous, le bilan se fait au cabinet. » + bouton.
- **RDV-C (maladies et conseils)** : `[ADAPTÉ : /]` « Le cabinet vous reçoit pour tout bilan visuel, prescription de corrections optiques, suivi de pathologies (DMLA, glaucome, diabète...), 2ème avis... » + bouton.
  *Version d'origine (description de l'accueil) :* « Le cabinet vous reçoit pour tout bilan visuel, prescription de corrections optiques,  suivi de pathologies (dmla , glaucome, diabète...), 2ème avis... »

---

## 4.1 Accueil — `/`

**Titre d'onglet** `[ORIGINAL : /]` : « Site du Docteur Stopek - ophtalmologue et chirurgien »
**H1** `[NOUVEAU]` : Dr Dan Stopek, ophtalmologue-chirurgien à Paris
**Sous-titre** `[ORIGINAL : /]` : OPHTALMOLOGUE - CHIRURGIEN
**Bouton RDV** : en haut, juste sous le titre.

**Sections, dans l'ordre**

1. **Phrase d'accroche** `[ORIGINAL : /]` (début de la description de l'accueil, aujourd'hui invisible à l'écran) : « Spécialisé dans les corrections laser de la vision et la chirurgie de la cataracte. »
2. **Trois grandes entrées** (cartes avec photo ou image de la vidéo) :
   - Cataracte : `[ORIGINAL : /]` « Comprendre la cataracte et son traitement » → `/cataracte-operation`
   - Chirurgie au laser : `[ORIGINAL : /]` « Présentation des 3 techniques de correction de la myopie au Laser » → `/chirurgie-refractive`
   *Attention : la page laser actuelle ne détaille pas ces 3 techniques. Voir questions.*
   - Maladies de l'œil en vidéo : `[NOUVEAU]` « Comprendre vos yeux en vidéo » → `/maladies-de-l-oeil-en-video`
3. **Qui est le Dr Stopek** `[ORIGINAL : /histoire — note *]` : « Dr Dan STOPEK, ophtalmologue spécialisé en lasers de la myopie et en chirurgie de la cataracte, est installé à Paris et attaché à l'Hôpital des Quinze-Vingts. »
   Lien `[NOUVEAU]` : « Lire son parcours » → `/le-dr-stopek`
   **Photo à fournir** : portrait du Dr Stopek (vraie photo).
4. **DocteurVideo** : `[ORIGINAL : /histoire]` « Il s'agit de vidéos qui répètent et complètent les messages délivrés en consultation. » puis `[ORIGINAL : /]` « + de 1.000.000 vues » et « 5 vidéos sélectionnées » (avec un lien vers la section « Dans les congrès médicaux » de `/le-dr-stopek`). `[À COMPLÉTER PAR LE DR STOPEK : confirmer ou actualiser ces deux chiffres]`
5. **Vignettes vidéo** `[ORIGINAL : /]` : les 9 vignettes actuelles, chacune avec son titre et sa phrase (voir inventaire), regroupées sous « Maladies de l'œil en vidéo ».
6. **Le cabinet** : adresse `[ORIGINAL : /]` + bouton RDV + lien « Infos pratiques ».

**Vidéos** : aucune lancée sur l'accueil (vitesse de chargement et simplicité). Les vignettes mènent aux pages.
**Photos à fournir** : portrait du Dr Stopek ; façade ou entrée du cabinet.

---

## 4.2 Le Dr Stopek — `/le-dr-stopek`

**H1** `[NOUVEAU]` : Le Dr Dan Stopek
**Titre d'onglet** `[NOUVEAU]` : Dr Dan Stopek, ophtalmologue-chirurgien à Paris

1. **Présentation** `[ORIGINAL : /histoire — note *]` : « Dr Dan STOPEK, ophtalmologue spécialisé en lasers de la myopie et en chirurgie de la cataracte, est installé à Paris et attaché à l'Hôpital des Quinze-Vingts. »
   `[À COMPLÉTER PAR LE DR STOPEK : formation, diplômes, numéro RPPS, secteur de conventionnement — rien de cela n'est sur le site]`
2. **L'histoire de DocteurVideo** : `[ORIGINAL : /histoire — § « L'histoire deDocteurVideo »]`, texte complet, notes * et ** comprises. Seule retouche : `[ADAPTÉ]` « L'histoire de DocteurVideo » (espace manquante).
   *Original du titre : « L'histoire deDocteurVideo »*
3. **Dans les congrès médicaux** : `[ORIGINAL : /dans-les-congres — § entier]`. Voir une question sur la formulation « Société de l'Association Française des Implants... ».
4. **Chaîne YouTube** `[NOUVEAU]` : « Toutes les vidéos sont aussi sur la chaîne YouTube du Dr Stopek. » → `https://www.youtube.com/@DrStopek` `[À COMPLÉTER PAR LE DR STOPEK : confirmer la chaîne, absente du site actuel]`
5. **Bouton RDV** (fin de page) + RDV-C.

**Vidéos** : aucune. **Photos à fournir** : portrait ; une photo en consultation ou au cabinet.

---

## 4.3 Chirurgie de la cataracte — `/cataracte-operation`

La page actuelle est déjà la meilleure du site. On garde son texte. On change surtout l'ordre des boutons et l'habillage.

**Titre d'onglet** `[ORIGINAL : /cataracte-operation]` : « L'opération de la cataracte par Dr Stopek »
**H1** `[ORIGINAL : /cataracte-operation]` : « Chirurgie de la cataracte à Paris – Dr Dan Stopek »
**Sous-titre** `[ORIGINAL : /cataracte-operation]` : « Information patient, stratégie personnalisée et choix des implants »
**Bouton RDV** en haut `[NOUVEAU : emplacement seulement]`.

**Sections, dans l'ordre** (toutes `[ORIGINAL : /cataracte-operation — § « titre »]`, à copier sans changement, sauf mention)

1. **Vidéo** (`Tx14OYcf8r8`) + les trois lignes « Vidéo sélectionnée au Festival du film d'Ophtalmologie du Deauville en 2009 / … congrès de la Société Française d'Ophtalmologie en 2011 / … congrès de la Société de l'Association Française des Implants et de chirurgie Réfractive en 2013 »
2. § « Qu'est-ce que la cataracte ? »
3. § « Quand faut-il envisager une opération ? »
4. § « Bilan préopératoire au cabinet du Dr Dan Stopek à Paris » — `[ADAPTÉ]` « 67 boulevard du Picpus » devient « 67 boulevard de Picpus » (pour accorder avec le pied de page)
   *Original : « 67 boulevard du Picpus »*
5. § « L'enjeu principal aujourd'hui : choisir sa vision après la chirurgie »
6. § « Le rôle du chirurgien : accompagner et guider le choix »
7. § « Comment se déroule l'intervention ? »
8. § « Où sont réalisées les interventions ? » — même correction d'adresse
9. § « Résultats attendus »
10. § « Questions fréquentes sur la cataracte » (13 questions, inchangées)
11. § « Conclusion »
12. **RDV-A** : § « Prendre rendez-vous » + bouton
13. `[NOUVEAU]` **À lire aussi** : « Cataracte et DMLA » → `/dmla-humide-exsudative` ; « Cataracte et diabète » → `/diabete-retinopathie` (ces deux questions existent déjà dans la FAQ).
14. `[NOUVEAU]` Lien « Votre parcours au cabinet » → `/parcours-patient`

**Changements de forme seulement** : supprimer les trois titres vides (`####`) de l'original ; mettre « Questions fréquentes » en H2 et chaque question en H3 ; liste à puces pour les symptômes.
**À faire valider par le Dr Stopek** : la réponse « Oui, c'est une chirurgie très fréquente et très sécurisée » (FAQ) est une affirmation médicale ; garder si elle lui convient. Pas de chiffre ajouté.
**Photos à fournir** : le Dr Stopek en consultation ; façade ou salle d'une des deux cliniques `[À COMPLÉTER PAR LE DR STOPEK : autorisation des cliniques]`.

---

## 4.4 Chirurgie réfractive — `/chirurgie-refractive`

**Titre d'onglet / H1** `[ORIGINAL : /les-lasers]` : « L'opération de la vue au Laser »
**Sous-titre** `[ORIGINAL : /les-lasers]` : « Les lasers de la vision »
**Bouton RDV** : en haut.

1. **Introduction** `[ORIGINAL : /les-lasers]` : « Le Docteur STOPEK est spécialisé dans les opérations de chirurgie réfractive au laser qu'il pratique depuis 15 ans. »
   `[À COMPLÉTER PAR LE DR STOPEK : « depuis 15 ans » n'est pas daté ; actualiser le nombre d'années]`
2. **Le bilan au cabinet** `[ORIGINAL : /les-lasers]` : « Le bilan préopératoire est effectué au cabinet. Le Docteur STOPEK vous précisera les techniques auxquelles vous êtes éligibles, et vous guidera dans votre choix. »
3. **Les techniques** `[À COMPLÉTER PAR LE DR STOPEK : noms des techniques pratiquées (le site actuel annonce « 3 techniques » sans les nommer), une phrase par technique, ce qu'elles corrigent. Présenter les techniques à égalité, sans en mettre une seule en avant]`
   Vidéo `[À COMPLÉTER PAR LE DR STOPEK : la vidéo « Présentation des 3 techniques de correction de la myopie au Laser » citée sur l'accueil n'est pas sur la page laser actuelle]`
4. **Ce que l'on corrige** `[À COMPLÉTER PAR LE DR STOPEK : myopie, astigmatisme, hypermétropie, presbytie — lesquels sont traités par laser ? Rien n'est écrit sur le site]`
5. **Où a lieu l'intervention** `[ORIGINAL : /les-lasers]` : « Le Docteur STOPEK pratique les interventions au laser dans deux centres laser à Paris : - le Centre Laser Victor Hugo - le Centre Laser Vision 15-20 »
   `[À COMPLÉTER PAR LE DR STOPEK : adresses des deux centres]`
6. **Organisation** `[ORIGINAL : /les-lasers]` : « Ses assistantes du Cabinet vous organiseront l'intervention, et resteront à votre disposition pour toute interrogation. »
7. **Après l'intervention** `[ORIGINAL : /les-lasers]` : « Le suivi sera assuré par le Docteur STOPEK à son cabinet. »
8. **Simulateur** `[À COMPLÉTER PAR LE DR STOPEK : à quoi sert la page « SMILE CALCULATOR » ? Si c'est un outil utile, le garder en lien ici ; sinon le retirer]`
9. **Lien** `[NOUVEAU]` : « Pour les enfants : des verres de lunettes pour freiner la myopie » → `/myopie`
10. **RDV-B** + bouton.

**Pas de promesse de résultat** : aucun texte sur la précision ou l'indépendance aux lunettes n'est ajouté. **Photos à fournir** : photos réelles des deux centres laser ou du Dr Stopek en consultation `[À COMPLÉTER PAR LE DR STOPEK : autorisation des centres]`.

---

## 4.5 Freiner la myopie de l'enfant — `/myopie`

**Titre d'onglet** `[ORIGINAL : /myopie]` : « verres de lunettes qui freinent la myopie » (majuscule initiale en plus)
**H1** `[ORIGINAL : /myopie]` : « Des verres de lunettes pour freiner la myopie chez les enfants et les adolescents »
**Vidéo** : `yrXCdsMVR7Y`.

1. `[ORIGINAL : /myopie]` « La myopie se développe au cours de l'enfance et de l'adolescence. »
2. `[ADAPTÉ : /myopie]` « Des verres incorporant des cellules optiques de défocalisation périphérique, qui visent à limiter le développement de la myopie, sont arrivés en France en 2001. »
   *Original : « Des verres, incorporant des cellules optiques de défocalisation periphérique, visent à limiter le développement de la myopie sont arrivés en France en 2001. »*
3. `[ORIGINAL : /myopie]` « Aujourd'hui la majorité des verriers proposent dans leurs gammes des verres à effet frénateur de myopie. »
4. `[NOUVEAU]` Lien « Chirurgie réfractive » ← page parente ; **RDV-C**.

---

## 4.6 Maladies de l'œil en vidéo — `/maladies-de-l-oeil-en-video`

**H1** `[NOUVEAU]` : Maladies de l'œil en vidéo
**Introduction** `[NOUVEAU]` : « Le Dr Stopek vous explique en vidéo plusieurs maladies de l'œil et des gestes utiles au quotidien. »

**Cartes** (une par page, ordre proposé : sujets les plus liés à la chirurgie et à la rétine d'abord)

| Carte | Texte | Lien |
|---|---|---|
| DMLA | `[ORIGINAL : /]` « Comprendre la DMLA, son traitement et son suivi » | `/dmla-humide-exsudative` |
| Diabète | `[ORIGINAL : /]` « Comprendre le diabète et protéger sa vue » | `/diabete-retinopathie` |
| Corps flottants liés à un DPV | `[ORIGINAL : /]` « Comprendre le DPV et prévenir ses risques » | `/corps-flottants-yeux-dpv` |
| Syndrome de Charles Bonnet | `[ORIGINAL : /]` « Créations visuelles » | `/syndrome-de-charles-bonnet` |
| Chalazion | `[ORIGINAL : /]` « Conseils pratiques pour traiter un chalazion » | `/chalazion-soins-blepharite-massage` |
| Lentilles | `[ORIGINAL : /]` « Conseils pratiques pour manipuler vos lentilles » | `/lentilles-de-contact` |

Fin de page : **RDV-C**.
`[À COMPLÉTER PAR LE DR STOPEK : la vignette « Créations visuelles » est-elle bien le sous-titre voulu pour Charles Bonnet ?]`

---

## 4.7 DMLA humide — `/dmla-humide-exsudative`

**Titre d'onglet / H1** `[ORIGINAL : /dmla-humide-exsudative]` : « La DMLA exsudative ou "humide" »
**Vidéo** : `EIVU3JwlNPg`, avec `[ORIGINAL]` « Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2013 ». **Bouton RDV** : en haut.

Sections (toutes `[ORIGINAL : /dmla-humide-exsudative — § « titre »]`, dans cet ordre) : L'injection intra-vitréenne (dite IVT) · Le médicament injecté · Les autres traitements · Les compléments alimentaires · La rééducation visuelle · Les équipements optiques · Ergothérapeutes, psychologues · La conduite automobile · La famille · La recherche médicale.

- Retouche de forme seulement : séparer « Demandez à votre ophtalmologiste. » et le titre « La famille », collés dans l'original.
- `[NOUVEAU]` Lien en fin de page : « Cataracte et DMLA » → `/cataracte-operation`. Texte d'appui `[ORIGINAL : /cataracte-operation — FAQ]` : « Les deux pathologies peuvent coexister. Le bilan permet d'adapter la stratégie. »
- Fin de page : **RDV-C**.
**À faire valider** : la phrase « Ils tentent de freiner la maladie » (compléments alimentaires) ; aucune promesse ajoutée.

---

## 4.8 Diabète et rétinopathie — `/diabete-retinopathie`

**Titre d'onglet / H1** `[ORIGINAL : /diabete-retinopathie]` : « Le diabète peut toucher vos yeux »
**Vidéo** : `_0Aw6SX_6rI`, avec `[ORIGINAL]` « Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2015 ». **Bouton RDV** : en haut.

1. **Le diabète, en résumé** `[ORIGINAL : /diabete-retinopathie — § « EN RESUME »]` (le problème, le risque, le but du traitement, les moyens). Ce bloc remplace le « bloc diabète » parasite des autres pages.
   `[ADAPTÉ]` « Le but du tratement » → « Le but du traitement » *(original : « LE BUT DU TRATEMENT »)*
2. **Au fond d'œil** : les stades. `[ORIGINAL : /diabete — § « AU FOND D'OEIL... »]` : « Tout va bien — contrôle annuel » ; « La maladie s'installe — contrôle rapproché, ! équilibre glycémie » ; « La maladie menace — +laser +injections » ; « La maladie se manifeste — +laser +injections +/- Chirurgie ».
   `[À COMPLÉTER PAR LE DR STOPEK : valider l'ordre et le sens des stades 0, 1, 3, 4 et les images de fond d'œil ; le texte de la page /diabete est dans le désordre dans le code]`
   **Images à fournir** : les vrais fonds d'œil du Dr Stopek (présents sur le site actuel).
3. **En pratique — La surveillance** `[ORIGINAL : /diabete-retinopathie]` : « En cas de diabète, effectuez un contrôle ophtalmologique tous les ans »
4. **Le traitement oculaire** `[ORIGINAL : /diabete-retinopathie]` : « Les traitements oculaires sont adaptés à chaque cas et au stade de l'atteinte ophtalmologique : Laser rétinien · Injection intra-vitréeenne · Chirurgie oculaire »
   `[ADAPTÉ]` « intra-vitréeenne » → « intra-vitréenne ». *Original : « Injection intra-vitréeenne »*
5. **Appel final** `[ORIGINAL : /diabete]` : « Faites un contrôle avec votre ophtalmologue tous les ans. » + bouton + **RDV-C**.
6. `[NOUVEAU]` Lien « Cataracte et diabète » → `/cataracte-operation`.

---

## 4.9 Chalazion — `/chalazion-soins-blepharite-massage`

**Titre d'onglet** `[ORIGINAL : /chalazion-soins-blepharite-massage]` : « Le chalazion expliqué par DocteurVideo »
**H1** `[ORIGINAL]` : « Le chalazion »
**Introduction** `[ORIGINAL : meta]` : « Les soins de paupières en vidéo pour se débarrasser du chalazion... »
**Vidéos** : `vji5gGRZfSo` (1/2), `t0M6agT6r74` (2/2), avec `[ORIGINAL]` « Vidéo sélectionnée au congrès de la Société Française d'Ophtalmologie en 2012 ».
**Sections** `[ORIGINAL]` : « Comment le traiter » · « Parfois une chirurgie s'impose » · « En cas de chalazions à répétition : consultez votre ophtalmologue »
`[À COMPLÉTER PAR LE DR STOPEK : les deux premières sections n'ont aucun texte (le contenu est dans la vidéo). Ajouter 3 à 5 lignes issues de la vidéo, ou la transcription]`
Fin de page : **RDV-C**.

---

## 4.10 Corps flottants (DPV) — `/corps-flottants-yeux-dpv`

**Titre d'onglet** `[ORIGINAL]` : « Les corps flottants expliqués par Dr Stopek »
**H1** `[ORIGINAL]` : « Corps flottants liés à un DPV »
**Vidéo** : `Q0FfCOjziH8`, avec `[ORIGINAL]` « Video sélectionnée au congrès de la Société Française d'Ophtalmologie en 2017 » (`[ADAPTÉ]` : « Vidéo », avec accent).
**Sections** (toutes `[ORIGINAL : /corps-flottants-yeux-dpv — § « titre »]`) : Le décollement postérieur du vitré (DPV) · Les signes d'alerte · Si le fond d'œil révèle une déchirure de la rétine.
- Placer **« Les signes d'alerte »** en premier, juste sous la vidéo, pour les patients pressés (changement d'ordre seulement).
- `[À COMPLÉTER PAR LE DR STOPEK : en cas de signe d'alerte, comment joindre le cabinet rapidement ? Un lien Doctolib n'est pas adapté à une urgence]`
Fin de page : **RDV-C**.

---

## 4.11 Syndrome de Charles Bonnet — `/syndrome-de-charles-bonnet`

**Titre d'onglet** `[ORIGINAL]` : « Qu'est ce que le syndrome de Charles Bonnet »
**H1** `[ORIGINAL]` : « Le syndrome de Charles Bonnet »
**Introduction** `[ORIGINAL : meta]` : « "Mamie a des hallucinations alors qu'elle est malvoyante ?!" Rassurez-vous, c'est peut-être un syndrome de Charles Bonnet. Le Dr Stopek vous explique... »
**Vidéo** : `mgyyDiu4qiI`, avec `[ORIGINAL]` « Conception Dr Dan STOPEK ».
`[À COMPLÉTER PAR LE DR STOPEK : cette page n'a aucun texte. Ajouter 3 à 5 lignes issues de la vidéo, ou la transcription]`
Fin de page : **RDV-C**.

---

## 4.12 Lentilles de contact — `/lentilles-de-contact`

**Titre d'onglet** `[ORIGINAL]` : « Comment poser une lentille de contact? »
**H1** `[ORIGINAL]` : « Les lentilles de contact »
**Introduction** `[ORIGINAL : meta]` : « Le Dr Stopek vous montre comment manipuler les lentilles, et les précautions à respecter pour éviter les infections de la cornée »
**Sections** `[ORIGINAL]` : « Les manipulations » (vidéo `s0D7AnPFWRg`) · « Les précautions et le suivi » (vidéo `pKeU0nq5JPY`)
`[À COMPLÉTER PAR LE DR STOPEK : titres plus clairs pour les deux vidéos (« lentille DV 1 / 2 » sur YouTube) ; texte d'appui]`
Fin de page : **RDV-C**.

---

## 4.13 Votre parcours au cabinet — `/parcours-patient`

**H1** `[NOUVEAU]` : Votre parcours au cabinet
**Introduction** `[ADAPTÉ : /cataracte-operation]` : « Le bilan préopératoire et le suivi s'effectuent au cabinet du Dr Stopek. »
*Original (description) : « Le bilan pré-opératoire et le suivi s'effectuent à son cabinet. »*
**Bouton RDV** : en haut.

Quatre étapes. Pour chaque étape, deux colonnes : **Cataracte** et **Laser**.

1. **La consultation** `[ADAPTÉ : /]` : « Le cabinet vous reçoit pour tout bilan visuel, prescription de corrections optiques, suivi de pathologies (DMLA, glaucome, diabète...), 2ème avis... » *(original : voir RDV-C)*
2. **Le bilan préopératoire**
   - Cataracte `[ORIGINAL : /cataracte-operation — § « Bilan préopératoire… »]` : « Cette consultation est une étape essentielle car elle permet : d'évaluer précisément la cataracte / de mesurer l'œil pour calculer l'implant / de vérifier la rétine et la cornée / de définir les objectifs visuels après chirurgie »
   - Laser `[ORIGINAL : /les-lasers]` : « Le bilan préopératoire est effectué au cabinet. Le Docteur STOPEK vous précisera les techniques auxquelles vous êtes éligibles, et vous guidera dans votre choix. »
   `[À COMPLÉTER PAR LE DR STOPEK : durée de la consultation, examens réalisés, documents à apporter (ordonnance, lunettes, lentilles ?)]`
3. **L'intervention**
   - Cataracte `[ORIGINAL : /cataracte-operation — § « Comment se déroule l'intervention ? »]` et § « Où sont réalisées les interventions ? »
   - Laser `[ORIGINAL : /les-lasers]` : « Ses assistantes du Cabinet vous organiseront l'intervention, et resteront à votre disposition pour toute interrogation. » + les deux centres.
   `[À COMPLÉTER PAR LE DR STOPEK : préparation la veille et le jour même, accompagnant, horaires]`
4. **Le suivi**
   - Cataracte `[ORIGINAL : /cataracte-operation — FAQ]` : « Quand la vision s'améliore-t-elle ? Souvent dès les premiers jours, avec une stabilisation progressive sur quelques semaines. » et « Peut-on conduire après l'opération ? La reprise de la conduite dépend de la récupération visuelle et est validée lors du suivi post-opératoire. »
   - Laser `[ORIGINAL : /les-lasers]` : « Le suivi sera assuré par le Docteur STOPEK à son cabinet. »
   `[À COMPLÉTER PAR LE DR STOPEK : calendrier des contrôles après l'intervention]`

**Tarifs, remboursement, mutuelle** : `[À COMPLÉTER PAR LE DR STOPEK : informations à donner avant la consultation, s'il le souhaite. Rien n'est écrit sur le site]`
**Photos à fournir** : salle d'attente, salle d'examen, équipe du cabinet (avec accord des personnes).
Fin de page : bouton RDV.

---

## 4.14 Infos pratiques et rendez-vous — `/rendez-vous-contact`

**H1** `[NOUVEAU]` : Infos pratiques et rendez-vous
**Bouton RDV** : très grand, en haut. `[ORIGINAL : /cataracte-operation]` « PRENDRE RENDEZ-VOUS » → Doctolib.

1. **Le cabinet** `[ORIGINAL : /]` : « DOCTEUR DAN STOPEK / OPHTALMOLOGUE - CHIRURGIEN / 67 BOULEVARD DE PICPUS / 75012 PARIS »
   `[À COMPLÉTER PAR LE DR STOPEK : nom du cabinet (« Cabinet Stopek & Roman » ?), téléphone, horaires, étage et interphone, accès pour fauteuil roulant]`
2. **Comment venir** `[À COMPLÉTER PAR LE DR STOPEK : métro, bus, stationnement ; plan intégré]`
3. **Où sont réalisées les interventions**
   - Cataracte `[ORIGINAL : /cataracte-operation — § « Où sont réalisées les interventions ? »]` : Clinique Mont Louis – Paris 11e ; Clinique Saint-Jean-de-Dieu – Paris 7e.
   - Laser `[ORIGINAL : /les-lasers]` : Centre Laser Victor Hugo ; Centre Laser Vision 15-20.
   `[À COMPLÉTER PAR LE DR STOPEK : adresses complètes des quatre lieux]`
4. **En cas de signe d'alerte** `[ORIGINAL : /corps-flottants-yeux-dpv]` : « En cas d'éclairs lumineux, d'apparition de multiples points noirs flottants "pluie de poivre" ou d'un voile noir persistant amputant une partie de la vue d'un oeil => consultez votre ophtalmologue en urgence pour contrôler votre fond d'oeil. »
   `[À COMPLÉTER PAR LE DR STOPEK : conduite à tenir précise avec le cabinet]`
5. **Autres moyens de prendre rendez-vous** `[À COMPLÉTER PAR LE DR STOPEK : par téléphone ? Pour les personnes qui n'utilisent pas Internet]`
6. **Mentions légales** `[À COMPLÉTER PAR LE DR STOPEK]`.

**Photos à fournir** : façade du cabinet, entrée.

---

# 5. Correspondance des URL (redirections 301)

Le site est bien réalisé avec Wix (confirmé par le code de la page). Sous Wix, les redirections se créent dans les réglages SEO (« Redirections d'URL »). Une redirection ne conserve pas l'ancre (`#...`).

| Ancienne URL | Nouvelle URL | Action |
|---|---|---|
| `/` | `/` | Identique |
| `/histoire` | `/le-dr-stopek` | 301 |
| `/dans-les-congres` | `/le-dr-stopek` | 301 (la section « Dans les congrès médicaux » est sur cette page) |
| `/les-lasers` | `/chirurgie-refractive` | 301 |
| `/smile-simulator` | `/chirurgie-refractive` | 301 **si l'outil est retiré** ; sinon identique |
| `/cataracte-operation` | `/cataracte-operation` | Identique |
| `/les-cataractes` (404 aujourd'hui) | `/cataracte-operation` | 301 |
| `/dmla-humide-exsudative` | `/dmla-humide-exsudative` | Identique |
| `/les-dmla-humides` (404 aujourd'hui) | `/dmla-humide-exsudative` | 301 |
| `/diabete-retinopathie` | `/diabete-retinopathie` | Identique |
| `/diabete` | `/diabete-retinopathie` | 301 |
| `/chalazion-soins-blepharite-massage` | `/chalazion-soins-blepharite-massage` | Identique |
| `/les-chalazions-cxxo` (404 aujourd'hui) | `/chalazion-soins-blepharite-massage` | 301 |
| `/corps-flottants-yeux-dpv` | `/corps-flottants-yeux-dpv` | Identique |
| `/syndrome-de-charles-bonnet` | `/syndrome-de-charles-bonnet` | Identique |
| `/myopie` | `/myopie` | Identique |
| `/lentilles-de-contact` | `/lentilles-de-contact` | Identique |
| `/copie-de-accueil-dr-video` (404 aujourd'hui) | `/` | 301 |
| *(nouvelle page)* | `/maladies-de-l-oeil-en-video` | À créer |
| *(nouvelle page)* | `/parcours-patient` | À créer |
| *(nouvelle page)* | `/rendez-vous-contact` | À créer |

Je n'ai pas vérifié dans Google quelles anciennes adresses sont encore indexées. Les quatre adresses en 404 sont à garder dans la liste par prudence.

---

# 6. Questions pour le Dr Stopek

**Identité et obligations**

1. Quelle est la formulation exacte à utiliser pour votre titre et votre poste : « attaché à l'Hôpital des Quinze-Vingts » (site actuel) ou CHNO des Quinze-Vingts ?
2. Souhaitez-vous indiquer vos diplômes et votre formation ? Lesquels ?
3. Quelles mentions légales faut-il publier (numéro RPPS, conseil de l'Ordre, éditeur du site, hébergeur) ?
4. Le nom du cabinet est-il « Cabinet Stopek & Roman » ? Le Dr Roman doit-il apparaître sur le site ? Avec quelle présentation ?
5. Votre chaîne YouTube (`@DrStopek`) doit-elle être liée ? Les vidéos sont-elles aussi sur YouTube sous la même chaîne ?

**Cabinet et rendez-vous**

6. Quel est le téléphone du cabinet ? Les horaires ? Peut-on prendre rendez-vous par téléphone ?
7. Métro, bus, stationnement, accès pour fauteuil roulant ?
8. Que dit-on à un patient qui a un signe d'alerte (éclairs, voile noir) : numéro, consigne ?
9. Adresse : « boulevard de Picpus » ou « boulevard du Picpus » ? Je propose « de Picpus ».
10. Souhaitez-vous donner des informations sur les tarifs, dépassements d'honoraires, remboursement ? Où ?

**Chirurgie réfractive**

11. Quelles techniques de laser pratiquez-vous ? Quelles sont les « 3 techniques » de la vignette d'accueil ? La vidéo existe-t-elle ? Où est-elle ?
12. Quels défauts de vue sont traités (myopie, astigmatisme, hypermétropie, presbytie) ?
13. « Depuis 15 ans » : quelle formulation actuelle ?
14. Quelles sont les adresses du Centre Laser Victor Hugo et du Centre Laser Vision 15-20 ?
15. À quoi sert `/smile-simulator` (« SMILE CALCULATOR ») ? Faut-il le garder ?

**Cataracte et autres pages**

16. La phrase « chirurgie très fréquente et très sécurisée » vous convient-elle ?
17. Quelles sont les adresses des cliniques Mont Louis et Saint-Jean-de-Dieu ? Peut-on les nommer et les photographier ?
18. Quelle page diabète est la plus à jour, `/diabete` ou `/diabete-retinopathie` ? Pouvez-vous valider les stades 0 à 4 ?
19. Les chiffres « + de 1.000.000 vues » et « 5 vidéos sélectionnées » sont-ils à jour ?
20. Pouvez-vous fournir 3 à 5 lignes (ou la transcription) pour les pages chalazion, Charles Bonnet et lentilles, qui n'ont presque pas de texte ?
21. Faut-il corriger « Société de l'Association Française des Implants et de la chirurgie Réfractive » (page congrès) ? Le nom exact de la société ?
22. Voulez-vous garder la vignette « Créations visuelles » comme sous-titre de Charles Bonnet ?
23. Combien de temps durent les consultations, que faut-il apporter, quel est le calendrier de suivi ? (page « Votre parcours »)

**Photos et vidéos à fournir (vraies photos uniquement)**

24. Portrait du Dr Stopek. Photo en consultation.
25. Façade et entrée du cabinet, salle d'attente, salle d'examen. Équipe, avec accord des personnes.
26. Photos des cliniques et des centres laser, si les établissements l'autorisent.
27. Fonds d'œil réels pour la page diabète (déjà sur le site actuel : confirmer les droits).
28. Vidéo ou courte présentation filmée du Dr Stopek pour l'accueil (facultatif).

**Validation**

29. Pouvez-vous relire chaque texte marqué `[ADAPTÉ]` et chaque réponse médicale reprise telle quelle ?
30. Acceptez-vous de retirer le bloc « diabète » des pages qui ne parlent pas de diabète ?
