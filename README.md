# K-Punk blog scraper

Scraping Mark Fisher's blog for tagging and graphing via Logseq.

## Environment

*I use Powershell on Windows, with Python3 installed*.

1. `python3 -m venv venv`
2. `.\venv\Scripts\Activate.ps1`
3. `python .\Kpunkspi\run_spi.py`

## Working log

1. Tidied up the repo
2. Read through the scapy docs on [Spiders](https://docs.scrapy.org/en/latest/topics/spiders.html).
3. Decided on the parsing model:
    - `parse` will scape the archive section to collect a list of archive months
    - `parse_month` will scape the list of posts and collects their links
    - `parse_post` will read each post and scrapes it's content.
4. Implemented the above in `kpunk.py`.

## [Original Repo](https://github.com/Connor-Scott/WordPress_blog_scraper) readme

### Effective Strategies for Data Extraction with Web-Scraping

- This was posted to my Substack Blog Chi2Snake or "KySnek," a pseudonym that was at one point associated with this GitHub Profile too.

- What perplexes me about most articles you’ll find when you google “web scraping with Python” is how many articles insist on using Selenium.
  - Don’t get me wrong the Python Selenium API has its place but for fast, scalable web scraping it most likely isn’t what you’re looking for.
  - It was originally intended for developers looking to test their webpages.
  - That original use shows when you try to let it loose on a bunch of websites.
  - If those webpages happen to heavily rely on JavaScript it’s a viable option, though I suspect most people really need another library.

- The best library for web scraping is Scrapy in my opinion.
  - It has inbuilt support for importing settings, custom middleware, and pipeline data processing protocols.
  - Best of all, Scrapy is very fast, even faster if you turn off auto-throttling and maximize the number of concurrent requests you let it execute.

- If you just need to import a single document, use the requests library.
  - For any task that can truly be called web scraping, you’re best bet is to use Scrapy.
  - A notable limitation of Scrapy however is its lack of built-in tools for directly interacting with JavaScript-generated content.
  - Any webpage that buries links in a backend databases and requires a user to send requests to navigate to other pages needs a slightly different approach.
  - For anything that needs JavaScript heavy web automation I recommend using the Playwright library.
  - If you need it to be fast and scalable you should use the asynchronous extension.
  - Beautifulsoup is another good option but I’ve found it’s API less user friendly than Playwright’s.
  - It’s also primarily a parsing library.
  - These are great options if you don’t have a large number of individual pages to scrape.
  - They also require less work in many cases than Scrapy.
  - The work you put into Scrapy does result in a huge payoff for scalability and speed.

- To set up a Scrapy implementation use this file architecture or something similar:

  ```plaintext
  scrapyProject/
  ├── scrapyProject/
  │   ├── __init__.py
  │   ├── items.py
  │   ├── middlewares.py
  │   ├── pipelines.py
  │   ├── settings.py
  │   └── spiders/
  │       ├── __init__.py
  │       ├── spider1.py
  │       └── spider2.py
  └── scrapy.cfg
  ```

- Inside the spider files you’ll make classes for each spider and set up the scraping architecture.
  - Integrating Playwright with Scrapy is feasible, though implementing Playwright asynchronously within Scrapy is challenging due to its concurrent asynchronous operations.
  - An approach I’ve taken is sending out an asynchronous Playwright program to scout the territory before sending in Scrapy spiders.
  - But this is ideal only if the webpages they link to contain links to other sites in its html content.
  - Otherwise your best bet for sites that rely entirely on client-side scripting with JavaScript is it to just design a Playwright implementation to gather content.

- If you have a site that uses JavaScript often but not entirely you’ll benefit from using both.
  - Do this by inserting Playwright code inside of a Scrapy spider.
  - This should be done with Playwright’s synchronous API to avoid overloading Scrapy.
  - However, this can slow your program down.
  - To fix this you can adjust the wait time playwright uses to load content and/or use a while loop to have it quit once your function finds the link they’re looking for.
  - Yielding the web content your after is best gathered with Scrapy’s modules, it’s ever so slightly faster.

- Yielding content is best done with the relative xpaths or the css related to the content you want.
  - An xpath that’s too exact won’t generalize to similar sites, in many cases even if the webpage has the exact same layout.
  - Testing these prior to letting your spiders loose is ideal.
  - Otherwise you’ll end up with a bunch of trash database entries.
  - You could use the console on your favorite browser’s dev tools but I’ve found that sometimes the commands don’t transfer cleanly.
  - Loading a Scrapy interpreter in your terminal makes for convenient testing.
  - This approach allows you to test the relative path using Scrapy functions and sub-functions in a single step.
  - Then just copy that line into the spider class’s function your building.
  - It’s an ideal place to test out your code.
  - If you do run into an error when that spider runs or get peculiarities in your data then 99% of the time it isn’t because of that line of code.
  - Usually the guilty line of code is inside the pipeline’s processing functions when the spider finds a contingency I didn’t outline a conditional for.
  - Other times it’s in the yield statement.

- Another very attractive component of the Scrapy library is proxy rotation.
  - They don’t provide any proxies, it’s outside the scope of the library, but if you’re IP address is getting banned by an overprotective web admin protocol this is an invaluable tool.
  - There are many proxies available for free too.
  - You can even web scrape lists of them from various sites! Then point Scrapy in the direction of those proxies through your projects settings file.
  - It’ll rotate through them.

- One of the things that surprised me most about scraping some .gov sites is that my IP was never banned, not once.
  - If that’s your goal using proxies is overkill.
  - This does make your spiders more robust though and depending on your use case a valuable asset for your spiders to have.

- You can customize your spiders in a variety of other ways.
  - Another useful customization is to up the number of retries that your spiders make on each site, and remove any throttling.
  - The settings default to a reasonable level for auto-throttling the number of requests though.
  - It’s really only applicable for large projects, and upping the level of throttling can be helpful for limiting how frequently your IP address gets banned or for eliminating internet bandwidth as a limiting factor.

- Scrapy’s settings will also default to ignoring robots.txt, a doc all websites have that I suspect is only ever read by google’s or other search engines vast hoards of spiders.
  - If the webpages that you’re scraping don’t want to be indexed then it won’t make a difference to your spiders.
  - Your spider can crawl on anything.

- The settings also default to letting it dump logs and processed data in your terminal.. but you can easily change that.
  - I recommend having it process them into .log files and setup Scrapy to send them to a unique folder.
  - This makes it easier to track progress over time and identify errors.

- Collecting data for machine learning projects is one of the most helpful applications for web scraping.
  - Many strides have been made in NLP transformers that drastically reduce the need for huge training sets, but for other applications such as image and music generation with ML do require a large amount of training data.
  - In fact a lot of the specifics of your model may not matter much when compared to the need for quality training .jpegs or .midi files.
  - This is how developing fast custom spiders can up the quality of your machine learning projects, enabling the collection of large data sets.
  - It’s important to note that bias can be inserted into these data as a result of your web scraping protocol.
  - Generalizability can be effected as a direct result of unfair sampling by your spiders.

- Scraping public records from .gov sites is another valuable use case.
  - Data brokerages often use web-scraping techniques to gather data, which they usually sell to marketing teams within corporations at a high profit margin.
  - Often the scraping implementation and data verification process does not need to be all that sophisticated to payoff for them either.
  - And more power to them for capitalizing on that.
