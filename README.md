# Zhongjiang Yao

Academic homepage for Zhongjiang Yao, postdoctoral researcher at King's College London. [GitHub Pages](https://yaozhongjiang.github.io/) publishes this Jekyll site from the `main` branch.

## Pages

- **Home** (`/`) — biography, recent activities, and papers from the latest publication year.
- **Publications** (`/publication/`) — journal papers, conference papers, preprints, and citation counts.
- **Work** (`/work/`) — positions and patents.
- **Contact** (`/contact/`) — email and address.

## Publication refresh

[Update publications](.github/workflows/update-publications.yml) runs every four months, at 08:00 UTC on 1 January, 1 May, and 1 September. It reads the ORCID in [`_config.yml`](_config.yml) and refreshes [`_data/publications.yml`](_data/publications.yml) from OpenAlex and Semantic Scholar.

## Local preview

Install Ruby, RubyGems, GCC, and Make ([Jekyll requirements](https://jekyllrb.com/docs/installation/#requirements)). Dependencies are the `github-pages` gem in the [Gemfile](Gemfile) (`~> 232`).

```bash
bundle install
bash run_server.sh
```

Then open [http://127.0.0.1:4000](http://127.0.0.1:4000). On Windows, run `run_server.bat` instead of `run_server.sh`.
