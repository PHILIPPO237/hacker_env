# -*- coding: utf-8 -*-
"""
Module SETUP_TERMUX — préparation complète de l'environnement Termux.
Inspiré du style hacker_env.py : couleurs, animations, journalisation.
"""

import os
import sys
import shutil
from datetime import datetime

from core.colors import NeonTheme, default_theme
from core.effects import (
    clear, typewrite, scanline, print_title_neon, print_end_neon,
    print_success, print_warn, print_error, print_info, spinner, stop_spinner,
    glitch_text, rainbow_line, pulse_text
)
from core.system import (
    run_cmd, install_pkg, is_pkg_installed, check_internet, check_space, check_os
)


class TermuxSetup:
    """Prépare automatiquement l'environnement Termux pour un nouvel utilisateur."""

    ESSENTIAL_PACKAGES = [
        "python", "git", "curl", "wget", "zsh", "nano", "vim",
        "zip", "unzip", "tar", "tree", "jq", "openssh",
        "clang", "make", "cmake", "rust", "nodejs",
        "proot", "proot-distro", "htop", "neofetch", "openssl-tool"
    ]

    PYTHON_LIBS = [
        "requests", "rich", "colorama", "psutil"
    ]

    # Paquets connus pour être lourds à installer
    HEAVY_PACKAGES = {"cmake", "rust", "nodejs", "proot", "proot-distro"}

    def __init__(self, theme=None, log_dir=None):
        self.theme = theme or default_theme
        self.log_dir = log_dir or os.path.expanduser("~/.termux-hacker-env/logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(
            self.log_dir, f"setup-{datetime.now():%Y%m%d_%H%M%S}.log"
        )
        self.missing_packages = []
        self.installed_packages = []

    # ─────────────────────────────────────────────────────────────────
    #  Journalisation
    # ─────────────────────────────────────────────────────────────────

    def _log(self, message):
        """Écrit dans le fichier de log."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────────────
    #  1. Connexion Internet
    # ─────────────────────────────────────────────────────────────────

    def _check_internet(self):
        """Vérifie la connexion Internet."""
        print_title_neon(
            "CONNEXION INTERNET", "Vérification réseau",
            self.theme.get("CYAN"), self.theme.get("BLUE"), self.theme
        )
        self._log("Vérification connexion Internet")

        if check_internet():
            print_success("Connexion Internet — OK")
            self._log("Internet OK")
            print_end_neon(self.theme.get("CYAN"), self.theme)
            return True
        else:
            print_error("Pas de connexion Internet détectée.")
            print_warn(
                "La préparation de Termux nécessite Internet pour télécharger les paquets."
            )
            self._log("Internet absent")
            print_end_neon(self.theme.get("CYAN"), self.theme)
            return False

    # ─────────────────────────────────────────────────────────────────
    #  2. Mise à jour Termux
    # ─────────────────────────────────────────────────────────────────

    def _update_termux(self):
        """Met à jour les dépôts et les paquets."""
        print_title_neon(
            "MISE À JOUR", "pkg update && pkg upgrade",
            self.theme.get("ORANGE"), self.theme.get("YELLOW"), self.theme
        )
        self._log("Mise à jour Termux")
        print_info("Cette opération peut prendre plusieurs minutes...", "⏳")

        # pkg update
        print(f"  {self.theme.get('CYAN')}➤  pkg update -y{self.theme.colors['RST']}")
        stop_flag, thread = spinner("Mise à jour des dépôts", self.theme.get("ORANGE"), self.theme)
        try:
            success, _, code = run_cmd(["pkg", "update", "-y"], timeout=300, silent=True)
            stop_spinner(stop_flag, thread)
            if success:
                print_success("Dépôts mis à jour")
                self._log("pkg update OK")
            else:
                print_warn(f"pkg update a retourné le code {code}")
                self._log(f"pkg update code {code}")
        except KeyboardInterrupt:
            stop_spinner(stop_flag, thread)
            print_warn("Interrompu par l'utilisateur.")
            raise
        except Exception as e:
            stop_spinner(stop_flag, thread)
            print_error(f"Erreur lors de pkg update : {str(e)}")
            self._log(f"Erreur pkg update: {e}")

        # pkg upgrade
        print(f"  {self.theme.get('CYAN')}➤  pkg upgrade -y{self.theme.colors['RST']}")
        stop_flag, thread = spinner("Upgrade des paquets", self.theme.get("ORANGE"), self.theme)
        try:
            success, _, code = run_cmd(["pkg", "upgrade", "-y"], timeout=300, silent=True)
            stop_spinner(stop_flag, thread)
            if success:
                print_success("Paquets mis à jour")
                self._log("pkg upgrade OK")
            else:
                print_warn(f"pkg upgrade a retourné le code {code}")
                self._log(f"pkg upgrade code {code}")
        except KeyboardInterrupt:
            stop_spinner(stop_flag, thread)
            print_warn("Interrompu par l'utilisateur.")
            raise
        except Exception as e:
            stop_spinner(stop_flag, thread)
            print_error(f"Erreur lors de pkg upgrade : {str(e)}")
            self._log(f"Erreur pkg upgrade: {e}")

        print_end_neon(self.theme.get("ORANGE"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  3. Installation des paquets essentiels
    # ─────────────────────────────────────────────────────────────────

    def _install_packages(self):
        """Installe uniquement les paquets absents."""
        print_title_neon(
            "PAQUETS ESSENTIELS", "Installation des outils de base",
            self.theme.get("GREEN"), self.theme.get("LIME"), self.theme
        )
        self._log("Installation paquets essentiels")

        self.missing_packages = []
        self.installed_packages = []

        for pkg in self.ESSENTIAL_PACKAGES:
            if is_pkg_installed(pkg):
                print_success(f"{pkg:20} — déjà installé")
                self.installed_packages.append(pkg)
                self._log(f"{pkg} déjà installé")
                continue

            print_info(f"{pkg:20} — installation...", "📦")
            self._log(f"Installation {pkg}")

            # Timeout adapté : 600s pour les paquets lourds, 300s sinon
            timeout = 600 if pkg in self.HEAVY_PACKAGES else 300
            stop_flag, thread = spinner(
                f"Installation {pkg}", self.theme.get("GREEN"), self.theme
            )
            try:
                success, _, code = run_cmd(
                    ["pkg", "install", "-y", pkg], timeout=timeout, silent=True
                )
                stop_spinner(stop_flag, thread)
                if success:
                    print_success(f"{pkg:20} — installé")
                    self.installed_packages.append(pkg)
                    self._log(f"{pkg} installé")
                else:
                    print_error(f"{pkg:20} — échec (code {code})")
                    self.missing_packages.append(pkg)
                    self._log(f"{pkg} échec code {code}")
            except KeyboardInterrupt:
                stop_spinner(stop_flag, thread)
                print_warn("Interrompu par l'utilisateur.")
                raise
            except Exception as e:
                stop_spinner(stop_flag, thread)
                print_error(f"{pkg:20} — erreur ({str(e)})")
                self.missing_packages.append(pkg)
                self._log(f"{pkg} erreur: {e}")

        print_end_neon(self.theme.get("GREEN"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  4. Configuration du stockage
    # ─────────────────────────────────────────────────────────────────

    def _setup_storage(self):
        """Lance termux-setup-storage si nécessaire."""
        print_title_neon(
            "STOCKAGE", "Configuration de l'accès Android",
            self.theme.get("PINK"), self.theme.get("PURPLE"), self.theme
        )
        self._log("Configuration stockage")

        storage_path = os.path.expanduser("~/storage")
        if os.path.exists(storage_path):
            print_success("Stockage déjà configuré (~/storage existe)")
            self._log("Stockage déjà configuré")
        else:
            print_warn("Le stockage externe n'est pas encore configuré.")
            print_info("Une autorisation Android va être demandée.", "📱")
            print_info(
                "Accepte-la pour permettre à Termux d'accéder à tes fichiers.", "💡"
            )
            input(
                f"  {self.theme.get('CYAN')}➤  Appuie sur Entrée pour lancer termux-setup-storage...{self.theme.colors['RST']}"
            )
            try:
                success, out, code = run_cmd(
                    ["termux-setup-storage"], timeout=300, silent=False
                )
                if success:
                    print_success("Stockage configuré avec succès")
                    self._log("termux-setup-storage OK")
                else:
                    print_warn("termux-setup-storage a terminé avec un code non nul")
                    self._log(f"termux-setup-storage code {code}")
            except KeyboardInterrupt:
                print_warn("Interrompu.")
                raise
            except Exception as e:
                print_error(f"Erreur : {str(e)}")
                self._log(f"Erreur termux-setup-storage: {e}")

        print_end_neon(self.theme.get("PINK"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  5. Vérification des outils
    # ─────────────────────────────────────────────────────────────────

    def _verify_tools(self):
        """Contrôle la présence des outils clés."""
        print_title_neon(
            "VÉRIFICATION DES OUTILS", "Contrôle de présence",
            self.theme.get("YELLOW"), self.theme.get("GOLD"), self.theme
        )
        self._log("Vérification outils")

        tools = [
            ("python", ["python", "--version"]),
            ("pip", ["pip", "--version"]),
            ("git", ["git", "--version"]),
            ("curl", ["curl", "--version"]),
            ("wget", ["wget", "--version"]),
            ("zsh", ["zsh", "--version"]),
            ("rustc", ["rustc", "--version"]),
            ("node", ["node", "--version"]),
        ]

        for name, cmd in tools:
            try:
                success, out, _ = run_cmd(cmd, capture_output=True, timeout=10)
                if success and out.strip():
                    print_success(f"{name:10} — ✓ Installé  ({out.strip()})")
                    self._log(f"{name} OK: {out.strip()}")
                else:
                    print_error(f"{name:10} — ✗ Absent")
                    self._log(f"{name} absent")
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print_error(f"{name:10} — ✗ Erreur ({str(e)})")
                self._log(f"{name} erreur: {e}")

        print_end_neon(self.theme.get("YELLOW"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  6. Installation des bibliothèques Python
    # ─────────────────────────────────────────────────────────────────

    def _install_python_libs(self):
        """Met pip à jour et installe les bibliothèques manquantes."""
        print_title_neon(
            "BIBLIOTHÈQUES PYTHON", "Mise à jour de pip et installation",
            self.theme.get("BLUE"), self.theme.get("CYAN"), self.theme
        )
        self._log("Installation bibliothèques Python")

        # Mise à jour de pip (via python -m pip pour fiabilité)
        print_info("Mise à jour de pip...", "⬆️")
        self._log("Mise à jour pip")
        stop_flag, thread = spinner("Upgrade pip", self.theme.get("BLUE"), self.theme)
        try:
            success, _, _ = run_cmd(
                ["python", "-m", "pip", "install", "--upgrade", "pip"], timeout=180, silent=True
            )
            stop_spinner(stop_flag, thread)
            if success:
                print_success("pip mis à jour")
                self._log("pip upgrade OK")
            else:
                print_warn("Échec de la mise à jour de pip")
                self._log("pip upgrade échec")
        except KeyboardInterrupt:
            stop_spinner(stop_flag, thread)
            raise
        except Exception as e:
            stop_spinner(stop_flag, thread)
            print_error(f"Erreur pip upgrade : {str(e)}")
            self._log(f"Erreur pip upgrade: {e}")

        # Installation des libs
        for lib in self.PYTHON_LIBS:
            check_cmd = ["python", "-c", f"import {lib}"]
            try:
                success, _, _ = run_cmd(check_cmd, timeout=10, silent=True)
                if success:
                    print_success(f"{lib:15} — déjà installé")
                    self._log(f"{lib} déjà installé")
                    continue
            except KeyboardInterrupt:
                raise
            except Exception:
                pass

            print_info(f"{lib:15} — installation...", "📦")
            self._log(f"Installation {lib}")
            stop_flag, thread = spinner(
                f"Installation {lib}", self.theme.get("BLUE"), self.theme
            )
            try:
                success, _, _ = run_cmd(
                    ["python", "-m", "pip", "install", lib], timeout=180, silent=True
                )
                stop_spinner(stop_flag, thread)
                if success:
                    print_success(f"{lib:15} — installé")
                    self._log(f"{lib} installé")
                else:
                    print_error(f"{lib:15} — échec")
                    self._log(f"{lib} échec")
                    if lib == "psutil":
                        print_warn("psutil nécessite souvent clang et les headers Python.")
                        print_info("Essaye : pkg install clang python", "💡")
            except KeyboardInterrupt:
                stop_spinner(stop_flag, thread)
                raise
            except Exception as e:
                stop_spinner(stop_flag, thread)
                print_error(f"Erreur {lib} : {str(e)}")
                self._log(f"Erreur {lib}: {e}")

        print_end_neon(self.theme.get("BLUE"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  7. Diagnostic complet
    # ─────────────────────────────────────────────────────────────────

    def _get_missing_essential(self):
        """Retourne la liste des paquets essentiels manquants."""
        return [p for p in self.ESSENTIAL_PACKAGES if not is_pkg_installed(p)]

    def _diagnostic(self):
        """Affiche un rapport système complet et coloré."""
        print_title_neon(
            "DIAGNOSTIC COMPLET", "Rapport système Termux",
            self.theme.get("PURPLE"), self.theme.get("PINK"), self.theme
        )
        self._log("Diagnostic complet")

        try:
            # Collecte des informations
            android_ver = "n/a"
            success, out, _ = run_cmd(
                ["getprop", "ro.build.version.release"], capture_output=True, timeout=5
            )
            if success:
                android_ver = out.strip()

            arch = "n/a"
            success, out, _ = run_cmd(["uname", "-m"], capture_output=True, timeout=5)
            if success:
                arch = out.strip()

            py_ver = "n/a"
            success, out, _ = run_cmd(["python", "--version"], capture_output=True, timeout=5)
            if success:
                py_ver = out.strip()

            git_ver = "n/a"
            success, out, _ = run_cmd(["git", "--version"], capture_output=True, timeout=5)
            if success:
                git_ver = out.strip()

            pip_ver = "n/a"
            success, out, _ = run_cmd(["pip", "--version"], capture_output=True, timeout=5)
            if success:
                pip_ver = out.strip()

            # RAM
            ram = "n/a"
            success, out, _ = run_cmd(
                ["sh", "-c", "free -h | awk '/^Mem:/ {print $3\"/\"$2}'"],
                capture_output=True, timeout=5,
            )
            if success and out.strip():
                ram = out.strip()
            else:
                success, out, _ = run_cmd(
                    ["sh", "-c", "awk '/MemTotal/ {print int($2/1024)\"M\"}' /proc/meminfo"],
                    capture_output=True, timeout=5,
                )
                if success:
                    memtotal = out.strip()
                    success, out, _ = run_cmd(
                        ["sh", "-c", "awk '/MemAvailable/ {print int($2/1024)\"M\"}' /proc/meminfo"],
                        capture_output=True, timeout=5,
                    )
                    if success:
                        ram = f"{out.strip()}/{memtotal}"

            # Disk (calcul en Python pur, plus de shell/awk fragile ici)
            home = os.path.expanduser("~")
            try:
                total, used, free = shutil.disk_usage(home)
                gi = 1024 ** 3
                disk = f"{used // gi}G/{total // gi}G (dispo {free // gi}G)"
            except Exception:
                disk = "n/a"

            net = "✅ Connecté" if check_internet() else "❌ Hors ligne"
            storage = (
                "✅ Configuré"
                if os.path.exists(os.path.expanduser("~/storage"))
                else "❌ Non configuré"
            )

            success, out, _ = run_cmd(
                ["sh", "-c", "dpkg -l | awk 'NR>5 {print $2}'"], capture_output=True, timeout=10
            )
            installed = out.strip().splitlines() if success else []

            missing = (
                self.missing_packages
                if self.missing_packages
                else self._get_missing_essential()
            )

            # Affichage
            c1 = self.theme.get("CYAN", True)
            c2 = self.theme.get("GREEN", True)
            rst = self.theme.colors["RST"]

            print(f"  {c1}📱 Version Android :{rst}  {android_ver}")
            print(f"  {c1}🏗️  Architecture    :{rst}  {arch}")
            print(f"  {c1}🐍 Python          :{rst}  {py_ver}")
            print(f"  {c1}📦 Git             :{rst}  {git_ver}")
            print(f"  {c1}📥 Pip             :{rst}  {pip_ver}")
            print(f"  {c1}🧠 RAM             :{rst}  {ram}")
            print(f"  {c1}💾 Stockage        :{rst}  {disk}")
            print(f"  {c1}🌐 Internet        :{rst}  {net}")
            print(f"  {c1}📂 Stockage Termux :{rst}  {storage}")
            print()

            if installed:
                print(f"  {c2}✓ Paquets installés ({len(installed)}):{rst}")
                cols = 3
                display = installed[:30]
                for i in range(0, len(display), cols):
                    row = display[i : i + cols]
                    print("     " + "  ".join(f"{p:20}" for p in row))
                if len(installed) > 30:
                    print(f"     ... et {len(installed) - 30} autres")
            else:
                print(f"  {self.theme.get('RED', True)}✗ Impossible de lister les paquets{rst}")

            print()
            if missing:
                print(f"  {self.theme.get('RED', True)}✗ Paquets manquants ({len(missing)}):{rst}")
                for p in missing:
                    print(f"     - {p}")
            else:
                print(f"  {c2}✓ Aucun paquet essentiel manquant !{rst}")

            self._log(
                f"Diagnostic: Android={android_ver}, Arch={arch}, Python={py_ver}, "
                f"RAM={ram}, Disk={disk}, Net={net}"
            )
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print_error(f"Erreur lors du diagnostic : {str(e)}")
            self._log(f"Erreur diagnostic: {e}")

        print_end_neon(self.theme.get("PURPLE"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  8. Réparation automatique
    # ─────────────────────────────────────────────────────────────────

    def _repair(self):
        """Nettoie le cache, corrige les dépendances et réinstalle les paquets manquants."""
        print_title_neon(
            "RÉPARATION AUTOMATIQUE", "Nettoyage et correction",
            self.theme.get("ORANGE"), self.theme.get("RED"), self.theme
        )
        self._log("Réparation automatique")

        # Nettoyage cache
        print_info("Nettoyage du cache des paquets...", "🧹")
        self._log("Nettoyage cache")
        try:
            run_cmd(["pkg", "clean"], timeout=30, silent=True)
            print_success("Cache nettoyé")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print_warn(f"Impossible de nettoyer le cache : {str(e)}")
            self._log(f"Erreur pkg clean: {e}")

        # Correction dépendances
        print_info("Correction des dépendances...", "🔧")
        self._log("Correction dépendances")
        stop_flag, thread = spinner(
            "Fix broken packages", self.theme.get("ORANGE"), self.theme
        )
        try:
            success, _, _ = run_cmd(
                ["apt", "--fix-broken", "install", "-y"], timeout=180, silent=True
            )
            stop_spinner(stop_flag, thread)
            if success:
                print_success("Dépendances corrigées")
                self._log("apt fix-broken OK")
            else:
                print_warn("Échec de la correction des dépendances")
                self._log("apt fix-broken échec")
        except KeyboardInterrupt:
            stop_spinner(stop_flag, thread)
            raise
        except Exception as e:
            stop_spinner(stop_flag, thread)
            print_error(f"Erreur : {str(e)}")
            self._log(f"Erreur apt fix-broken: {e}")

        # Réinstallation paquets manquants
        missing = self._get_missing_essential()
        if missing:
            print_info(
                f"Réinstallation de {len(missing)} paquet(s) manquant(s)...", "📦"
            )
            self._log(f"Réinstallation {missing}")
            for pkg in missing:
                print_info(f"Réinstallation de {pkg}...", "🔄")
                if install_pkg(pkg, auto_yes=True):
                    print_success(f"{pkg} réinstallé")
                    self._log(f"{pkg} réinstallé")
                else:
                    print_error(f"Échec réinstallation {pkg}")
                    self._log(f"{pkg} réinstall échec")
        else:
            print_success("Tous les paquets essentiels sont présents")

        print_end_neon(self.theme.get("ORANGE"), self.theme)

    # ─────────────────────────────────────────────────────────────────
    #  Orchestration
    # ─────────────────────────────────────────────────────────────────

    def run(self):
        """Exécute la préparation complète de Termux."""
        clear()
        rainbow_line("  ═══════════════════════════════════════════════", self.theme)
        glitch_text("  PRÉPARATION DE TERMUX", self.theme.get("PINK", True))
        scanline("█", self.theme.get("CYAN"), self.theme)
        print()

        # Étape 1 : Internet
        if not self._check_internet():
            print_error("Préparation annulée : connexion Internet requise.")
            return False

        # Étape 2 : Mise à jour
        self._update_termux()

        # Étape 3 : Paquets essentiels
        self._install_packages()

        # Étape 4 : Stockage
        self._setup_storage()

        # Étape 5 : Vérification outils
        self._verify_tools()

        # Étape 6 : Libs Python
        self._install_python_libs()

        # Étape 7 : Diagnostic
        self._diagnostic()

        # Étape 8 : Réparation (optionnelle)
        print()
        ans = input(
            f"  {self.theme.get('CYAN')}➤  Lancer la réparation automatique ? (O/n) [n] : {self.theme.colors['RST']}"
        ).strip().lower()
        if ans in ("o", "y", "oui", "yes"):
            self._repair()

        # Rapport final
        print()
        rainbow_line("  ═══════════════════════════════════════════════", self.theme)
        print_success("Préparation de Termux terminée !")
        print_info(f"Log : {self.log_file}", "📝")
        print()

        return True

    def run_repair(self):
        """Exécute uniquement la réparation automatique."""
        clear()
        rainbow_line("  ═══════════════════════════════════════════════", self.theme)
        glitch_text("  RÉPARATION AUTOMATIQUE", self.theme.get("ORANGE", True))
        scanline("█", self.theme.get("RED"), self.theme)
        print()

        self._repair()
        self._diagnostic()

        print()
        print_success("Réparation terminée !")
        print_info(f"Log : {self.log_file}", "📝")
        print()
