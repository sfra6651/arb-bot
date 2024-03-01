// index.js
const fs = require("fs");
const puppeteer = require("puppeteer");

async function rugby_odds(element) {
  const home = await element.$(".event-card__body__name__home");

  const away = await element.$(".event-card__body__name__away");

  const h = await home.evaluate((el) => el.textContent);
  const a = await away.evaluate((el) => el.textContent);

  // console.log(h, a);

  const id = `${h}.${a}`;
  const oddsElements = await element.$$(".button--outcome__price");
  const odds0 = await oddsElements[0].evaluate((el) => el.textContent);
  const odds1 = await oddsElements[1].evaluate((el) => el.textContent);
  const odds2 = await oddsElements[2].evaluate((el) => el.textContent);
  const odds = [odds0, odds1, odds2];

  return {
    id: id,
    // home,
    // away,
    odds: odds,
  };
}

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
  });
  const page = await browser.newPage();

  headers = {
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
  };

  await page.setExtraHTTPHeaders(headers);

  await page.goto("https://www.tab.co.nz/sport/27/rugby-union/matches", {
    waitUntil: "networkidle0",
  });

  await page.waitForSelector(".heading.heading--competition");

  const data = await page.$$(".event-list__item.event-list__item--rugby");

  var rugbyOdds = [];

  for (const element of data) {
    try {
      const json = await rugby_odds(element);
      rugbyOdds.push(json);
    } catch (err) {
      continue;
    }
  }

  const jsonString = JSON.stringify(rugbyOdds, null, 2);
  fs.writeFile("data/rugby_union/TAB.json", jsonString, (err) => {
    if (err) {
      console.error("An error occurred:", err);
      return;
    }
    console.log("JSON file has been saved with the array of objects.");
  });

  await browser.close();
})();
