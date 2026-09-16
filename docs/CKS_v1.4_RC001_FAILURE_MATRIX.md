# CKS v1.4 RC001 Failure Matrix

| Area | Failure | Expected handling |
|---|---|---|
| Schema | invalid object | reject validation |
| Metrics | missing fields | WARN |
| Graph | broken relation | fail graph check |
| Review Gate | missing evidence | block gate |
| Dashboard | missing artifact | report error |
