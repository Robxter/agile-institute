# Pending owner decisions (class A)

## PENDING-001 · Resend sender and recipients
`MAIL_FROM` must be on a domain verified in Resend (e.g. `Agile Institute™ <hola@agileinstitute.es>`), and
`MAIL_TEAM_TO` must list who receives new pilot requests. Set both plus `RESEND_API_KEY` in the Render dashboard.
Until then the BFF stores requests but sends no email.

## ~~PENDING-002 · "Recursos Humanos" on the landing~~ — resolved 2026-11-25
Owner: the texts in `landing.ts` prevail, not the structure. The section keeps the owner's title and five cards
verbatim (Persona, Líder, Equipo, Recursos Humanos, Organización); each card links to its dashboard
(Líder → `#/liderazgo`), and Recursos Humanos, which has no dimension of its own, opens the centro de mando home (`/app`).
