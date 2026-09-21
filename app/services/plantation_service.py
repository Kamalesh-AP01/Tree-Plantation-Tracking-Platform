from datetime import date

from app.models import tree, plantation


def plant_tree(db, user_id, tree_name, location_id, planting_date):
    # Check whether the tree already exists
    existing_tree = (
        db.query(tree.Tree)
        .filter(tree.Tree.tree_name == tree_name)
        .first()
    )

    if existing_tree:
        tree_data = existing_tree
    else:
        tree_data = tree.Tree(
            tree_name=tree_name
        )

        db.add(tree_data)
        db.commit()
        db.refresh(tree_data)

    # Create plantation record
    plantation_data = plantation.Plantation(
        user_id=user_id,
        tree_id=tree_data.id,
        location_id=location_id,
        planting_date=date.fromisoformat(planting_date),
    )

    db.add(plantation_data)
    db.commit()
    db.refresh(plantation_data)

    return plantation_data, tree_data