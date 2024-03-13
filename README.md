# New Relic Synthetics Scripts

## A collection of custom scripts to manage New Relic Synthetic Monitors using the NerdGraph API, mainly Scripted API synthetics

`Python 3.7+` is required.

### Automated install

**Copy and paste into your terminal:**

```sh
curl https://gist.githubusercontent.com/GorillaBearWolf/c7690697fafb16aa13a38328b3a4a91a/raw/276089b79d7b15017e1eede6db1cdca3c26f6060/new_relic_scripts_install.sh | sh
```

#### Install script link

<https://gist.github.com/GorillaBearWolf/c7690697fafb16aa13a38328b3a4a91a>

### Manual install

- Clone the repo
- `cd` to the download location
- `sudo chmod +x setup.sh`
- `./setup.sh`

### Post-install

**In download location:**

1. Set the values of `NEW_RELIC_API_KEY` and `NEW_RELIC_ACCOUNT_ID` in `.env`
2. `source .venv/bin/activate`

### Todo

- [ ] Comments/docstrings
- [ ] `setup.py`
- [ ] Improve Javascript
- [ ] Improve packaging
- [x] Authorization via environment variable
  - [x] `setup.sh`
  - [x] `os` module
  - [x] `python-dotenv`
