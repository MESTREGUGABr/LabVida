## Problem Statement

O LabVida possui estados `CANCELADA` para a Ordem de Servico e `CANCELADO` para seus itens, mas ainda nao possui um fluxo coerente para cancelar itens ou agregar esses estados. Sem essa regra, um cancelamento parcial pode cancelar indevidamente a OS ou apagar o fato de que outros itens foram concluidos com sucesso.

## Solution

Implementar o cancelamento de itens da Ordem de Servico com uma regra agregada clara: a OS so assume `CANCELADA` quando todos os seus itens estiverem cancelados. Cancelar um ou mais itens nao cancela a OS enquanto houver trabalho ativo. Se restarem itens ativos pendentes, a OS continua no fluxo; se todos os itens ativos tiverem Laudos liberados, a OS assume `CONCLUIDA`.

## User Stories

1. As a gestor autorizado, I want to cancel an individual active OS item, so that a procedure that will not be performed is removed from the remaining work without canceling unrelated items.
2. As a gestor autorizado, I want the system to reject cancellation of an item that already has a released Laudo, so that a completed clinical result is not erased by an operational cancellation.
3. As a gestor autorizado, I want the system to reject cancellation of an item that is already faturado, so that financial records are not invalidated by an operational cancellation.
4. As a gestor autorizado, I want every item cancellation to identify the authenticated user, so that critical operational changes remain traceable.
5. As an atendente, I want an OS with at least one active pending item to remain in its current operational flow after a partial cancellation, so that the remaining work can continue.
6. As an atendente, I want an OS with canceled items and all remaining active items with released Laudos to become `CONCLUIDA`, so that successful work is recognized even when another requested procedure was canceled.
7. As an atendente, I want an OS whose final remaining item is canceled to become `CANCELADA`, so that an OS with no remaining work is not left open indefinitely.
8. As a gestor autorizado, I want an attempt to cancel an entire OS containing a released or faturado item to be blocked, so that the aggregate cancellation rule cannot conflict with completed work.
9. As a gestor autorizado, I want to cancel the remaining active items individually when an OS contains completed items, so that the completed items remain valid and the aggregate status can become `CONCLUIDA`.
10. As an auditor, I want OS status transitions caused by item cancellation to be recorded in `os_status_historico`, so that the lifecycle of the OS can be reconstructed.
11. As an auditor, I want each OS status transition to record the authenticated user who caused it, so that the actor of the aggregate decision is distinguishable from the responsible technician of a Laudo.
12. As an operador, I want repeated cancellation attempts to be rejected or treated as no-ops according to the existing status rules, so that history does not contain misleading duplicate transitions.

## Implementation Decisions

- Use the existing Ordem de Servico service as the highest integration seam for item cancellation and aggregate status evaluation.
- Introduce an operation for canceling an individual OS item that validates the item and its parent OS, checks the actor's authorization, changes only an active item, and records the authenticated user for auditability.
- Treat `CANCELADO` as the only non-active item state for the aggregate rules. Items with released Laudos or `FATURADO` status cannot be canceled.
- Define the aggregate status rules as follows:
  - all items `CANCELADO` -> OS `CANCELADA`;
  - at least one active item pending -> OS remains in its current operational status;
  - no active pending item and every active item has a released Laudo -> OS `CONCLUIDA`.
- A canceled item does not invalidate a released item. An OS containing canceled items and successfully released active items becomes `CONCLUIDA`, not `CANCELADA`.
- Block integral OS cancellation when any item has a released Laudo or is `FATURADO`; item-level cancellation remains the allowed operation for remaining active items.
- Record an OS transition in `os_status_historico` only when the aggregate status actually changes, using the authenticated user as `usuario_id`.
- Keep the responsible technician of a Laudo separate from the authenticated user who performs the cancellation or causes the OS transition.
- Keep the operation transactional: item status, aggregate OS status, status history, and audit information must succeed or fail together.
- Prefer existing status values and persistence structures; no new OS or item status is needed.

## Testing Decisions

- Test external behavior through the existing service-level database seam, not private helper functions or implementation details.
- Cover cancellation of a single active item while another item remains pending; the OS must not be canceled.
- Cover cancellation of the final item; the OS must become `CANCELADA` and append one history record with the authenticated actor.
- Cover one canceled item plus one active item with released Laudo; the OS must become `CONCLUIDA`.
- Cover attempts to cancel released and faturado items; they must be rejected and leave the item, OS, and history unchanged.
- Cover integral OS cancellation attempts when completed items exist; they must be rejected.
- Cover repeated cancellation and already terminal OS/item states to prevent duplicate or contradictory history.
- Follow the existing laboratorial and atendimento service tests, which use real model state and assert observable status and history outcomes.

## Out of Scope

- Automatic conclusion after releasing the last Laudo; this belongs to issue #6.
- Designing a new RBAC system; use the project's existing authenticated-user and manager authorization direction.
- Retrofitting a complete corporate audit-log subsystem.
- Changing the meaning of `FATURADO`, revising released Laudos, or undoing completed clinical work.
- Adding new OS or item statuses.

## Further Notes

- Existing project documentation says that only managers may cancel critical operations and that cancellation is an auditable event.
- The domain glossary defines an active OS item as one that is not canceled and defines OS cancellation as the state where all items are canceled.
- The decision is recorded in ADRs 0005 and 0006.
