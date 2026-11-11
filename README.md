
# devdoctor

A lightweight CLI tool for checking your development environment.

devdoctor helps developers quickly inspect their operating system and installed development tools.

## Features

- Detect operating system and CPU architecture
- Check the current Python interpreter version
- Check Git, uv, Docker CLI, and fzf
- Report missing tools and command execution errors
- Run without administrator privileges
- Work offline

devdoctor does not modify your system configuration.

## Requirements

- Python 3.12 or later
- Linux or macOS
- uv (recommended)

## Installation

Clone the repository:

```bash
git clone https://github.com/zorac-dev/devdoctor.git
cd devdoctor
```

Run with uv:

```bash
uv run devdoctor check
```

## Usage

Check your development environment:

```bash
uv run devdoctor check
```

Example output:

```text
devdoctor v0.1.0
────────────────────────────────
SYSTEM
  OS       Ubuntu 26.04
  Arch     x86_64

DEVELOPMENT TOOLS
  Python   OK       3.12.16
  Git      OK       2.47.0
  uv       OK       0.9.0
  Docker   OK       29.0.0
  fzf      MISSING  Not installed
────────────────────────────────
4 installed / 1 missing / 0 errors
```

Show help:

```bash
uv run devdoctor --help
```

Show version:

```bash
uv run devdoctor --version
```

## Development

Install development dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest -v
```

Check code quality:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Limitations

- Docker checks only verify the Docker CLI version.
- The Docker daemon is not checked.
- The Python check reports the interpreter running devdoctor.
- Windows support has not yet been verified.

## Contributing

Bug reports, suggestions, and pull requests are welcome.

Please open an issue before proposing major changes.

## License

MIT License. See [LICENSE](LICENSE).

