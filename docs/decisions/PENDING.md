# Pending owner decisions (class A)

## PENDING-001 · Resend sender and recipients
`MAIL_FROM` must be on a domain verified in Resend (e.g. `Agile Institute™ <hola@agileinstitute.es>`), and
`MAIL_TEAM_TO` must list who receives new pilot requests. Set both plus `RESEND_API_KEY` in the Render dashboard.
Until then the BFF stores requests but sends no email.

## PENDING-002 · "Recursos Humanos" on the landing
The in-progress copy listed Persona, Líder, Equipo, Recursos Humanos, Organización under "Una vista para cada
dimensión". Following CHANGES.md ("una vista por cada dimensión competencial"), the section now shows the five
competency dimensions (Persona, Equipo, Liderazgo, Organización, IA transversal), each linking to its dashboard.
RRHH is a role, not a dimension, so it was left out. Confirm, or say where RRHH should appear.
