# Revue de sécurité — Injection SQL

## Prompt utilisé

```text
Le connecteur db.query est simulé directement dans src/legacy_auth.js.
Tu peux adapter cette simulation dans ce fichier pour permettre une
requête paramétrée. Cette adaptation fait partie de la correction.

Modifie uniquement src/legacy_auth.js :

1. Fais accepter à db.query une chaîne SQL et un tableau de paramètres.
2. Dans authenticateUser, utilise une requête SQL fixe avec deux
   placeholders ? et transmets email et password séparément.
3. Dans le connecteur simulé, vérifie la requête attendue et compare
   les paramètres aux identifiants légitimes déjà présents.
   Ne reconstruis jamais une chaîne SQL à partir des paramètres.
   Les paramètres doivent rester des données, même s’ils contiennent
   des caractères SQL.
4. Supprime la branche simulant la réussite de l’injection.
   N’ajoute aucun filtrage spécial visant la chaîne du Test 2.
5. Conserve exactement :
   - la signature authenticateUser(email, password) ;
   - le comportement synchrone ;
   - les objets retournés en cas de succès et d’échec ;
   - les données de l’utilisateur légitime ;
   - module.exports.
6. Ne modifie pas test_security.js et n’ajoute aucune dépendance.

Exécute npm run test:security avant et après la correction.
Présente le diff et les résultats réels des deux tests.

Précise que le connecteur reste une simulation de paramétrisation,
 et non une requête préparée exécutée par un véritable moteur SQL.
```

## Vulnérabilité identifiée

Dans `src/legacy_auth.js`, la fonction `authenticateUser(email, password)` concaténait directement les entrées utilisateur dans la requête SQL. Une valeur comme `admin@entreprise.com' OR '1'='1` pouvait ainsi modifier la logique de la requête. Le connecteur simulé reproduisait cette vulnérabilité en retournant un utilisateur administrateur lors de la tentative d’injection.

## Modifications proposées et appliquées

L’Agent a remplacé la concaténation par la requête fixe `SELECT * FROM users WHERE email = ? AND password = ?` et l’appel `db.query(sql, [email, password])`. Le connecteur local accepte désormais un tableau de paramètres et vérifie séparément les identifiants légitimes, sans reconstruire de SQL. La branche simulant la réussite de l’injection a été supprimée.

Seul `src/legacy_auth.js` a été modifié. La signature de la fonction, son comportement synchrone, les objets retournés et l’export du module ont été conservés. Les tests n’ont pas été modifiés. Le connecteur reste une simulation de paramétrisation, sans exécution par un véritable moteur SQL.

## Résultats des tests avant et après

Commande utilisée :

```bash
npm run test:security
```

| Test | Avant correction | Après correction |
| --- | --- | --- |
| Test 1 : connexion légitime | Réussi | Réussi |
| Test 2 : tentative d’injection SQL | Échoué : l’injection réussissait | Réussi : la connexion malveillante est refusée |

Les résultats transmis par l’Agent confirment le passage des deux tests après correction et la préservation du comportement légitime dans cette simulation.
