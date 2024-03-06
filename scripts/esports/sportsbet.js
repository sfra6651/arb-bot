const fs = require("fs");
const puppeteer = require("puppeteer");
require("dotenv").config();

async function rodds(row) {
  try {
    const odds = [];
    const odd_handles = await row.$$('[data-automation-id="price-text"]');
    for (odd of odd_handles) {
      const first = await odd.evaluate((el) => el.textContent);
      odds.push(first);
    }
    const teams = await row.$$(
      ".size12_fq5j3k2.normal_fgzdi7m.caption_f4zed5e"
    );
    const team1 = await teams[0].evaluate((el) => el.textContent);
    const team2 = await teams[1].evaluate((el) => el.textContent);
    return {
      id: `${team1}.${team2}`,
      odds: odds,
    };
  } catch (err) {
    console.log(err);
    return {};
  }
}

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [process.env.PROXY_ARG],
  });

  const page = await browser.newPage();
  headers = {
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
  };

  await page.authenticate({
    username: process.env.PROXY_USER,
    password: process.env.PROXY_PASS,
  });
  await page.setExtraHTTPHeaders(headers);
  await page.goto("https://www.sportsbet.com.au/betting/e-sports", {
    // waitUntil: "networkidle0",
  });

  const tabs = await page.$$(".tabTouchable_f14y21fs");
  await tabs[1].click();

  await page.waitForSelector(".card_fohmrj3");
  const cards = await page.$$(".card_fohmrj3");
  var count = 0;
  var odds = [];

  for (const card of cards) {
    const json = await rodds(card);
    if (json.odds.length < 3) {
      json.odds.splice(1, 0, 0.0);
    }
    odds.push(json);
    count += 1;
    console.log((count / cards.length) * 100);
  }

  const jsonString = JSON.stringify(odds, null, 2);
  fs.writeFile("data/esports/sportsbet.json", jsonString, (err) => {
    if (err) {
      console.error("An error occurred:", err);
      return;
    }
    console.log("JSON file saved");
  });

  //   const html = await cards[0].evaluate((el) => el.outerHTML);
  //   console.log(html);

  await browser.close();
})();
