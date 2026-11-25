# Front-end · Landing Agile Institute

Landing page pública basada en `propuesta front-end.png`. Es una SPA en **React 18 + TypeScript + Vite** con un
**BFF Node** (backend-for-frontend) que la conecta con el centro de mando FastAPI (`../centro-de-mando`).

```
Navegador ──► Vite (dev :5173) ──/api, /app, /static──► BFF Node (:5174) ──┬─► /api/pilot-requests  (propio: valida y guarda)
                                                                           ├─► /api/health
                                                                           └─► /app → /, /static/*, resto de /api/*
                                                                                 ──► centro de mando FastAPI (:8765)
```

En producción el BFF también sirve `dist/`, así que todo sale por un único puerto. La landing y el centro de mando
comparten origen: la cookie de sesión del centro de mando (`SameSite=strict`) funciona sin CORS, **Acceder** abre
`/app` y cada entrada de "Tu cuadro de mando" abre su cuadro (`/app#/persona`, `/app#/equipo`…). Tras el acceso de
demostración se conserva el cuadro pedido; si el rol no lo tiene autorizado, el centro de mando vuelve a "Inicio".

## Arranque

```bash
cd front-end
npm install
cp .env.example .env        # opcional: puertos y URL del centro de mando
npm run dev                 # Vite (http://localhost:5173) + BFF en paralelo

# producción
npm run build && npm start  # http://127.0.0.1:5174

npm test                    # Vitest: UI (jsdom) + BFF (node)
npm run typecheck
```

Para que **Acceder**, `/app` y el resto de `/api` funcionen, arranca también el centro de mando
(`python -m uvicorn app.main:app --port 8765` en `../centro-de-mando`). Si no está en marcha, la landing funciona igual
y el BFF responde `502` a las rutas que delega.

## Despliegue en Render

`../render.yaml` (Blueprint) crea dos servicios en Frankfurt: **agile-landing** (web pública, Node: compila la landing
y arranca este BFF) y **centro-de-mando** (servicio privado, Python/FastAPI). El BFF recibe `CDM_API_URL` como
`host:puerto` de la red privada y escucha en el `PORT` que asigna Render. En Render: *New → Blueprint*, elige este
repositorio y confirma. Los datos de la demo son efímeros (ver comentarios de `render.yaml`).

## Variables

| Variable | Por defecto | Uso |
|---|---|---|
| `BFF_PORT` | `5174` | Puerto del BFF (y destino del proxy de Vite) |
| `CDM_API_URL` | `http://127.0.0.1:8765` | Centro de mando al que se delegan `/app`, `/static/*` y `/api/*` |
| `VITE_APP_URL` | `/app` | Destino de **Acceder** y de los accesos a cada cuadro (se fija al compilar) |
| `RESEND_API_KEY` | — | Clave de Resend. Sin ella el BFF no envía correos (solo los registra) |
| `MAIL_FROM` | — | Remitente de un dominio verificado en Resend |
| `MAIL_TEAM_TO` | — | Destinatarios internos (comas) del aviso de cada solicitud de piloto |

## Correo (Resend)

`server/mail.mjs` llama a la API REST de Resend (`POST https://api.resend.com/emails`) con `fetch`, sin SDK. Por
cada solicitud de piloto, tras guardarla, envía un **aviso al equipo** (`MAIL_TEAM_TO`, con `reply_to` al
solicitante) y un **acuse al solicitante**. Cada envío lleva `Idempotency-Key` (`pilot-team-<id>`, `pilot-ack-<id>`),
el texto del usuario se escapa en el HTML y un fallo de Resend solo se registra: nunca afecta a la respuesta ni a la
solicitud guardada. Para nuevos correos, reutiliza `sendEmail({ to, subject, html, text, replyTo, idempotencyKey })`.
En local el BFF no lee `.env`: exporta las variables o arranca con `node --env-file=.env server/index.mjs`.

## Estructura

```
src/
  content/landing.ts        Todo el texto de la página (editar aquí, no en los componentes)
  api/client.ts             Cliente HTTP tipado (solicitud de piloto, errores por campo)
  styles/tokens.css         Tokens de diseño: color, tipografía, radios, sombras
  styles/global.css         Base, accesibilidad, animación de aparición
  components/               Una sección por componente, cada una con su CSS Module
    illustrations/          Ilustraciones SVG en línea (sin imágenes externas)
  hooks/useReveal.ts        Aparición al hacer scroll (respeta prefers-reduced-motion)
server/index.mjs            BFF sin dependencias (node:http)
```

## Decisiones

- **CSS Modules + tokens** en lugar de un framework de utilidades: la página es pequeña y la identidad visual
  (azul petróleo `#0d3a4e`, verde azulado `#1fa39b`, cielo `#dcf0f6`, amarillo `#f3c623`) vive en un solo archivo.
- **Montserrat Variable** autoalojada con `@fontsource`: sin peticiones a terceros.
- **Ilustraciones en SVG** como componentes React: nítidas a cualquier tamaño y sin peso de imagen (JS total ≈ 55 kB gzip).
- **Formulario de piloto** en un `<dialog>` nativo, con validación en cliente y en servidor, mensajes por campo,
  campo trampa anti-spam y confirmación. Las solicitudes se guardan en `data/pilot-requests.jsonl` (ignorado por git);
  sustituir por correo/CRM es cambiar `handlePilotRequest` en el BFF.
- **Accesibilidad**: enlace "Saltar al contenido", jerarquía de encabezados, foco visible, menú móvil con
  `aria-expanded`, iconos decorativos ocultos y animaciones desactivadas con `prefers-reduced-motion`.
