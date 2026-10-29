import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';
import { dimensions, roles } from '../content/landing';

describe('Landing', () => {
  afterEach(() => vi.restoreAllMocks());

  it('muestra el titular, las cinco dimensiones y los seis roles', () => {
    render(<App />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(/responsable de la\s*IA/);
    const panel = screen.getByRole('complementary', { name: 'Tu cuadro de mando' });
    expect(within(panel).getAllByRole('link')).toHaveLength(dimensions.length);
    for (const role of roles.items) expect(screen.getByRole('heading', { name: role.title })).toBeInTheDocument();
    expect(screen.getByRole('note')).toHaveTextContent('Instrumento en fase piloto.');
  });

  it('valida el formulario de piloto antes de enviarlo', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch');
    render(<App />);
    await userEvent.click(screen.getAllByRole('button', { name: /Hablemos de un piloto/ })[0]);
    await userEvent.click(screen.getByRole('button', { name: /Enviar solicitud/ }));
    expect(screen.getByText('Indica tu nombre.')).toBeInTheDocument();
    expect(screen.getByText('Necesitamos tu consentimiento para contactarte.')).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('envía la solicitud al BFF y muestra la confirmación', async () => {
    const fetchSpy = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue(new Response(JSON.stringify({ id: 'abc' }), { status: 201 }));
    render(<App />);
    await userEvent.click(screen.getAllByRole('button', { name: /Hablemos de un piloto/ })[0]);
    await userEvent.type(screen.getByLabelText('Nombre'), 'Ana Pérez');
    await userEvent.type(screen.getByLabelText('Correo de trabajo'), 'ana@empresa.es');
    await userEvent.type(screen.getByLabelText('Organización'), 'Empresa S.A.');
    await userEvent.click(screen.getByRole('checkbox'));
    await userEvent.click(screen.getByRole('button', { name: /Enviar solicitud/ }));

    expect(await screen.findByText(/Hemos recibido tu solicitud/)).toBeInTheDocument();
    const [url, init] = fetchSpy.mock.calls[0];
    expect(url).toBe('/api/pilot-requests');
    expect(JSON.parse(init!.body as string)).toMatchObject({ email: 'ana@empresa.es', consent: true });
  });
});
