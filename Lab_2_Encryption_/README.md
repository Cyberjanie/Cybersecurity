# 🔐 Lab 2 – Encryption Algorithm

## 🎯 Objectif
Concevoir et tester un **algorithme de chiffrement symétrique** inspiré du fonctionnement de l’AES, afin de mieux comprendre les principes de substitution, permutation, clé de ronde et effet avalanche.

Ce projet s’inscrit dans le cadre de ma formation en **cybersécurité**. Il a pour but d’approfondir mes compétences en **cryptographie appliquée** et en **analyse de la diffusion** des bits lors du chiffrement.

---

## ⚙️ Description du projet
L’algorithme utilise :
- Un bloc de 128 bits (16 octets)
- Un chiffrement par rondes successives (12 rondes)
- Une **S-Box personnalisée**
- Des **sous-clés générées par XOR** avec la clé principale
- Des tests d’effet avalanche pour mesurer la sensibilité du système

Le code Python inclut une partie dédiée à la génération des sous-clés, au chiffrement bloc par bloc, et à l’analyse de la propagation des bits.

---

## 🧠 Ce que j’ai appris
- Structure interne d’un chiffrement symétrique
- Importance des S-Box dans la non-linéarité du chiffrement
- Conception d’un test d’effet avalanche pour mesurer la robustesse d’un algorithme
- Validation et documentation de résultats dans un rapport technique

---

## 📂 Contenu du dossier
- `encryption_algorithm.py` → Code source de l’algorithme  
- `rapport_encryption.pdf` → Rapport détaillé avec explications, schémas et résultats de tests  
- `README.md` → Présentation du lab

---

## 🧩 Prochaines étapes
- Implémenter une version avec **mode CBC** (Cipher Block Chaining)  
- Ajouter une **interface Flask** pour tester le chiffrement en ligne  
- Comparer les performances avec AES-128 (bibliothèque `pycryptodome`)

---

*Projet réalisé dans le cadre de mes études en cybersécurité au Collège Cumberland. Créé par Janie Sarrazin, Chloé Arseneault, Stacey Denis et Amélie Rivard.*

