### The hammerdirt! API

#### Purpose

The hammerdirt! API recieves, stores and provides access to data from hammerdirt! projects

#### Use

This API is part of the hammerdirt! infrastructure. Provides POST/PUT/GET endpoints for project data.

### The hammerdirt infrastructure:

These are the main components of the hammerdirt! infrastructure:

1. Data storage and distribution through the API:
  * api url: [https://mwshovel.pythonanywhere.com/](https://mwshovel.pythonanywhere.com/)
  * repo: this repo
  * Authenticated members can enter survey data and edit articles
  * Provides endpoints for client apps
  * Powered by Django REST
2. Data entry and management:
  * url: [https://www.hammerdirt.ch/](https://www.hammerdirt.ch/)
  * repo: [https://github.com/hammerdirt/pwa](https://github.com/hammerdirt/pwa)
  * Has access to POST and PUT endpoints
  * Includes WYISWYG editor by TinyMCE
  * Forms for entering survey data and commenting on articles
  * Built with ReactJS
3. Data visualisation, communication:
  * url: [https://www.plagespropres.ch/](https://www.plagespropres.ch/)
  * repo: [https://github.com/hammerdirt/client_pwa](https://github.com/hammerdirt/client_pwa)
  * Has access to GET endpoints
  * Built with ReactJS
4. Version control and collaboration:
  * version control : Git
  * collaboration: GitHub
  * url:[https://github.com/hammerdirt](https://github.com/hammerdirt) 

### About hammerdirt!

Hammerdirt! is a non-profit organisation based in Switzerland and dedicated to the collection, analysis and distribution of environmental data.

### About the API

This app is specifically designed to provide data-entry and text editing capabilities for ongoing environmental surveillance projects. Display and communication happens through the client app.

1. Stores data for hammerdirt projects
2. Provides authentication services

### Contributing 

1. Log your issues through GitHub in the usual way
2. If you have a fix submit a pull request 

### Joining hammerdirt!

1. see hammerdirt.ch in the docs tab "members"
