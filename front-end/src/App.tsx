import { useState } from 'react';
import { Assessment } from './components/Assessment';
import { Closing } from './components/Closing';
import { Dimensions } from './components/Dimensions';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { PilotModal } from './components/PilotModal';
import { Process } from './components/Process';
import { Roles } from './components/Roles';
import { useReveal } from './hooks/useReveal';

export default function App() {
  const [pilotOpen, setPilotOpen] = useState(false);
  const openPilot = () => setPilotOpen(true);
  useReveal();

  return (
    <>
      <a className="skip-link" href="#main">
        Saltar al contenido
      </a>
      <Header />
      <main id="main">
        <Hero onCta={openPilot} />
        <Dimensions />
        <Assessment />
        <Process />
        <Roles />
        <Closing onCta={openPilot} />
      </main>
      <PilotModal open={pilotOpen} onClose={() => setPilotOpen(false)} />
    </>
  );
}
