# CKS v1.2 Object Model

## Назначение

CKS хранит контекст, решения и знания через связанные объекты.

## Основные объекты

- Context — исходный контекст и ограничения.
- Proposal — предложение решения.
- Decision — принятое решение и его обоснование.
- Evidence — подтверждающие материалы.
- Change — реализованное изменение.
- Learning Event — полученный опыт.
- Knowledge — закреплённое знание.
- Snapshot — состояние системы для восстановления контекста.

## Связи

Context → Proposal → Decision → Change → Result → Learning Event → Knowledge → Snapshot

Decision должен иметь связь с Evidence.
Change должен иметь связь с Decision.

## Правило

Объекты CKS являются источником знаний. GitHub Project используется только для управления состоянием работы.
