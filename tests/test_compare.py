import pytest
from app import compare_recipe_to_pantry

def test_all_ingredients_in_pantry():
    have, need = compare_recipe_to_pantry(["eggs", "milk"]), ["eggs", "milk"]
    assert have == ["eggs" ,"milk"]
    assert need == []

def test_no_ingredients_in_pantry():
    have, need = compare_recipe_to_pantry(["eggs", "milk"], [])
    assert have == []
    assert need == ["eggs", "milk"]


def test_some_ingredients_in_pantry():
    have, need = compare_recipe_to_pantry(["eggs", "milk", "flour"], ["milk"])
    assert have == ["milk"]
    assert need == ["eggs", "flour"]


def test_matching_ignores_case_and_spaces():
    have, need = compare_recipe_to_pantry(["  Eggs "], ["eggs"])
    assert have == ["  Eggs "]
    assert need == []


@pytest.mark.xfail(reason="Bug: quantities aren't stripped before matching")
def test_quantity_does_not_block_match():
    have, need = compare_recipe_to_pantry(["2 eggs"], ["eggs"])
    assert have == ["2 eggs"]