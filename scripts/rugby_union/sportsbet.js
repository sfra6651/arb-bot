const fs = require("fs");
const puppeteer = require("puppeteer");

async function rodds(card) {
  //   console.log(card);
  const t = await card.$eval(
    ".size12_fq5j3k2.normal_fgzdi7m.caption_f4zed5e",
    (el) => el.textContent
  );
  const o = await card.$eval(
    ".size14_f7opyze.bold_f1au7gae.priceTextSize_frw9zm9",
    (el) => el.textContent
  );
  return {
    team: t,
    odds: o,
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
  await page.goto("https://www.sportsbet.com.au/betting/rugby-union", {
    // waitUntil: "networkidle0",
  });

  const tabs = await page.$$(".tabTouchable_f14y21fs");
  await tabs[1].click();

  await page.waitForSelector(".priceButtonContentMultiLine_f1nrpck2");
  const cards = await page.$$(".priceButtonContentMultiLine_f1nrpck2");

  var odds = [];
  //   console.log(cards);
  for (const card of cards) {
    const json = await rodds(card);
    odds.push(json);
  }

  var finalOdds = [];
  for (var i = 0; i < odds.length; i += 3) {
    finalOdds.push({
      id: `${odds[i].team}.${odds[i + 2].team}`,
      odds: [odds[i].odds, odds[i + 1].odds, odds[i + 2].odds],
    });
  }

  //   await new Promise((resolve) => setTimeout(resolve, 2000));
  //   await page.screenshot({ path: `sprotsbet.png` });

  const jsonString = JSON.stringify(finalOdds, null, 2);
  fs.writeFile("data/rugby_union/sportsbet.json", jsonString, (err) => {
    if (err) {
      console.error("An error occurred:", err);
      return;
    }
    console.log("JSON file has been saved with the array of objects.");
  });

  await browser.close();
})();
