"""Tests for the demo UML simulation script.

These tests verify that the demo simulation correctly creates UML elements
including classes, attributes, operations, associations, and generalizations.
"""

import pytest

from gaphor import UML
from gaphor.core.modeling import Diagram
from gaphor.diagram.drop import drop
from gaphor.UML.recipes import create_association, create_generalization


class TestCreateClassWithAttributes:
    """Tests for creating UML classes with attributes and operations."""

    def test_create_simple_class(self, element_factory):
        """Test creating a simple class without attributes or operations."""
        cls = element_factory.create(UML.Class)
        cls.name = "SimpleClass"

        assert cls.name == "SimpleClass"
        assert len(cls.ownedAttribute) == 0
        assert len(cls.ownedOperation) == 0

    def test_create_class_with_attributes(self, element_factory):
        """Test creating a class with attributes."""
        cls = element_factory.create(UML.Class)
        cls.name = "User"

        # Add attributes
        attr1 = element_factory.create(UML.Property)
        attr1.name = "id"
        attr1.typeValue = "int"
        cls.ownedAttribute = attr1

        attr2 = element_factory.create(UML.Property)
        attr2.name = "username"
        attr2.typeValue = "string"
        cls.ownedAttribute = attr2

        assert cls.name == "User"
        assert len(cls.ownedAttribute) == 2
        assert cls.ownedAttribute[0].name == "id"
        assert cls.ownedAttribute[0].typeValue == "int"
        assert cls.ownedAttribute[1].name == "username"
        assert cls.ownedAttribute[1].typeValue == "string"

    def test_create_class_with_operations(self, element_factory):
        """Test creating a class with operations."""
        cls = element_factory.create(UML.Class)
        cls.name = "User"

        # Add operation with return type
        op = element_factory.create(UML.Operation)
        op.name = "login"

        return_param = element_factory.create(UML.Parameter)
        return_param.direction = "return"
        return_param.typeValue = "bool"
        op.ownedParameter = return_param

        # Add input parameter
        input_param = element_factory.create(UML.Parameter)
        input_param.name = "password"
        input_param.direction = "in"
        input_param.typeValue = "string"
        op.ownedParameter = input_param

        cls.ownedOperation = op

        assert len(cls.ownedOperation) == 1
        assert cls.ownedOperation[0].name == "login"
        assert len(cls.ownedOperation[0].ownedParameter) == 2

    def test_create_class_with_multiple_operations(self, element_factory):
        """Test creating a class with multiple operations."""
        cls = element_factory.create(UML.Class)
        cls.name = "ShoppingCart"

        operations = ["addItem", "removeItem", "checkout", "getTotal"]
        for op_name in operations:
            op = element_factory.create(UML.Operation)
            op.name = op_name
            cls.ownedOperation = op

        assert len(cls.ownedOperation) == 4
        op_names = [op.name for op in cls.ownedOperation]
        assert "addItem" in op_names
        assert "removeItem" in op_names
        assert "checkout" in op_names
        assert "getTotal" in op_names


class TestAssociations:
    """Tests for creating associations between classes."""

    def test_create_association_between_classes(self, element_factory):
        """Test creating an association between two classes."""
        class_a = element_factory.create(UML.Class)
        class_a.name = "User"

        class_b = element_factory.create(UML.Class)
        class_b.name = "Order"

        assoc = create_association(class_a, class_b)

        assert assoc is not None
        assert len(assoc.memberEnd) == 2
        types = [p.type for p in assoc.memberEnd]
        assert class_a in types
        assert class_b in types

    def test_association_end_names(self, element_factory):
        """Test setting names on association ends."""
        user = element_factory.create(UML.Class)
        user.name = "User"

        order = element_factory.create(UML.Class)
        order.name = "Order"

        assoc = create_association(user, order)
        assoc.memberEnd[0].name = "orders"
        assoc.memberEnd[1].name = "customer"

        assert assoc.memberEnd[0].name == "orders"
        assert assoc.memberEnd[1].name == "customer"

    def test_multiple_associations(self, element_factory):
        """Test creating multiple associations."""
        user = element_factory.create(UML.Class)
        user.name = "User"

        order = element_factory.create(UML.Class)
        order.name = "Order"

        cart = element_factory.create(UML.Class)
        cart.name = "ShoppingCart"

        assoc1 = create_association(user, order)
        assoc2 = create_association(user, cart)

        associations = list(element_factory.select(UML.Association))
        assert len(associations) == 2
        assert assoc1 in associations
        assert assoc2 in associations


