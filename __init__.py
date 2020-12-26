#
# Credit goes to https://eshapard.github.io/
# Resets ease to given value all the time
#
# Updated for version 2.1.35 by dmg@uvic.ca
#
#
from anki.hooks import addHook
from aqt import gui_hooks
from anki import hooks
from aqt import mw

import types


def load_config():
    addonConfig = mw.addonManager.getConfig(__name__)
    if (addonConfig == None):
        addonConfig = {'defaults': {'defaultEase': 250, 'verbose': 0}}
    config = types.SimpleNamespace(**addonConfig['defaults'])
    # anki keeps the ease (factor) as 'permil', not 'percent'
    # but users specify percent
    config.defaultEasePerMil = config.defaultEase * 10
    return config

config = load_config()

def report_ease(reviewer, card, ease):
    if config.verbose:
        print("\nIn did answer review\n", card)
        
    assert card.factor == config.defaultEasePerMil
    return ease

def do_reset_ease_before(ease, reviewer, card):
    if (config.verbose and card.factor != config.defaultEasePerMil):
        print("\nReseting factor before review:\n ", card)
    card.factor = config.defaultEasePerMil
    return ease


def do_reset_ease_after(card, ease, early):
    if (config.verbose and card.factor != config.defaultEasePerMil):
        print("\nReseting factor in anki 2 sched:\n ", card)
    card.factor = config.defaultEasePerMil


gui_hooks.reviewer_did_answer_card.append(report_ease)

hooks.schedv2_did_answer_review_card.append(do_reset_ease_after)

gui_hooks.reviewer_will_answer_card.append(do_reset_ease_before)

