from unittest.mock import MagicMock

from app.services.plantation_service import plant_tree


def test_plant_tree_existing_tree():
    db = MagicMock()

    existing_tree = MagicMock()
    existing_tree.id = 10
    existing_tree.tree_name = "Mango"

    db.query.return_value.filter.return_value.first.return_value = existing_tree

    plantation_data, tree_data = plant_tree(
        db=db,
        user_id=1,
        tree_name="Mango",
        location_id=2,
        planting_date="2026-09-21",
    )

    assert tree_data is existing_tree
    assert plantation_data.user_id == 1
    assert plantation_data.tree_id == 10
    assert plantation_data.location_id == 2
    assert str(plantation_data.planting_date) == "2026-09-21"


def test_plant_tree_new_tree():
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    plantation_data, tree_data = plant_tree(
        db=db,
        user_id=1,
        tree_name="Neem",
        location_id=3,
        planting_date="2026-09-21",
    )

    assert tree_data.tree_name == "Neem"
    assert plantation_data.user_id == 1
    assert plantation_data.location_id == 3
    assert str(plantation_data.planting_date) == "2026-09-21"

    db.add.assert_called()
    assert db.commit.call_count == 2