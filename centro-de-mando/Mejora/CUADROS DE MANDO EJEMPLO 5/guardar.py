from pathlib import Path
import shutil,zipfile
from PIL import Image
source=Path('C:/Users/AntonioCano/.codex/generated_images/01a15387-8db8-76f1-8076-799fb1a337d1')
dest=Path('outputs/propuestas_visuales_v1');dest.mkdir(parents=True,exist_ok=True)
files=[('exec-ec22560d-ad9d-4bec-8719-e3195e54300d.png','01_Persona_Propuesta.png'),('exec-4f19eea8-7db4-48ff-9220-44a0fd70099b.png','02_Equipo_Propuesta.png'),('exec-3da1acaf-d7a7-4e91-8858-419fc1eda467.png','03_Liderazgo_Propuesta.png'),('exec-6f5ee10d-7456-4e71-8313-ec62625d47d8.png','04_Organizacion_Propuesta.png'),('exec-655b71dd-ac31-4858-9ea1-18eaae080116.png','05_IA_Propuesta.png')]
for original,name in files:
    shutil.copy2(source/original,dest/name)
    with Image.open(dest/name) as im:print(name,im.size)
note='''PROPUESTAS VISUALES · AGILE INSTITUTE

Cinco maquetas: Persona, Equipo, Liderazgo, Organización e IA transversal.
Generadas con la herramienta integrada de imágenes, usando las cinco referencias visuales facilitadas por el usuario para conservar su marca e imagen.

Son propuestas gráficas con datos DEMO, no resultados reales ni una aplicación funcional.
Integran indicadores de bienestar y experiencia laboral; no representan una escala global validada de bienestar o Flow.
Los gráficos y textos sirven para revisar la composición y el diseño. Su implementación debe utilizar los datos y reglas del Excel vigente.
Los rótulos heredados de las referencias, como Base en Excel v3.0, son parte de la maqueta; deberán actualizarse a la versión vigente al implementar.

Los PNG son imágenes de referencia, no pantallas interactivas ni archivos editables por capas.
Se incluyen los prompts empleados para facilitar futuras revisiones.
'''
(dest/'LEEME.txt').write_text(note,encoding='utf-8-sig')
archive=dest/'Propuestas_visuales_Agile_Institute_5_cuadros.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for _,name in files:z.write(dest/name,name)
    z.write(dest/'LEEME.txt','LEEME.txt')
    if (dest/'Prompts_utilizados.txt').exists():z.write(dest/'Prompts_utilizados.txt','Prompts_utilizados.txt')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(archive.resolve())
