// Todo el texto de la landing vive aquí: los componentes solo presentan.

export type DimensionKey = 'persona' | 'equipo' | 'liderazgo' | 'organizacion' | 'ia';
export type IconName = 'user' | 'users' | 'flag' | 'grid' | 'sparkle';

export interface Dimension {
  key: DimensionKey;
  title: string;
  question: string;
  icon: IconName;
}

export const nav = [
  { href: '#que-evaluamos', label: 'Qué evaluamos' },
  { href: '#como-funciona', label: 'Cómo funciona' },
  { href: '#vistas', label: 'Vistas' },
];

export const hero = {
  lead: 'Descubre las competencias de los lideres, los equipos y las personas de tu organizacion, su experiencia en el trabajo y el grado de madurez agil y del uso de la IA.',
  cta: 'Hablemos de un piloto en tu organización',
  dashboardTitle: 'Tu cuadro de mando',
  dashboardNote: 'Vistas de ejemplo con datos ilustrativos.',
};

export const dimensions: Dimension[] = [
  { key: 'persona', title: 'Personas', question: '¿Puedo organizarme, priorizar y aprender?', icon: 'user' },
  { key: 'equipo', title: 'Equipos', question: '¿Trabajamos con objetivos compartidos y confianza?', icon: 'users' },
  { key: 'liderazgo', title: 'Liderazgo', question: '¿Aporta propósito, autonomía y desarrollo?', icon: 'flag' },
  { key: 'organizacion', title: 'Organización', question: '¿Decidimos, innovamos y creamos valor con evidencia?', icon: 'grid' },
  { key: 'ia', title: 'IA transversal', question: '¿Usamos la IA de forma útil, crítica, segura y responsable?', icon: 'sparkle' },
];

export const assessment = {
  title: 'Qué evaluamos',
  items: [
    {
      title: 'Conductas observables',
      body: '180 conductas, 60 competencias y 13 metacompetencias, con tres ítems por competencia.',
    },
    {
      title: 'Ocho indicadores clave',
      body: 'Una lectura ejecutiva con indicadores de cada metacompetencia agil. La IA impacta transversalmente en cada una de las dimensiones.',
    },
    {
      title: 'Vínculo con la organización',
      body: 'El eNPS y el flow indican el grado de compromiso y bienestar organizativo.',
    },
  ],
};

export const process = {
  title: 'Un proceso para la acción',
  steps: [
    { title: 'Evaluar', body: 'Cuestionario por bloques' },
    { title: 'Comprender', body: 'Fortalezas y prioridades' },
    { title: 'Actuar', body: 'Plan con responsables' },
    { title: 'Revisar', body: 'Comparar dos mediciones compatibles' },
  ],
};

// Una vista (cuadro de mando) por dimensión competencial; textos = subtítulos de DASHBOARDS en centro-de-mando/app/dashboard.py.
export const views: { title: string; items: { key: DimensionKey; title: string; body: string }[]; indicators: string[] } = {
  title: 'Una vista para cada dimensión competencial',
  items: [
    { key: 'persona', title: 'Persona', body: 'Conoce tus competencias y planifica tu desarrollo' },
    { key: 'equipo', title: 'Equipo', body: 'Contribución individual al equipo, agregada sin exponer respuestas individuales' },
    { key: 'liderazgo', title: 'Liderazgo', body: 'Tu autopercepción junto a la percepción que recibes de tu equipo' },
    { key: 'organizacion', title: 'Organización', body: 'Lectura ejecutiva con evidencia y respeto por el anonimato' },
    { key: 'ia', title: 'IA transversal', body: 'Aumentar capacidades de forma útil, crítica, segura y responsable' },
  ],
  indicators: [
    'Capacidad',
    'Evidencia',
    'Personas',
    'Propósito',
    'Cliente',
    'Flujo',
    'Aprendizaje',
    'Responsabilidad',
    'Transferencia',
    'Bienestar',
    'Impacto',
  ],
};

export const pilotNotice = {
  title: 'Instrumento en fase piloto.',
  body: 'Los resultados son descriptivos y sirven para el desarrollo; no se usan para selección, promoción ni sanción. La validación psicométrica está en curso.',
};

export const footer = 'Instrumento piloto · datos ilustrativos · pendiente de validación · Agile Institute™';

export const organizationSizes = [
  { value: '<50', label: 'Menos de 50 personas' },
  { value: '50-250', label: 'Entre 50 y 250' },
  { value: '250-1000', label: 'Entre 250 y 1000' },
  { value: '>1000', label: 'Más de 1000' },
];
