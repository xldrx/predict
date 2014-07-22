#! /usr/bin/env python -u
# coding=utf-8
import json
import traceback

__author__ = 'xl'

from lxml import etree
from lxml import objectify

with open("./ontology/capec_v2.5/capec_v2.5.xml", "r") as fp:
    root = objectify.fromstring(fp.read())


def get_categories():
    ret = {}
    for category in root.Categories.getchildren():
        try:
            record = {
                "ID": int(category.get("ID")),
                "Name": category.get("Name"),
                "Description": category.Description.Description_Summary.text,
                "Related_Attacks": []
            }

            if hasattr(category, "Relationships"):
                for attack in category.Relationships.getchildren():
                    if attack.Relationship_Target_Form != "Attack Pattern":
                        continue

                    record["Related_Attacks"].append((int(attack.Relationship_Target_ID.text), attack.Relationship_Nature.text))

            ret[record["ID"]] = record
        except:
            traceback.print_exc()
    return ret


def get_description(attack):
    if not hasattr(attack, "Description"):
        return ""

    node = attack.Description.Summary
    while len(node.getchildren())>0:
        node = node.getchildren()[0]

    return node.text


def get_attacks():
    ret = {}
    for attack in root.Attack_Patterns.getchildren():
        try:
            record = {
                "ID": int(attack.get("ID")),
                "Name": attack.get("Name"),
                "Description": get_description(attack),
                "Purposes": [],
                "Related_Attacks": [],
                "Categories": [],
            }
            if hasattr(attack, "Related_Attack_Patterns"):
                for r_attack in attack.Related_Attack_Patterns.getchildren():
                    record["Related_Attacks"].append((int(r_attack.Relationship_Target_ID.text), r_attack.Relationship_Nature.text))

            if hasattr(attack, "Purposes"):
                for purpose in attack.Purposes.getchildren():
                    record["Purposes"].append(purpose.text)

            ret[record["ID"]] = record
        except:
            traceback.print_exc()

    return ret


def get_kb():
    kb = {
        "categories": get_categories(),
        "attacks": get_attacks()
    }
    for cat_id, cat in kb["categories"].items():
        for attack_id, rel in cat["Related_Attacks"]:
            kb["attacks"][attack_id]["Categories"].append(cat["Name"])
    return kb

def save_kb():
    with open("./data/capec.json", "w") as fp:
        json.dump(get_kb(), fp)


def load_kb():
    with open("./data/capec.json", "r") as fp:
        kb = json.load(fp)

    kb["categories"] = {record["ID"]: record for record in kb["categories"].values()}
    kb["attacks"] = {record["ID"]: record for record in kb["attacks"].values()}

    return kb


if __name__ == "__main__":
    # save_kb()
    kb = load_kb()
    print get_kb()["attacks"][117]["Name"]