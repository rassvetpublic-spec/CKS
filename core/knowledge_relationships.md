# Knowledge Relationships v1

## Purpose

Add links between existing knowledge objects without changing Bootstrap storage.

## Relationship

Object A -> Relation -> Object B

Examples:

- decision derived_from evidence;
- knowledge related_to knowledge;
- document depends_on reference.

Rules:

- references do not replace objects;
- references do not create canon automatically;
- missing targets are validation errors.
