# Desarrollo Local - Configuración de VS Code

Este documento explica cómo configurar tu entorno local para desarrollar DAGs de Airflow con VS Code.

## 🚀 Configuración Rápida

```bash
make setup-local
```

Este comando automatiza toda la configuración necesaria para que VS Code reconozca las importaciones de Airflow.

## ❓ ¿Por qué es necesario?

Airflow se ejecuta **dentro de contenedores Docker**, por lo tanto las bibliotecas de Python (como `airflow`, `apache-airflow-providers-*`, etc.) no están instaladas en tu sistema local. Esto causa que VS Code/Pylance muestre errores como:

```
Import "airflow.providers.standard.operators.python" could not be resolved
```

## ✅ ¿Qué hace `make setup-local`?

1. **Crea un entorno virtual local** (`.venv/`) con Python 3.12+
2. **Instala Apache Airflow 3.1.3** y todos los providers necesarios
3. **Usa las mismas dependencias** que el contenedor Docker ([docker/requirements.txt](docker/requirements.txt))
4. **Configura VS Code** automáticamente ([.vscode/settings.json](.vscode/settings.json))

## 📝 Pasos Posteriores

Después de ejecutar `make setup-local`:

### 1. Recarga VS Code

Presiona `Ctrl+Shift+P` → "Developer: Reload Window"

### 2. Selecciona el Intérprete Python

Presiona `Ctrl+Shift+P` → "Python: Select Interpreter" → Selecciona `.venv/bin/python`

### 3. Verifica

Abre [dags_local/dag_email_manual.py](dags_local/dag_email_manual.py) y verifica que ya no haya errores de importación.

## 🎯 Resultado

Ahora tendrás:

- ✅ **IntelliSense completo** - Autocompletado de código
- ✅ **Type hints** - Sugerencias de tipos
- ✅ **Documentación inline** - Hover sobre funciones para ver docs
- ✅ **Sin errores de importación** - Pylance reconoce todas las bibliotecas

## ⚠️ Importante

El entorno virtual `.venv` es **SOLO para VS Code**:

- ✅ Sirve para IntelliSense y análisis de código
- ❌ **NO se usa** para ejecutar Airflow
- ❌ **NO se versiona** en git (está en `.gitignore`)

**Airflow sigue ejecutándose en Docker** con sus propias dependencias.

## 🔄 Actualizar Dependencias

Si se actualizan las dependencias en [docker/requirements.txt](docker/requirements.txt), ejecuta:

```bash
rm -rf .venv
make setup-local
```

Esto recreará el entorno virtual con las nuevas dependencias.

## 📁 Archivos Relacionados

- [docker/requirements.txt](docker/requirements.txt) - Dependencias de producción (usadas en Docker)
- [.vscode/settings.json](.vscode/settings.json) - Configuración de VS Code
- [.gitignore](.gitignore) - Excluye `.venv` del control de versiones
- [Makefile](Makefile) - Comando `setup-local`

## 🛠️ Troubleshooting

### VS Code sigue mostrando errores

1. Verifica que el intérprete correcto esté seleccionado:
   - Abrir Command Palette: `Ctrl+Shift+P`
   - "Python: Select Interpreter"
   - Debe decir `.venv` o `/home/paxo/air123/.venv/bin/python`

2. Recarga VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"

3. Reinstala el entorno:
   ```bash
   rm -rf .venv
   make setup-local
   ```

### El comando `make setup-local` falla

1. Verifica que Python 3 esté instalado:
   ```bash
   python3 --version
   ```

2. Verifica que `python3-venv` esté instalado:
   ```bash
   sudo apt install python3-venv
   ```

### Errores al instalar dependencias

Si hay errores al instalar `pyodbc` u otras dependencias, es posible que falten bibliotecas del sistema:

```bash
sudo apt-get update
sudo apt-get install -y python3-dev unixodbc-dev
```

Luego vuelve a ejecutar:
```bash
make setup-local
```

## 📚 Más Información

- [docs/dag-development-guide.md](docs/dag-development-guide.md) - Guía completa de desarrollo de DAGs
- [docs/installation-guide.md](docs/installation-guide.md) - Guía de instalación de Airflow
- [README.md](README.md) - Documentación general del proyecto

---

**Última actualización:** 2025-11-18