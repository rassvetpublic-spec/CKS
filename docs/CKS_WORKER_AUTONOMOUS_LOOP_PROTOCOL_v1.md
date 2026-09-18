# CKS WORKER AUTONOMOUS LOOP PROTOCOL v1

## Purpose

Define the autonomous Worker cycle for GitHub-based task discovery, execution, and reporting.

## Repository

REPOSITORY:
https://github.com/rassvetpublic-spec/CKS

## Loop

READ PROJECT
↓
SCAN ISSUES
↓
CLAIM TASK
↓
EXECUTE
↓
REPORT
↓
CHECK CHANGES
↓
RESTART LOOP

## Issue discovery

Worker searches open issues for tasks without an assigned executor.

If a task exists and has no executor:

- claim the task;
- record Worker identity;
- start execution.

## Claim format

CLAIMED:

Worker:

Repository:
https://github.com/rassvetpublic-spec/CKS

Task:

Started:

## Channel rule

Every Worker task must define:

REPOSITORY:
TARGET:
CHANNEL:
RETURN FORMAT:

If CHANNEL is missing:

Worker must create a comment in the task stating that GitHub Issue conversation is used as the fallback feedback channel.

## Reporting

If a report template exists, use it.

If no template exists:

STATUS:
PASS / FAIL / BLOCKED

DONE:
-

EVIDENCE:
-

BLOCKERS:
-

NEXT:
-

## Change detection

After completing a task, Worker repeats issue inspection.

New issue, task update, or relevant GitHub change restarts the loop from READ PROJECT.
