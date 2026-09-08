# Le défi du contexte implicite et de l’architecture

## Prompt utilisé

```text
Analyse les fichiers joints :
- 02_context_engineering/src/repositories/user.repository.js
- 02_context_engineering/src/services/user.service.js

Crée un service d’export d’un utilisateur au format JSON dans :
02_context_engineering/src/services/user-export.service.js

Avant de générer le fichier, identifie le pattern d’accès au repository
et la gestion des exceptions utilisés dans user.service.js.

Le nouveau service doit :
- exposer une méthode async exportUserByEmail(email) ;
- utiliser la méthode existante findByEmail(email) du repository ;
- reproduire exactement l’import du repository et son mode d’appel ;
- reprendre la même vérification d’utilisateur absent et le même
  message d’erreur que user.service.js ;
- respecter la même propagation des exceptions ;
- suivre les mêmes conventions de nommage et d’export d’une instance ;
- retourner l’utilisateur sous forme de chaîne JSON, sans écrire sur disque.

Ne modifie pas les fichiers existants.
N’ajoute aucune dépendance ni méthode au repository.
N’accède pas directement à la base de données.

Crée le fichier et résume brièvement les éléments de l’architecture
existante repris dans le service.
```

## Fichiers fournis à Copilot comme contexte

Les deux fichiers suivants ont été joints à la demande dans Copilot Chat :

- `02_context_engineering/src/repositories/user.repository.js`
- `02_context_engineering/src/services/user.service.js`

## Service généré

- **Nom :** `user-export.service.js`
- **Chemin :** `02_context_engineering/src/services/user-export.service.js`
- **Méthode :** `async exportUserByEmail(email)`

## Architecture existante reprise

Le service importe directement le repository avec `require('../repositories/user.repository')` et appelle sa méthode synchrone `findByEmail(email)` depuis une méthode de service déclarée `async`. Il reprend la vérification `if (!user)` et l’exception `throw new Error("Utilisateur introuvable dans le système")`. Les exceptions sont propagées sans interception locale. Il conserve l’organisation en classe et l’export d’une instance avec `module.exports = new UserExportService()`. L’accès aux données reste délégué au repository ; le résultat est converti en chaîne JSON avec `JSON.stringify(user)`, sans écriture sur disque.
