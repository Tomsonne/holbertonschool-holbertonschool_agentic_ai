# MCP Setup

## Serveur MCP configuré

Le serveur MCP configuré dans le workspace est :

`crm-server`

Il est exécuté localement avec Node.js et utilise le transport `stdio`.

## Tool CRM détecté

Le Tool CRM détecté par GitHub Copilot est :

`get_customer_status`

Ce Tool permet de récupérer le statut d'un client et de sa commande à partir de son adresse e-mail.

## Vérification

La connexion entre GitHub Copilot et le serveur MCP a été vérifiée avec succès.

Lors de la demande :

"Quels sont les outils externes (MCP) auxquels tu as accès ?"

Copilot a identifié le serveur `crm-server` ainsi que le Tool `get_customer_status`.

Le serveur MCP est donc correctement chargé dans VS Code et son Tool est accessible depuis Copilot Chat.