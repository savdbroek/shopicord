<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/savdbroek/shopicord">
    <img src="images/shopicord.png" alt="Logo" width="120" height="120">
  </a>

<h3 align="center">Shopicord</h3>

  <p align="center">
    A Discord bot to retrieve Shopify Orders and Statistics
    <br />
    <a href="https://github.com/savdbroek/shopicord"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/savdbroek/shopicord/issues">Report Bug</a>
    ·
    <a href="https://github.com/savdbroek/shopicord/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#setup-discord-bot">Setup Discord bot</a></li>
        <li><a href="#setup-shopify-app">Setup Shopify App</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple Discord bot I developed to keep track of orders on my own Shopify Store. It was my first Python project and never intended for the public.
However, I feel like it might be of use to someone out there. I will be going through the code eventually to optimize it.

Please let me know if you find any bugs or have feature requests!




### Built With

* [![Python][Python.org]][Python-url]




<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The following things are required before using this project.
* Docker
* Shopify Store
* Discord Server
* API-Ninjas Key (free) [https://api-ninjas.com/](https://api-ninjas.com/)
* Setup Discord Bot - <a href="#discord-bot">Setting up a Discord Bot/a>
* Setup Shopify App - <a href="#shopify-app">Setting up a Shopify App</a>

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/savdbroek/shopicord.git
   ```
2. Edit the .env file in /app
   ```sh
   nano app/.env
   ```
3. Add your Discord ID to authors list in bot.py
   ```python
   authors = [YOUR DISCORD ID('s)]
   ```
4. Build & Run the Container
   ```sh
   docker run -it $(docker build -q .)
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Setup Discord Bot -->
### Setup Discord Bot

Use the following page to create your own Discord Bot:

[https://discordpy.readthedocs.io/en/stable/discord.html](Creating a Discord bot)

You need your Bot Token.

<!-- Creating Shopify App -->
### Setup Shopify App

Don't worry you won't need to do anything complicated. Just open up your Shopify Admin page and follow along.

1. Open Settings
2. Open Apps and sales channels
3. Click Develop Apps
4. Click Create an App
5. Give your App a beautiful name (Does not matter what)
6. Click Create App
7. Click Configure Admin API Scope
8. Check the following boxes:
   * read_analytics
   * read_assigned_fulfillment_orders
   * read_customers
   * read_inventory
   * read_orders
   * read_product_listings
   * read_products
   * write_reports
   * read_reports
   * read_shopify_payments_payouts
9. Click Save
10. Click API Credentials
11. Click Install App
12. Click Reveal token once
13. Copy your Shopify API Token
14. Paste your Shopify API Token into app/.env


<!-- USAGE EXAMPLES -->
## Usage

Currently there two commands:

* !orders - Display a list of all current open orders + show closed orders from current month and current balance
* !order order_# - Takes order number as argument. Shows information abou the order.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Optimize and cleanup code
- [ ] You name it ;)

See the [open issues](https://github.com/savdbroek/shopicord/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sander van den Broek - savdbroek@proton.me

Project Link: [https://github.com/savdbroek/shopicord](https://github.com/savdbroek/shopicord)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [https://github.com/othneildrew/Best-README-Template](Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/savdbroek/shopicord.svg?style=for-the-badge
[contributors-url]: https://github.com/savdbroek/shopicord/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/savdbroek/shopicord.svg?style=for-the-badge
[forks-url]: https://github.com/savdbroek/shopicord/network/members
[stars-shield]: https://img.shields.io/github/stars/savdbroek/shopicord.svg?style=for-the-badge
[stars-url]: https://github.com/savdbroek/shopicord/stargazers
[issues-shield]: https://img.shields.io/github/issues/savdbroek/shopicord.svg?style=for-the-badge
[issues-url]: https://github.com/savdbroek/shopicord/issues
[license-shield]: https://img.shields.io/github/license/savdbroek/shopicord.svg?style=for-the-badge
[license-url]: https://github.com/savdbroek/shopicord/blob/master/LICENSE
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
