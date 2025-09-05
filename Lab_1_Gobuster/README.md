# Cybersecurity
# 🕵️‍♀️ Home Lab_1  Gobuster 

## 🎯 Objectif
Mettre en place un **home lab de cybersécurité** pour apprendre à découvrir des répertoires cachés d’un site web à l’aide de **Gobuster**.

## 🛠️ Environnement
- **VirtualBox** – gestionnaire de VM  
- **Ubuntu Server 22.04** – machine cible (hébergeant Apache + répertoires cachés)  
- **Kali Linux** – machine attaquante (exécution de Gobuster)  

## ⚙️ Étapes principales
1. **Installation d’Ubuntu Server**  
   - Téléchargement de l’ISO depuis [ubuntu.com](https://ubuntu.com/download/server).  
   - Configuration minimale :  
     - RAM : 2–4 Go  
     - CPU : 2 cœurs  
     - Disque : 20–30 Go  
   - Partitionnement avec LVM activé.  

2. **Configuration réseau**  
   - Problème initial : Kali ne voyait pas Ubuntu en mode NAT.  
   - Solution : ajout d’un **Adapter 2 en Host-only** sur les deux VMs.  
   - Attribution d’une IP avec `dhclient` et configuration via Netplan.  
   - Vérification de la connectivité avec `ping`.  

3. **Test avec Gobuster**  
   - Commande utilisée :  
     ```bash
     gobuster dir -u http://<IP_Ubuntu> -w /usr/share/wordlists/dirb/common.txt
     ```  
   - Résultats : découverte de répertoires avec différents codes (200, 301, 403).  

## 📑 Résultats et apprentissages
- Compréhension du rôle des **wordlists** dans la reconnaissance web.  
- Interprétation des codes HTTP :  
  - **200** → accessible  
  - **301** → redirection (souvent ajout du `/`)  
  - **403** → interdit  
  - **404** → inexistant  
- Importance de la configuration réseau dans VirtualBox (NAT vs Host-only).  
- Notion de légalité : ⚠️ **Gobuster ne doit être utilisé que sur ses propres systèmes ou avec autorisation.**

## 📂 Documentation complète
📄 Le rapport détaillé (avec captures d’écran et explications étape par étape) est disponible ici :  
👉 [cybersecurity-homelab_01_gobuster]([Lab_1_Gobuster/cybersecurity-homelab_01_gobuster_biffé.pdf](https://github.com/Cyberjanie/Cybersecurity/blob/main/Lab_1_Gobuster/cybersecurity-homelab_01_gobuster_biff%C3%A9.pdf))

## ✅ Conclusion
Ce premier lab a permis de :  
- Construire un environnement d’attaque/défense réaliste.  
- Mettre en pratique un scan de répertoires web.  
- Apprendre à documenter les difficultés et solutions rencontrées.  

---

👩‍💻 *Projet réalisé dans le cadre de mon apprentissage en cybersécurité.*  
