# -*- coding: utf-8 -*-
"""
Module GUIDE — assistant guidé pour l'installateur.

Ajoute deux choses au-dessus des simples input() :
  1. Une aide contextuelle : taper "?" à n'importe quelle question
     affiche une explication puis repose la question (au lieu de la
     traiter comme une réponse invalide).
  2. Un fil d'Ariane visible : "Étape 3/7 · Choix du prompt" affiché
     avant chaque étape, avec les choix déjà faits en rappel.
"""


class Guide:
    def __init__(self, theme, total_steps):
        self.theme = theme
        self.total_steps = total_steps
        self.current_step = 0
        self.trail = []  # [(label, valeur_choisie), ...]

    def remember(self, label, value):
        """Ajoute un choix au fil d'Ariane (affiché dans les étapes suivantes)."""
        self.trail.append((label, value))

    def step(self, label):
        """Affiche le repère d'étape + le fil d'Ariane, avant le contenu de l'étape."""
        self.current_step += 1
        t = self.theme
        bar_len = 20
        filled = int(bar_len * self.current_step / self.total_steps)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(
            f"\n  {t.get('DIM')}{t.colors['DIM']}"
            f"{t.get('primary', True)}[{bar}]{t.colors['RST']} "
            f"{t.colors['DIM']}Étape {self.current_step}/{self.total_steps} · {t.colors['RST']}"
            f"{t.get('secondary', True)}{label}{t.colors['RST']}"
        )
        if self.trail:
            recap = "  ".join(f"{lbl}: {val}" for lbl, val in self.trail[-3:])
            print(f"  {t.colors['DIM']}déjà choisi → {recap}{t.colors['RST']}")

    def ask(self, prompt, default=None, help_text=None, validator=None, choices=None):
        """
        Pose une question avec support de "?" pour l'aide contextuelle.

        Args:
            prompt: texte affiché avant la saisie (sans les [ ] par défaut)
            default: valeur renvoyée si l'utilisateur appuie juste sur Entrée
            help_text: texte affiché si l'utilisateur tape "?"
            validator: fonction(str) -> bool, réponse invalide sinon
            choices: liste optionnelle de réponses valides (raccourci à validator)
        """
        t = self.theme
        hint = " [?=aide]" if help_text else ""
        default_hint = f" [{default}]" if default is not None else ""
        while True:
            raw = input(f"  {t.get('CYAN')}➤  {prompt}{default_hint}{hint} : {t.colors['RST']}").strip()

            if raw == "?":
                if help_text:
                    print(f"  {t.get('GOLD')}💡 {help_text}{t.colors['RST']}")
                else:
                    print(f"  {t.get('DIM')}Pas d'aide supplémentaire pour cette question.{t.colors['RST']}")
                continue

            if not raw and default is not None:
                return default

            if choices and raw not in choices:
                print(f"  {t.get('RED', True)}✖ Réponse invalide. Choix possibles : {', '.join(choices)}{t.colors['RST']}")
                continue

            if validator and not validator(raw):
                print(f"  {t.get('RED', True)}✖ Réponse invalide. Tape ? pour de l'aide.{t.colors['RST']}")
                continue

            return raw

    def ask_yes_no(self, prompt, default="o", help_text=None):
        raw = self.ask(prompt, default=default, help_text=help_text, choices=None,
                        validator=lambda r: r.lower() in ("o", "n", "y"))
        return raw.lower() in ("o", "y")
