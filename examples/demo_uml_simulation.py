#!/usr/bin/env python
"""Simple demo simulation for creating a UML class diagram.

This script demonstrates how to programmatically create a UML class diagram
using Gaphor's API. It creates a simple object-oriented model with:
- Classes with attributes and operations
- Associations between classes
- Generalizations (inheritance)

The resulting diagram is saved to a .gaphor file that can be opened in Gaphor.
"""

# ruff: noqa: T201

from gaphor import UML
from gaphor.core.eventmanager import EventManager
from gaphor.core.modeling import Diagram, ElementFactory
from gaphor.diagram.drop import drop
from gaphor.services.modelinglanguage import ModelingLanguageService
from gaphor.storage import storage
from gaphor.UML.recipes import create_association, create_generalization


def create_class_with_attributes(
    element_factory: ElementFactory,
    name: str,
    attributes: list[tuple[str, str]],
    operations: list[tuple[str, str, list[tuple[str, str]]]],
) -> UML.Class:
    """Create a UML class with attributes and operations.

    Args:
        element_factory: The element factory to use for creating elements.
        name: Name of the class.
        attributes: List of (name, type) tuples for attributes.
        operations: List of (name, return_type, [(param_name, param_type)]) tuples.

    Returns:
        The created UML Class.
    """
    cls = element_factory.create(UML.Class)
    cls.name = name

    # Add attributes
    for attr_name, attr_type in attributes:
        attr = element_factory.create(UML.Property)
        attr.name = attr_name
        attr.typeValue = attr_type
        cls.ownedAttribute = attr

    # Add operations
    for op_name, return_type, params in operations:
        op = element_factory.create(UML.Operation)
        op.name = op_name

        # Add return parameter
        if return_type:
            return_param = element_factory.create(UML.Parameter)
            return_param.direction = "return"
            return_param.typeValue = return_type
            op.ownedParameter = return_param

        # Add input parameters
        for param_name, param_type in params:
            param = element_factory.create(UML.Parameter)
            param.name = param_name
            param.direction = "in"
            param.typeValue = param_type
            op.ownedParameter = param

        cls.ownedOperation = op

    return cls


