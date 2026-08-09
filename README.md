# LLUVIA's THINGS ABOUT WORLD

Personal Jekyll blog for `https://guoziqiang198.github.io`, based on the open-source Hux Blog theme.

## Publish with GitHub Pages

1. Push this directory to the public repository `GuoZiqiang198.github.io`.
2. Open **Settings → Pages** in the GitHub repository.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Select `main` and `/(root)`, then wait for `pages build and deployment` to complete.
5. Visit `https://guoziqiang198.github.io`.

## Write a post

Create a Markdown file under `_posts/` using this filename format:

```text
YYYY-MM-DD-post-slug.md
```

## Preview locally

Ruby is installed at `E:\TOOLS\Ruby34-x64`. It was intentionally not added to the permanent Windows `PATH`. In each new PowerShell window, run:

```powershell
$env:Path = 'E:\TOOLS\Ruby34-x64\bin;' + $env:Path
cd E:\Codex\GuoZiqiang198.github.io
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

Then open `http://127.0.0.1:4000`. Press `Ctrl+C` in the terminal to stop the preview server.

To generate the static site without starting a server:

```powershell
$env:Path = 'E:\TOOLS\Ruby34-x64\bin;' + $env:Path
cd E:\Codex\GuoZiqiang198.github.io
bundle exec jekyll build
```

The generated files are written to `_site\`.

## Validate the project structure

Use the selected Python 3.9 environment:

```powershell
& 'D:\miniconda3\envs\python39\python.exe' scripts\validate_site.py
```

This checks the site configuration, front matter, required assets, `CNAME`, and leftover upstream tracking identifiers. Run it alongside the full Jekyll build above.

## Personalization checklist

- Edit `_config.yml` to change the description and social links.
- Edit `about.html` to replace the starter biography.
- Replace `img/lluvia-rain-header.png` if you prefer another header image.
- Review and preview each new post before pushing it.

## Attribution

The layout is based on [Hux Blog](https://github.com/Huxpro/huxpro.github.io), licensed under Apache License 2.0. The upstream `LICENSE` file and theme attribution are preserved.
