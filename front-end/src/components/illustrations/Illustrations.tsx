// Ilustraciones planas en SVG (sin imágenes externas), en la línea gráfica de la propuesta.
import type { DimensionKey } from '../../content/landing';

const C = {
  ink: '#0d3a4e',
  teal: '#1fa39b',
  blue: '#1b7db3',
  sun: '#f3c623',
  skin: '#ffffff',
  sky: '#dcf0f6',
  white: '#ffffff',
};

interface PersonProps {
  x: number;
  y: number;
  s?: number;
  shirt?: string;
  long?: boolean;
  hair?: string;
}

/** Busto de persona: cabeza, pelo, cara sonriente y torso. (x, y) = centro de la cabeza. */
function Person({ x, y, s = 1, shirt = C.ink, long = false, hair = C.ink }: PersonProps) {
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <path d="M-20 44c0-16 9-24 20-24s20 8 20 24z" fill={shirt} />
      <path d="M-5 20l5 7 5-7" fill={C.white} />
      {long && <path d="M-14 -2c-2 14-2 24 3 28h22c5-4 5-14 3-28z" fill={hair} />}
      <circle r="13" fill={C.skin} stroke={C.ink} strokeWidth="2.4" />
      <path d="M-13.5 -1c0-11 6-15.5 13.5-15.5S13.5 -12 13.5 -1C9 -6 3-8-1-12c-3 5-8 9-12.5 11z" fill={hair} />
      <circle cx="-4.5" cy="2" r="1.5" fill={C.ink} />
      <circle cx="4.5" cy="2" r="1.5" fill={C.ink} />
      <path d="M-4 7q4 3.5 8 0" stroke={C.ink} strokeWidth="1.8" fill="none" strokeLinecap="round" />
    </g>
  );
}

function Bars({ x, y, h = [10, 16, 22], w = 7, colors = [C.blue, C.teal, C.sun] }: { x: number; y: number; h?: number[]; w?: number; colors?: string[] }) {
  return (
    <g>
      {h.map((bh, i) => (
        <rect key={i} x={x + i * (w + 3)} y={y - bh} width={w} height={bh} fill={colors[i % colors.length]} />
      ))}
    </g>
  );
}

function Laptop({ x, y, chart = 'bars' }: { x: number; y: number; chart?: 'bars' | 'line' }) {
  return (
    <g transform={`translate(${x} ${y})`}>
      <rect x="-22" y="-30" width="44" height="30" rx="3" fill={C.white} stroke={C.ink} strokeWidth="3" />
      {chart === 'bars' ? (
        <Bars x={-11} y={-6} h={[8, 13, 18]} w={6} />
      ) : (
        <path d="M-14 -9l8-8 6 5 10-10" stroke={C.blue} strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      )}
      <circle cx="-12" cy="3" r="4" fill={C.white} stroke={C.ink} strokeWidth="2" />
      <circle cx="12" cy="3" r="4" fill={C.white} stroke={C.ink} strokeWidth="2" />
    </g>
  );
}

function PersonaArt() {
  return (
    <>
      <Person x={84} y={62} s={1.25} long />
      <rect x="18" y="118" width="170" height="8" fill={C.ink} />
      <rect x="24" y="126" width="158" height="40" fill={C.blue} />
      <Laptop x={90} y={118} />
      {/* bombilla */}
      <g transform="translate(176 52)">
        <circle r="9" fill={C.sun} />
        <rect x="-4" y="9" width="8" height="5" rx="1" fill={C.ink} />
        <path d="M0 -20v-6M-15 -12l-5-4M15 -12l5-4" stroke={C.sun} strokeWidth="3" strokeLinecap="round" />
      </g>
      {/* planta */}
      <path d="M212 122c-14-6-22-24-12-40 10 8 16 24 12 40z" fill={C.blue} />
      <path d="M214 122c4-22 18-34 34-34-2 18-16 32-34 34z" fill={C.ink} />
      <path d="M212 124c-8-12-4-30 4-38 6 12 6 28-4 38z" fill={C.teal} />
      <path d="M198 124h30l-4 42h-22z" fill={C.sun} />
    </>
  );
}

