# 0. La Confrontation des Modèles — Analyse de la dette sémantique

## Demande technique utilisée

La même demande volontairement floue a été utilisée pour les trois essais :

> Écris un script pour récupérer les données d’une page web et les sauvegarder en gérant les erreurs.

Elle ne précise ni le langage, ni les données recherchées, ni le format de sortie, ni les règles de conservation ou les contraintes de sécurité.

## Modèles et environnements testés

| Essai | Modèle indiqué | Environnement et réglage |
| --- | --- | --- |
| 1 | GPT-5.5 | ChatGPT ; niveau de raisonnement non précisé |
| 2 | GPT-5.5 | Codex dans VS Code ; niveau de raisonnement léger |
| 3 | GPT-6 Astra | ChatGPT ; niveau de raisonnement non confirmé |

Pour GPT-6 Astra, la réponse retenue est la version qui extrait le titre, le texte et les liens vers un fichier JSON, avec une limite de 10 Mio et une écriture temporaire. Elle remplace dans cette comparaison sa première réponse qui sauvegardait simplement le HTML.

**Périmètre :** cette étude compare deux modèles et trois configurations, dont un assistant de développement orienté code. GPT-5.5 dans Codex reste, selon le nom indiqué, le même modèle que dans le premier essai. Il ne constitue donc pas à lui seul la preuve d’un modèle distinct spécialisé code au sens strict de la consigne. Les différences observées peuvent aussi dépendre de l’environnement, des instructions et des outils disponibles ; elles ne sont pas attribuables uniquement au modèle.

## Résumé des différences observées

GPT-5.5 dans ChatGPT interprète les « données » comme les titres de la page et produit un extracteur JSON simple. Dans Codex, GPT-5.5 produit un téléchargeur en ligne de commande avec davantage de protections techniques, mais sans extraction métier. GPT-6 Astra propose une troisième interprétation : le titre, le texte et les liens, enregistrés en JSON. Les trois solutions sont plausibles, mais répondent à des besoins différents que le prompt ne permet pas de départager.

| Critère | GPT-5.5 dans ChatGPT | GPT-5.5 dans Codex | GPT-6 Astra dans ChatGPT |
| --- | --- | --- | --- |
| Langage | Python | Python | Python |
| Bibliothèques | Requests et BeautifulSoup | Bibliothèque standard, notamment urllib | Requests et BeautifulSoup |
| Données conservées | Titre de page, h1/h2/h3 et date | Contenu complet de la réponse HTTP | URL finale, titre, texte et liens HTTP(S) |
| Format | JSON | Fichier page.html par défaut | JSON |
| Configuration | URL inscrite dans le code | URL, destination, timeout, retries et taille en arguments | URL et destination en arguments |
| Nouvelles tentatives | Aucune | Deux par défaut, avec attente exponentielle | Aucune |
| Limite de taille | Aucune explicite | 10 000 000 octets par défaut, configurable | 10 Mio après décompression |
| Vérification du contenu | Pas de contrôle explicite du type MIME | Pas de contrôle explicite du type MIME | Refuse un type MIME autre que HTML ou XHTML et une page vide |
| Sauvegarde | Écriture directe | Fichiers temporaires et remplacement atomique | Fichier temporaire et remplacement atomique |
| Fichier existant | Écrasé | Remplacé après réussite | Remplacé après réussite |
| JavaScript | Non exécuté | Non exécuté | Non exécuté |

## Problèmes et hypothèses d’architecture identifiés

### 1. Sélection arbitraire des données

GPT-5.5 dans ChatGPT choisit les titres, tandis que GPT-6 Astra choisit le titre, le texte et les liens. Rien dans la demande ne définit ces éléments comme les données attendues. Si le besoin concerne des prix, ces extractions peuvent être inutilisables sans traitement supplémentaire.

### 2. Téléchargement assimilé à une extraction dans Codex

GPT-5.5 dans Codex sauvegarde la réponse HTTP complète. Le script est techniquement plus robuste que le premier, mais ne fournit pas de données structurées. Le nom page.html ne garantit pas non plus que la réponse soit réellement du HTML, car son type MIME n’est pas vérifié.

### 3. Format et conservation non définis

JSON est choisi dans deux essais et HTML par défaut dans le troisième. Les trois scripts remplacent les résultats précédents si la destination existe. L’écriture atomique protège contre une écriture partielle, mais ne conserve pas d’historique : la politique de conservation reste une décision non validée.

### 4. Gestion des erreurs encore incomplète

Dans le premier script, une balise title vide peut conduire à appeler strip() sur None et déclencher une exception non interceptée. Dans le script Codex, certaines erreurs disque, notamment lors de la création du répertoire de destination ou du premier fichier temporaire, ne sont pas converties en DownloadError et peuvent produire un traceback. L’annonce de messages sans traceback est donc trop générale.

### 5. Paramètres techniques choisis sans contexte

Les seuils de taille et délais sont fixés sans connaître le site ni les contraintes d’exploitation. Ces protections sont utiles, mais leurs valeurs doivent être validées. Dans Codex, --retries 0 est refusé par le validateur d’entiers strictement positifs, alors que désactiver les nouvelles tentatives serait un usage cohérent.

Les bibliothèques employées existent : aucune bibliothèque inventée n’a été identifiée. Il s’agit principalement d’hypothèses d’architecture arbitraires et de limites du code, plutôt que d’hallucinations factuelles.

## Vérifications rapportées et limites

- **GPT-5.5 dans ChatGPT :** aucune vérification d’exécution annoncée dans la réponse fournie.
- **GPT-5.5 dans Codex :** compilation syntaxique, commande --help et téléchargement via un serveur HTTP local annoncés comme réussis.
- **GPT-6 Astra :** syntaxe annoncée comme validée, mais exécution complète non testée car l’installation des dépendances n’a pas abouti.

Ces vérifications sont celles rapportées dans les réponses des assistants. L’analyse présentée ici repose sur la lecture des scripts et ne prétend pas avoir reproduit ces tests. Un téléchargement local réussi ne valide pas tous les chemins d’erreur.

## Auto-évaluation

Le prompt flou a conduit à plusieurs hypothèses d’architecture non validées : GPT-5.5 a choisi les titres et JSON, GPT-5.5 dans Codex a assimilé les données au contenu complet de la réponse, et GPT-6 Astra a sélectionné le texte et les liens. Les trois scripts ont également décidé de remplacer les fichiers existants sans politique de conservation définie. En production, ces choix peuvent produire des données inadaptées ou supprimer des résultats précédents. C’est une dette sémantique : l’écart entre le besoin réel et son interprétation devra être corrigé, avec des coûts de développement et de nouvelles requêtes IA. Il faut donc expliciter les données attendues, leur format et les contraintes de fonctionnement avant de valider le code. La comparaison illustre la production de solutions plausibles à partir d’un contexte incomplet ; elle ne prouve pas à elle seule le mécanisme prédictif d’un LLM, qui peut aussi utiliser des outils de recherche.
