# jirib's Scoop bucket

A personal [Scoop](https://scoop.sh) bucket. Currently provides:

| App       | Description                                        |
| --------- | -------------------------------------------------- |
| `context` | [ConTeXt LMTX](https://www.contextgarden.net/) typesetting system (Windows x64) |

## Adding the bucket

```powershell
scoop bucket add jirib https://github.com/jirib/scoop-bucket
```

## Installing ConTeXt LMTX

```powershell
scoop install context
```

This downloads the official `context-win64.zip` bootstrap and runs the
cross-platform `mtx-install.lua` installer, which populates the full ConTeXt
tree under `tex/texmf-win64/` and generates the cache and formats. No need to
run `install.bat` / `setpath.bat` or edit your PATH manually.

After installation, `mtxrun` and `context` are shimmed, and the whole
`tex\texmf-win64\bin` directory is added to your PATH:

```powershell
mtxrun --version
context --version
```

## Updating

ConTeXt LMTX is a rolling release with no semantic versions. The manifest
version tracks the upstream build date, so:

```powershell
scoop update context
```

will detect a newer build (via `tex/status.tma`) and re-run the installer to
pull the latest tree.