function EquipoArt() {
  return (
    <>
      <circle cx="30" cy="40" r="11" fill={C.sun} />
      <rect x="60" y="14" width="136" height="52" rx="4" fill={C.white} />
      <Bars x={70} y={58} h={[14, 22, 30, 38]} w={9} colors={[C.blue, C.teal, C.ink, C.sun]} />
      <path d="M150 50l12-12 9 7 16-16" stroke={C.ink} strokeWidth="3.2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <Person x={60} y={92} shirt={C.blue} />
      <Person x={130} y={88} s={1.05} long hair="#5a5a5a" shirt={C.ink} />
      <Person x={200} y={92} long shirt={C.ink} />
      <rect x="120" y="116" width="22" height="10" fill={C.white} stroke={C.ink} strokeWidth="2" />
      <rect x="12" y="124" width="236" height="8" fill={C.ink} />
      <rect x="20" y="132" width="220" height="34" fill={C.blue} />
    </>
  );
}

function LiderazgoArt() {
  return (
    <>
      <path d="M0 166l64-80 72 80z" fill={C.blue} />
      <path d="M70 166l90-118 100 118z" fill={C.ink} />
      <path d="M160 48l-22 29 10 -4 6 8 6-8 8 6 10-2z" fill={C.white} />
      {/* bandera */}
      <path d="M160 48V14" stroke={C.ink} strokeWidth="2.4" />
      <path d="M160 14h22l-6 7 6 7h-22z" fill={C.sun} />
      {/* escaladora */}
      <g transform="translate(176 44)">
        <circle r="7" fill={C.white} stroke={C.ink} strokeWidth="2" />
        <path d="M-7-1c0-6 3-9 7-9s7 3 7 9c-4-2-8-3-14 0z" fill={C.ink} />
        <path d="M-8 8h16v16h-16z" fill={C.teal} />
        <path d="M8 10l8-12" stroke={C.ink} strokeWidth="3" strokeLinecap="round" />
        <path d="M-4 24v14M4 24v14" stroke={C.ink} strokeWidth="3.4" />
      </g>
      {/* escalador */}
      <g transform="translate(116 90)">
        <circle r="6" fill={C.white} stroke={C.ink} strokeWidth="2" />
        <path d="M-6-1c0-5 3-7 6-7s6 2 6 7c-4-2-8-2-12 0z" fill={C.ink} />
        <path d="M-7 7h14v14h-14z" fill={C.blue} />
        <path d="M7 9l7-6" stroke={C.ink} strokeWidth="3" strokeLinecap="round" />
        <path d="M-3 21v12M3 21v12" stroke={C.ink} strokeWidth="3" />
      </g>
    </>
  );
}

function Windows({ x, y, cols, rows, color }: { x: number; y: number; cols: number; rows: number; color: string }) {
  const cells = [];
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) cells.push(<rect key={`${r}-${c}`} x={x + c * 9} y={y + r * 11} width="5" height="6" fill={color} />);
  return <>{cells}</>;
}

