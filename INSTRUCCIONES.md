# 🎱 Baloto Stats — Guía completa de instalación

## Estructura del proyecto
```
baloto-full/
├── index.html                      ← App PWA principal
├── manifest.json                   ← Config instalable
├── sw.js                           ← Offline / caché
├── data/
│   └── resultados.json             ← Historial de sorteos (se actualiza solo)
├── scripts/
│   └── scraper.py                  ← Bot que raspa resultados reales
└── .github/
    └── workflows/
        └── actualizar.yml          ← Automatización 3x por semana
```

---

## PASO 1 — Crear cuenta en GitHub (gratis)

1. Ve a → https://github.com/signup
2. Elige un usuario, correo y contraseña
3. Verifica tu correo
4. ¡Listo! Tienes cuenta de GitHub

---

## PASO 2 — Crear el repositorio

1. En GitHub, haz clic en el botón verde **"New"** (arriba a la izquierda)
2. Nombre del repo: `baloto-stats`
3. Marca **"Public"** (necesario para GitHub Pages gratis)
4. Haz clic en **"Create repository"**

---

## PASO 3 — Subir los archivos

### Opción A — Desde la web (sin instalar nada)

1. En tu repo vacío, haz clic en **"uploading an existing file"**
2. Arrastra TODOS los archivos y carpetas del ZIP descomprimido
3. En el campo "Commit changes" escribe: `Subir app Baloto Stats`
4. Clic en **"Commit changes"**

> ⚠️ **Importante:** GitHub no acepta carpetas vacías. Asegúrate de subir
> los archivos dentro de `.github/workflows/` manualmente si la web no los detecta.
> Para subir archivos ocultos (.github): usa GitHub Desktop (ver Opción B).

### Opción B — GitHub Desktop (recomendado)

1. Descarga → https://desktop.github.com
2. Inicia sesión con tu cuenta
3. Clic en **"Add" → "Add existing repository"**
4. Selecciona la carpeta `baloto-full`
5. Clic en **"Publish repository"**
6. Asegúrate que sea **Public** → **Publish**

---

## PASO 4 — Activar GitHub Pages

1. En tu repo, ve a **Settings** (pestaña arriba)
2. En el menú izquierdo: **Pages**
3. En "Source" elige: **Deploy from a branch**
4. Branch: **main** / Folder: **/ (root)**
5. Clic en **Save**
6. Espera ~2 minutos
7. Tu app queda en: `https://TU_USUARIO.github.io/baloto-stats`

---

## PASO 5 — Verificar la automatización

1. En tu repo ve a la pestaña **Actions**
2. Verás el workflow **"Actualizar resultados Baloto"**
3. Para probarlo ahora: clic en el workflow → **"Run workflow"** → **"Run workflow"**
4. Verás el log en tiempo real. Si el scraper obtiene datos nuevos, hace commit automático

El bot corre automáticamente:
- **Martes noche** (después del sorteo de Baloto/Revancha)
- **Jueves noche** (después del sorteo de Miloto)
- **Viernes noche** (después del sorteo de Baloto/Revancha)

---

## PASO 6 — Instalar en tu celular

### Android (Chrome)
1. Abre `https://TU_USUARIO.github.io/baloto-stats` en Chrome
2. Toca el menú ⋮ → **"Instalar app"** o **"Agregar a pantalla de inicio"**
3. Ya aparece como app en tu pantalla principal

### iPhone/iPad (Safari obligatorio)
1. Abre la URL en **Safari**
2. Toca el botón compartir **□↑**
3. **"Añadir a pantalla de inicio"** → Añadir

---

## ¿Qué pasa si el scraper no puede obtener datos?

No pasa nada malo. El scraper está diseñado para ser conservador:
- Si no logra conectarse al sitio → NO modifica `resultados.json`
- Si obtiene datos pero ya existen para esa fecha → NO duplica
- Los datos históricos del ZIP inicial siempre estarán disponibles

En ese caso la app sigue funcionando con los datos que ya tiene.

---

## Personalizar colores o nombre

En `index.html` busca `:root {` y cambia:
```css
--blue: #4a8fff;    /* color principal */
--green: #3ecf8e;   /* color Miloto */
--purple: #a78bfa;  /* color Revancha */
```

Para cambiar el nombre busca `Baloto Stats` y reemplázalo.
