# Antigravity State Adapter v1

## Назначение

State Adapter (адаптер состояния) является промежуточным слоем между KAT9I_OS Runtime и Antigravity GUI.

Он запрещает прямую зависимость интерфейса от внутренних процессов исполнения.

## Граница

```
KAT9I_OS Runtime
        ↓
State Adapter
        ↓
Event Contract
        ↓
Antigravity GUI
        ↓
Electron
```

## Ответственность

State Adapter:

- принимает подтверждённые состояния;
- нормализует формат данных;
- передаёт события GUI;
- сохраняет связь с evidence.

## Запрещено

State Adapter не:

- принимает решения;
- изменяет CKS Canon;
- выполняет задачи worker;
- заменяет QA.

## Минимальная модель состояния

```
system
 ├─ status
 └─ version

task
 ├─ id
 └─ status

qa
 └─ evidence

worker
 └─ queue_state
```

## Связь QA_CONTEXT

Для отображения проверок используется:

```
QA_CONTEXT = PR_HEAD + BASE_REFERENCE
```

GUI показывает состояние проверки, но не становится источником вердикта.