class TestGeneralizations:
    """Tests for creating generalizations (inheritance)."""

    def test_create_generalization(self, element_factory):
        """Test creating a generalization relationship."""
        parent = element_factory.create(UML.Class)
        parent.name = "User"

        child = element_factory.create(UML.Class)
        child.name = "Admin"

        gen = create_generalization(parent, child)

        assert gen is not None
        assert gen.general is parent
        assert gen.specific is child

    def test_child_inherits_from_parent(self, element_factory):
        """Test that the generalization establishes proper inheritance."""
        parent = element_factory.create(UML.Class)
        parent.name = "User"

        child = element_factory.create(UML.Class)
        child.name = "Admin"

        gen = create_generalization(parent, child)

        assert parent in child.general
        assert child in parent.specific


class TestDiagramCreation:
    """Tests for creating diagrams and dropping elements."""

    def test_create_empty_diagram(self, element_factory):
        """Test creating an empty diagram."""
        diagram = element_factory.create(Diagram)
        diagram.name = "Test Diagram"

        assert diagram.name == "Test Diagram"
        assert len(diagram.ownedPresentation) == 0

    def test_drop_class_on_diagram(self, element_factory):
        """Test dropping a class on a diagram."""
        cls = element_factory.create(UML.Class)
        cls.name = "TestClass"

        diagram = element_factory.create(Diagram)
        diagram.name = "Test Diagram"

        presentation = drop(cls, diagram, x=100, y=100)

        assert presentation is not None
        assert len(diagram.ownedPresentation) == 1
        assert cls.presentation[0] is presentation

    def test_drop_multiple_classes_on_diagram(self, element_factory):
        """Test dropping multiple classes on a diagram."""
        class1 = element_factory.create(UML.Class)
        class1.name = "Class1"

        class2 = element_factory.create(UML.Class)
        class2.name = "Class2"

        class3 = element_factory.create(UML.Class)
        class3.name = "Class3"

        diagram = element_factory.create(Diagram)
        diagram.name = "Test Diagram"

        drop(class1, diagram, x=100, y=100)
        drop(class2, diagram, x=300, y=100)
        drop(class3, diagram, x=500, y=100)

        assert len(diagram.ownedPresentation) == 3

    def test_drop_association_on_diagram(self, element_factory):
        """Test dropping an association on a diagram with both ends present."""
        class_a = element_factory.create(UML.Class)
        class_a.name = "ClassA"

        class_b = element_factory.create(UML.Class)
        class_b.name = "ClassB"

        assoc = create_association(class_a, class_b)

        diagram = element_factory.create(Diagram)
        diagram.name = "Test Diagram"

        # Drop classes first
        drop(class_a, diagram, x=100, y=100)
        drop(class_b, diagram, x=300, y=100)

        # Drop association
        drop(assoc, diagram, x=200, y=100)

        # Association should connect the two classes
        assert len(diagram.ownedPresentation) == 3

    def test_drop_generalization_on_diagram(self, element_factory):
        """Test dropping a generalization on a diagram."""
        parent = element_factory.create(UML.Class)
        parent.name = "Parent"

        child = element_factory.create(UML.Class)
        child.name = "Child"

        gen = create_generalization(parent, child)

        diagram = element_factory.create(Diagram)
        diagram.name = "Test Diagram"

        # Drop classes first
        drop(parent, diagram, x=100, y=100)
        drop(child, diagram, x=100, y=300)

        # Drop generalization
        drop(gen, diagram, x=100, y=200)

        assert len(diagram.ownedPresentation) == 3


