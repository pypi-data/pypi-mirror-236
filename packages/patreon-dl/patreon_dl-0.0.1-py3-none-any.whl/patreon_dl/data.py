from collections import defaultdict
from copy import deepcopy
from typing import Any, TypedDict

Data = dict[str, Any]
Included = Data


class Key(TypedDict):
    id: str
    type: str


class Item(TypedDict):
    id: str
    type: str
    attributes: dict[str, Any]
    relationships: dict[str, "Item"]


# Item before processing
class RawItem(TypedDict):
    id: str
    type: str
    attributes: dict[str, Any]
    relationships: dict[str, "Item"]


class Relationships(TypedDict):
    data: Key | list[Key] | None


def reify_relationships_one(
    item: RawItem,
    included: Included,
    recur_keys: list[str] | None = None,
) -> Item:
    return do_reify_relationships(item, included, recur_keys)


def reify_relationships_many(
    items: list[RawItem],
    included: Included,
    recur_keys: list[str] | None = None,
) -> list[Item]:
    return do_reify_relationships(items, included, recur_keys)


def do_reify_relationships(
    item: RawItem | list[RawItem] | None,
    included: Included,
    recur_keys: list[str] | None = None,
) -> Item | list[Item] | None:
    if item is None:
        return None

    if is_list(item):
        return [do_reify_relationships(i, included) for i in item]

    if "relationships" in item:
        for name, relationship in item["relationships"].items():
            reified = reify_relationship(relationship, included)
            if recur_keys and name in recur_keys:
                reified = do_reify_relationships(reified, included)
            item["relationships"][name] = reified

    return item


def reify_relationship(relationship: Relationships, included: Included) -> Data | list[Data] | None:
    key = relationship["data"]

    if isinstance(key, list):
        return [deepcopy(included[k["type"]][k["id"]]) for k in key]

    if isinstance(key, dict):
        return deepcopy(included[key["type"]][key["id"]])

    return None


def is_list(v: Any):
    return isinstance(v, list)


def parse_included(data: Data) -> Included:
    included: Data = defaultdict(dict)
    for include in data["included"]:
        included[include["type"]][include["id"]] = include
    return included