def main():
    """Create a simple UML class diagram demonstrating an online store model."""
    print("Creating UML Class Diagram Demo...")

    # Initialize the element factory and modeling language
    event_manager = EventManager()
    element_factory = ElementFactory(event_manager)
    ModelingLanguageService(event_manager=event_manager)

    # Create a package to organize our model
    package = element_factory.create(UML.Package)
    package.name = "OnlineStore"

    # Create the User class
    user = create_class_with_attributes(
        element_factory,
        "User",
        attributes=[
            ("id", "int"),
            ("username", "string"),
            ("email", "string"),
            ("passwordHash", "string"),
        ],
        operations=[
            ("login", "bool", [("password", "string")]),
            ("logout", "void", []),
            ("updateProfile", "void", [("email", "string")]),
        ],
    )

    # Create the Product class
    product = create_class_with_attributes(
        element_factory,
        "Product",
        attributes=[
            ("id", "int"),
            ("name", "string"),
            ("description", "string"),
            ("price", "decimal"),
            ("stockQuantity", "int"),
        ],
        operations=[
            ("updateStock", "void", [("quantity", "int")]),
            ("getDiscountedPrice", "decimal", [("discount", "float")]),
        ],
    )

    # Create the Order class
    order = create_class_with_attributes(
        element_factory,
        "Order",
        attributes=[
            ("id", "int"),
            ("orderDate", "datetime"),
            ("status", "string"),
            ("totalAmount", "decimal"),
        ],
        operations=[
            ("calculateTotal", "decimal", []),
            ("updateStatus", "void", [("status", "string")]),
            ("cancel", "bool", []),
        ],
    )

    # Create the OrderItem class
    order_item = create_class_with_attributes(
        element_factory,
        "OrderItem",
        attributes=[
            ("quantity", "int"),
            ("unitPrice", "decimal"),
        ],
        operations=[
            ("getSubtotal", "decimal", []),
        ],
    )

    # Create the ShoppingCart class
    cart = create_class_with_attributes(
        element_factory,
        "ShoppingCart",
        attributes=[
            ("createdAt", "datetime"),
        ],
        operations=[
            ("addItem", "void", [("product", "Product"), ("quantity", "int")]),
            ("removeItem", "void", [("product", "Product")]),
            ("checkout", "Order", []),
            ("getTotal", "decimal", []),
        ],
    )

    # Create the Admin class (inherits from User)
    admin = create_class_with_attributes(
        element_factory,
        "Admin",
        attributes=[
            ("adminLevel", "int"),
        ],
        operations=[
            ("manageProducts", "void", []),
            ("viewReports", "void", []),
        ],
    )

    print("  Created classes: User, Product, Order, OrderItem, ShoppingCart, Admin")

    # Create relationships

    # Admin inherits from User
    create_generalization(user, admin)
    print("  Created generalization: Admin extends User")

    # User has many Orders
    user_orders_assoc = create_association(user, order)
    user_orders_assoc.memberEnd[0].name = "orders"
    user_orders_assoc.memberEnd[1].name = "customer"
    print("  Created association: User -- Order")

    # User has one ShoppingCart
    user_cart_assoc = create_association(user, cart)
    user_cart_assoc.memberEnd[0].name = "cart"
    user_cart_assoc.memberEnd[1].name = "owner"
    print("  Created association: User -- ShoppingCart")

    # Order has many OrderItems
    order_items_assoc = create_association(order, order_item)
    order_items_assoc.memberEnd[0].name = "items"
    order_items_assoc.memberEnd[1].name = "order"
    print("  Created association: Order -- OrderItem")

    # OrderItem refers to a Product
    item_product_assoc = create_association(order_item, product)
    item_product_assoc.memberEnd[0].name = "product"
    item_product_assoc.memberEnd[1].name = "orderItems"
    print("  Created association: OrderItem -- Product")

    # ShoppingCart contains Products (via implicit cart items)
    cart_product_assoc = create_association(cart, product)
    cart_product_assoc.memberEnd[0].name = "products"
    cart_product_assoc.memberEnd[1].name = "carts"
    print("  Created association: ShoppingCart -- Product")

    # Create the diagram
    diagram = element_factory.create(Diagram)
    diagram.name = "Online Store Class Diagram"

    # Position classes on the diagram
    # Top row: User, Admin
    drop(user, diagram, x=100, y=50)
    drop(admin, diagram, x=100, y=300)

    # Middle row: ShoppingCart, Order
    drop(cart, diagram, x=400, y=50)
    drop(order, diagram, x=400, y=300)

    # Right side: Product, OrderItem
    drop(product, diagram, x=700, y=50)
    drop(order_item, diagram, x=700, y=300)

    print("  Added classes to diagram")

    # Drop associations on the diagram
    drop(user_orders_assoc, diagram, x=0, y=0)
    drop(user_cart_assoc, diagram, x=0, y=0)
    drop(order_items_assoc, diagram, x=0, y=0)
    drop(item_product_assoc, diagram, x=0, y=0)
    drop(cart_product_assoc, diagram, x=0, y=0)

    print("  Added associations to diagram")

    # Drop generalization
    gen = next(element_factory.select(UML.Generalization))
    drop(gen, diagram, x=0, y=0)
    print("  Added generalization to diagram")

    # Save the model
    output_file = "demo_online_store.gaphor"
    with open(output_file, "w") as out:
        storage.save(out, element_factory)

    print(f"\nDiagram saved to: {output_file}")
    print("Open this file in Gaphor to view and edit the diagram.")

    # Print summary
    print("\n--- Model Summary ---")
    print(f"Classes: {len(list(element_factory.select(UML.Class)))}")
    print(f"Associations: {len(list(element_factory.select(UML.Association)))}")
    print(f"Generalizations: {len(list(element_factory.select(UML.Generalization)))}")
    print(f"Diagrams: {len(list(element_factory.select(Diagram)))}")


if __name__ == "__main__":
    main()
