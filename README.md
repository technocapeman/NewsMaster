# NewsMaster
NewsMaster is an open-source, cross-platform news app founded by Kapilesh Pennichetty and Sanjay Balasubramanian and currently maintained by Kapilesh Pennichetty. It is a website and a Progressive Web Application developed on the Flask Web Framework for Python.

Features:
- Trending News: Shows international trending news on the home page.
- News Search (Powered by Google Programmable Search Engine): Allows you to search for news articles.
- Automatic Weather: Detects your location using your IP address, and gives you the current weather information for your location.
- Weather Search: Allows you to search for the current weather at any location in the world.
- Weather Advice Features: Temperature and Precipitation Advice features advise you about safe practices for your current weather.

To use the application, please visit [thenewsmaster.herokuapp.com](thenewsmaster.herokuapp.com)!

## Production Workflow
1. Commits are pushed and tested on the downstream dev branch.
2. Once all commits have been thoroughly tested for stability, a pull request will be made to the upstream main branch.
3. Once all checks have passed on the pull request, the commits will be merged into the upstream main branch. An action will automatically deploy the changed main branch to production.

Please note that the code to retrieve IP addresses is different between the dev and the main branches. This is because the code used to retrieve IP addresses in production will not work for testing on a local machine, and likewise, code used for testing will not work for production. Therefore, when a pull request or commit is made to the repository, actions will automatically find and replace this code depending on the branch.

## Contributions
Contributions (such as Pull Requests and Issues) to NewsMaster are greatly appreciated. Please contribute to the dev branch of this repository rather than the main branch which is used for production.
