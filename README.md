# NewsMaster
[![CodeQL Production](https://github.com/technocapeman/NewsMaster/actions/workflows/codeql_main.yml/badge.svg)](https://github.com/technocapeman/NewsMaster/actions/workflows/codeql_main.yml)
[![CodeQL Development](https://github.com/technocapeman/NewsMaster/actions/workflows/codeql_dev.yml/badge.svg)](https://github.com/technocapeman/NewsMaster/actions/workflows/codeql_dev.yml)

NewsMaster is an open-source, cross-platform news app founded by Kapilesh Pennichetty and Sanjay Balasubramanian, and
currently maintained by Kapilesh Pennichetty. It is a website and a Progressive Web Application developed on the Flask
Web Framework for Python.

Features:

- Trending News: Shows international trending news on the home page.
- News Search (Powered by Google Programmable Search Engine): Allows you to search for news articles.
- Automatic Weather: Detects your location using your IP address, and gives you the current weather information for your
  location.
- Weather Search: Allows you to search for the current weather at any location in the world.
- Weather Advice Features: Temperature and Precipitation Advice features advise you about safe practices for your
  current weather.

To use the application, please visit [thenewsmaster.herokuapp.com](thenewsmaster.herokuapp.com)!

## Production Workflow

1. Commits are pushed and tested on the downstream dev branch. CodeQL scanning will automate security testing of the
   code, and the code will be manually tested for stability.
2. Once all commits have been thoroughly tested for stability and security, a pull request will be made to the upstream
   main branch.
3. Once all checks have passed, the commits will be merged into the upstream main branch. A GitHub action will then
   automatically deploy the main branch to production.

**PLEASE NOTE**: The code to retrieve IP addresses is different between the dev and main branches. This is because the
code used to retrieve IP addresses in production will fail when testing on a local machine, and likewise, the code used
for testing locally is not appropriate for production. Therefore, when a pull request or commit is issued to the
repository, the repository's GitHub Actions will automatically find and replace this code according to the branch.

## Contributions

Contributions to NewsMaster are greatly appreciated. Please abide by the following guidelines when contributing:

1. Please contribute to the dev branch of this repository rather than the main branch which is used for production.
2. Please ensure that your code is well-documented and well-formatted.
3. When making a Pull Request, please enable "Allow edits from maintainers." This allows for the aforementioned GitHub
   Actions to find and replace the appropriate IP address code, and for maintainers to make modifications if needed.

Thank you for contributing to NewsMaster!

## Credits

Special thanks to [Mr. Bailey Hulsey](https://github.com/BaileyH) for educating and inspiring us with his knowledge of
computer science!
