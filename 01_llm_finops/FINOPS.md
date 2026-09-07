# FINOPS — Mesures, calculs et réflexion

## 1. Mesure du prompt

Le prompt de documentation JSDoc fourni dans l’exercice représente **75 tokens**, selon la capture de l’outil OpenAI Tokenizer, avec l’onglet **GPT-5.x & O1/3** sélectionné.

## 2. Coût d’une exécution

Tarifs utilisés : **5 $ par million de tokens d’entrée** et **15 $ par million de tokens de sortie**, conformément à l’exemple de l’énoncé.

```text
Entrée : 75 tokens de prompt + 15 000 tokens de code = 15 075 tokens
Sortie : 500 tokens

Coût entrée = 15 075 × 5 / 1 000 000 = 0,075375 $
Coût sortie = 500 × 15 / 1 000 000 = 0,007500 $

Coût total = 0,082875 $
```

## 3. Coût de dix itérations avec historique

Hypothèse : dix appels au total. Chaque appel conserve le prompt, le code et les réponses précédentes de 500 tokens. Aucun volume supplémentaire de message d’erreur n’étant fourni, il n’est pas comptabilisé. Les tarifs sont appliqués sans remise de cache.

```text
Entrée à l’itération i = 15 075 + 500 × (i − 1)
```

| Itération | Tokens d’entrée | Tokens de sortie | Coût de l’appel ($) |
| --- | --- | --- | --- |
| 1 | 15 075 | 500 | 0,082875 |
| 2 | 15 575 | 500 | 0,085375 |
| 3 | 16 075 | 500 | 0,087875 |
| 4 | 16 575 | 500 | 0,090375 |
| 5 | 17 075 | 500 | 0,092875 |
| 6 | 17 575 | 500 | 0,095375 |
| 7 | 18 075 | 500 | 0,097875 |
| 8 | 18 575 | 500 | 0,100375 |
| 9 | 19 075 | 500 | 0,102875 |
| 10 | 19 575 | 500 | 0,105375 |

```text
Total entrée = 10 × 15 075 + 500 × (0 + 1 + ... + 9)
             = 173 250 tokens
Total sortie = 10 × 500 = 5 000 tokens

Coût total = (173 250 × 5 + 5 000 × 15) / 1 000 000
           = 0,941250 $
```

**Précision mathématique :** malgré le terme « exponentiel » employé dans l’énoncé, ajouter 500 tokens à chaque tour produit une croissance linéaire du contexte et quadratique du coût cumulé. Pour n appels :

```text
Coût(n) = 0,082875 × n + 0,00125 × n × (n − 1) $
```

## 4. Coût mensuel

La fréquence n’est pas précisée. On suppose **une boucle de dix appels par jour pendant trente jours**, avec un nouvel historique chaque jour.

```text
Coût mensuel = 30 × 0,941250 = 28,2375 $
```

Soit **28,24 $ par mois**, après arrondi au centime. Ce montant inclut la croissance du contexte au sein de chaque boucle.

## 5. Auto-évaluation et optimisation

Le calcul distingue les tokens d’entrée et de sortie et inclut les réponses précédentes réinjectées dans le contexte : elles ajoutent 22 500 tokens d’entrée sur dix appels. Le coût mensuel est de 28,2375 $ pour trente boucles indépendantes. Pour réduire ce coût, on peut tronquer les anciennes réponses inutiles en conservant les instructions, le code et le dernier diagnostic nécessaire. Il faut préserver les informations utiles à la correction et comptabiliser les tokens du diagnostic conservé.