class TestOnlineStoreModel:
    """Integration tests simulating the demo online store model."""

    def test_create_online_store_classes(self, element_factory):
        """Test creating all classes for the online store model."""
        class_names = ["User", "Product", "Order", "OrderItem", "ShoppingCart", "Admin"]
        classes = {}

        for name in class_names:
            cls = element_factory.create(UML.Class)
            cls.name = name
            classes[name] = cls

        created_classes = list(element_factory.select(UML.Class))
        assert len(created_classes) == 6

        for name in class_names:
            assert any(c.name == name for c in created_classes)

    def test_create_online_store_relationships(self, element_factory):
        """Test creating all relationships for the online store model."""
        # Create classes
        user = element_factory.create(UML.Class)
        user.name = "User"

        admin = element_factory.create(UML.Class)
        admin.name = "Admin"

        order = element_factory.create(UML.Class)
        order.name = "Order"

        cart = element_factory.create(UML.Class)
        cart.name = "ShoppingCart"

        product = element_factory.create(UML.Class)
        product.name = "Product"

        order_item = element_factory.create(UML.Class)
        order_item.name = "OrderItem"

        # Create generalization
        gen = create_generalization(user, admin)

        # Create associations
        create_association(user, order)
        create_association(user, cart)
        create_association(order, order_item)
        create_association(order_item, product)
        create_association(cart, product)

        # Verify
        generalizations = list(element_factory.select(UML.Generalization))
        assert len(generalizations) == 1
        assert gen.general is user
        assert gen.specific is admin

        associations = list(element_factory.select(UML.Association))
        assert len(associations) == 5

    def test_create_complete_online_store_diagram(self, element_factory):
        """Test creating a complete diagram with all elements."""
        # Create classes
        classes = {}
        for name in ["User", "Admin", "Product", "Order", "OrderItem", "ShoppingCart"]:
            cls = element_factory.create(UML.Class)
            cls.name = name
            classes[name] = cls

        # Create relationships
        gen = create_generalization(classes["User"], classes["Admin"])
        assoc1 = create_association(classes["User"], classes["Order"])
        assoc2 = create_association(classes["User"], classes["ShoppingCart"])
        assoc3 = create_association(classes["Order"], classes["OrderItem"])
        assoc4 = create_association(classes["OrderItem"], classes["Product"])
        assoc5 = create_association(classes["ShoppingCart"], classes["Product"])

        # Create diagram
        diagram = element_factory.create(Diagram)
        diagram.name = "Online Store Class Diagram"

        # Drop all classes
        drop(classes["User"], diagram, x=100, y=50)
        drop(classes["Admin"], diagram, x=100, y=300)
        drop(classes["ShoppingCart"], diagram, x=400, y=50)
        drop(classes["Order"], diagram, x=400, y=300)
        drop(classes["Product"], diagram, x=700, y=50)
        drop(classes["OrderItem"], diagram, x=700, y=300)

        # Drop all relationships
        drop(gen, diagram, x=0, y=0)
        drop(assoc1, diagram, x=0, y=0)
        drop(assoc2, diagram, x=0, y=0)
        drop(assoc3, diagram, x=0, y=0)
        drop(assoc4, diagram, x=0, y=0)
        drop(assoc5, diagram, x=0, y=0)

        # Verify diagram has all presentations
        # 6 classes + 1 generalization + 5 associations = 12 elements
        assert len(diagram.ownedPresentation) == 12


class TestPackageOrganization:
    """Tests for organizing elements in packages."""

    def test_create_package(self, element_factory):
        """Test creating a package."""
        package = element_factory.create(UML.Package)
        package.name = "OnlineStore"

        assert package.name == "OnlineStore"

    def test_element_factory_queries(self, element_factory):
        """Test querying elements from the factory."""
        # Create some elements
        for name in ["Class1", "Class2", "Class3"]:
            cls = element_factory.create(UML.Class)
            cls.name = name

        # Query by type
        classes = list(element_factory.select(UML.Class))
        assert len(classes) == 3

        # Query with predicate
        class2 = next(
            element_factory.select(
                lambda e: isinstance(e, UML.Class) and e.name == "Class2"
            )
        )
        assert class2.name == "Class2"


class TestOperationParameters:
    """Tests for operation parameters."""

    def test_operation_with_return_type(self, element_factory):
        """Test operation with a return type."""
        cls = element_factory.create(UML.Class)
        cls.name = "Calculator"

        op = element_factory.create(UML.Operation)
        op.name = "add"

        # Return parameter
        ret = element_factory.create(UML.Parameter)
        ret.direction = "return"
        ret.typeValue = "int"
        op.ownedParameter = ret

        cls.ownedOperation = op

        return_params = [p for p in op.ownedParameter if p.direction == "return"]
        assert len(return_params) == 1
        assert return_params[0].typeValue == "int"

    def test_operation_with_input_parameters(self, element_factory):
        """Test operation with input parameters."""
        cls = element_factory.create(UML.Class)
        cls.name = "Calculator"

        op = element_factory.create(UML.Operation)
        op.name = "add"

        # Input parameters
        param_a = element_factory.create(UML.Parameter)
        param_a.name = "a"
        param_a.direction = "in"
        param_a.typeValue = "int"
        op.ownedParameter = param_a

        param_b = element_factory.create(UML.Parameter)
        param_b.name = "b"
        param_b.direction = "in"
        param_b.typeValue = "int"
        op.ownedParameter = param_b

        cls.ownedOperation = op

        input_params = [p for p in op.ownedParameter if p.direction == "in"]
        assert len(input_params) == 2
        assert input_params[0].name == "a"
        assert input_params[1].name == "b"