function OrganizacionArt() {
  return (
    <>
      <circle cx="210" cy="30" r="11" fill={C.sun} />
      <rect x="48" y="62" width="44" height="98" fill={C.ink} />
      <Windows x={55} y={70} cols={4} rows={8} color={C.white} />
      <rect x="98" y="26" width="58" height="134" fill={C.blue} />
      <Windows x={105} y={34} cols={6} rows={11} color={C.white} />
      <Windows x={105} y={34} cols={1} rows={11} color={C.sun} />
      <rect x="160" y="72" width="44" height="88" fill={C.teal} />
      <Windows x={167} y={80} cols={4} rows={7} color={C.white} />
      <circle cx="30" cy="132" r="13" fill={C.teal} />
      <path d="M30 145v15" stroke={C.ink} strokeWidth="3" />
      <g transform="translate(222 118)">
        <circle r="6" fill={C.white} stroke={C.ink} strokeWidth="2" />
        <path d="M-6-1c0-5 3-7 6-7s6 2 6 7c-4-2-8-2-12 0z" fill={C.ink} />
        <path d="M-7 7h14v16h-14z" fill={C.ink} />
        <path d="M-3 23v14M3 23v14" stroke={C.ink} strokeWidth="3" />
      </g>
      <rect x="14" y="158" width="232" height="6" fill={C.ink} />
    </>
  );
}

function IaArt() {
  return (
    <>
      <Person x={62} y={62} s={1.2} long />
      <rect x="10" y="118" width="120" height="8" fill={C.ink} />
      <rect x="16" y="126" width="108" height="40" fill={C.blue} />
      <Laptop x={64} y={118} chart="line" />
      {/* chispa */}
      <rect x="100" y="26" width="38" height="32" rx="5" fill={C.white} />
      <path d="M119 30c1.5 7 4 9.5 11 11-7 1.5-9.5 4-11 11-1.5-7-4-9.5-11-11 7-1.5 9.5-4 11-11z" fill={C.sun} />
      {/* robot */}
      <g transform="translate(196 0)">
        <path d="M0 12v10" stroke={C.ink} strokeWidth="3" />
        <circle cy="10" r="5" fill={C.sun} />
        <rect x="-26" y="22" width="52" height="40" rx="12" fill={C.blue} />
        <rect x="-18" y="30" width="36" height="22" rx="8" fill={C.ink} />
        <rect x="-11" y="37" width="7" height="7" rx="2" fill={C.white} />
        <rect x="4" y="37" width="7" height="7" rx="2" fill={C.white} />
        <path d="M-6 62h12v8h-12z" fill={C.ink} />
        <rect x="-20" y="70" width="40" height="44" rx="12" fill={C.blue} />
        <circle cy="90" r="8" fill={C.sun} />
        <path d="M-20 84h-24M20 84h24" stroke={C.blue} strokeWidth="9" strokeLinecap="round" />
        <path d="M-9 114v40M9 114v40" stroke={C.ink} strokeWidth="9" />
      </g>
    </>
  );
}

const SCENES: Record<DimensionKey, () => JSX.Element> = {
  persona: PersonaArt,
  equipo: EquipoArt,
  liderazgo: LiderazgoArt,
  organizacion: OrganizacionArt,
  ia: IaArt,
};

export function DimensionIllustration({ dimension }: { dimension: DimensionKey }) {
  const Scene = SCENES[dimension];
  return (
    <svg viewBox="0 0 260 166" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false">
      <Scene />
    </svg>
  );
}

/** Persona presentando un gráfico: esquina del cuadro de mando del hero. */
export function PresenterIllustration() {
  return (
    <svg viewBox="0 0 190 120" aria-hidden="true" focusable="false">
      <ellipse cx="62" cy="88" rx="58" ry="30" fill={C.sky} />
      <circle cx="150" cy="40" r="38" fill={C.sky} />
      <rect x="92" y="18" width="78" height="56" rx="6" fill={C.white} />
      <Bars x={106} y={66} h={[16, 26, 20, 38]} w={9} colors={[C.blue, C.teal, C.ink, C.sun]} />
      <path d="M104 40l16-12 14 8 26-18" stroke={C.ink} strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M174 6c1 5 3 7 8 8-5 1-7 3-8 8-1-5-3-7-8-8 5-1 7-3 8-8z" fill={C.sun} />
      <Person x={44} y={42} s={1.1} />
      <path d="M62 82l28-14" stroke={C.ink} strokeWidth="7" strokeLinecap="round" />
    </svg>
  );
}
