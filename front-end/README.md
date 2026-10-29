# Front-end · Landing Agile Institute

Landing page pública basada en `propuesta front-end.png`. Es una SPA en **React 18 + TypeScript + Vite** con un
**BFF Node** (backend-for-frontend) que la conecta con el centro de mando FastAPI (`../centro-de-mando`).

```
Navegador ──► Vite (dev :5173) ──/api──► BFF Node (:5174) ──┬─► /api/pilot-requests  (propio: valida y guarda)
                                                            ├─► /api/health
                                                            └─► resto de /api/*  ──► centro de mando FastAPI (:8765)
```

En producción el BFF también sirve `dist/`, así que todo sale por un único puerto.

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

Para que **Acceder** y el resto de `/api` funcionen, arranca también el centro de mando
(`python -m uvicorn app.main:app --port 8765` en `../centro-de-mando`). Si no está en marcha, la landing funciona igual
y el BFF responde `502` a las rutas que delega.

## Variables

| Variable | Por defecto | Uso |
|---|---|---|
| `BFF_PORT` | `5174` | Puerto del BFF (y destino del proxy de Vite) |
| `CDM_API_URL` | `http://127.0.0.1:8765` | Centro de mando al que se delega `/api/*` |
| `VITE_APP_URL` | `/` | Destino del botón **Acceder** (se fija al compilar) |

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
