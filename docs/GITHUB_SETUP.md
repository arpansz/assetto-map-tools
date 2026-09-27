# GitHub setup checklist

## Before the first push

1. GitHub owner is configured as **[@arpansz](https://github.com/arpansz)**.
2. Project author and MIT copyright holder are set to **Arpan Hansda**.
3. Pick a repository description, for example:
   `Validation and diagnostics for Assetto Corsa map-building workflows.`
4. Suggested GitHub topics:
   `assetto-corsa`, `modding`, `blender`, `track-modding`, `3d`, `obj`, `python`, `validator`.

## Create and push the repository

From the extracted project directory:

```bash
git init
git add .
git commit -m "Initial release: acvalidate v0.1"
git branch -M main
git remote add origin https://github.com/arpansz/assetto-map-tools.git
git push -u origin main
```

Or create the empty repository first in GitHub, then follow the commands GitHub displays.

## Recommended GitHub settings

- Keep the repository public if the goal is open-source collaboration.
- Enable Issues.
- Enable Discussions once there are users who need support or want to propose rules.
- Protect `main` later if outside contributors begin sending pull requests.
- Add a short screenshot/GIF only after the CLI output is stable.

## First release

After validating the repository on your own project:

1. Create a tag such as `v0.1.0`.
2. Create a GitHub Release from that tag.
3. Copy the relevant section of `CHANGELOG.md` into the release notes.
4. Do not claim FBX/KN5 support until those paths are implemented and tested.
