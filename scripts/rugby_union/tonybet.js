const { all } = require("axios");
const fs = require("fs");
const puppeteer = require("puppeteer");

async function rodds(row) {
  //   console.log(card);
  try {
    const odds = [];
    const odd_handles = await row.$$('[data-test="outcome"]');
    for (odd of odd_handles) {
      const first = await odd.evaluate((el) => el.textContent);
      //   console.log(first);
      odds.push(first);
    }

    const teams = await row.$$(".event-table__team-name");
    const team1 = await teams[0].evaluate((el) => el.textContent);
    const team2 = await teams[1].evaluate((el) => el.textContent);
    return {
      id: `${team1}.${team2}`,
      odds: odds,
    };
  } catch {
    return {};
  }
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
  await page.goto("https://tonybet.com/nz/prematch", {
    // waitUntil: "networkidle0",
  });

  await page.waitForSelector(".event-table__row");

  await new Promise((resolve) => setTimeout(resolve, 2000));

  const events = await page.$$(".event-table");

  console.log(events.length);

  var data = [];

  for (const event of events) {
    const rows = await event.$$(".event-table__row");
    // await page.waitForSelector('[data-test="outcome"]');
    for (row of rows) {
      try {
        await row.scrollIntoView();
        await new Promise((resolve) => setTimeout(resolve, 300));
        const row_data = await rodds(row);
        // console.log(row_data);
        if (row_data) {
          data.push(row_data);
        }
      } catch (err) {}
    }
  }

  //   await new Promise((resolve) => setTimeout(resolve, 2000));
  //   await page.screenshot({ path: `sprotsbet.png` });

  const jsonString = JSON.stringify(data, null, 2);
  fs.writeFile("data/rugby_union/tonybet.json", jsonString, (err) => {
    if (err) {
      console.error("An error occurred:", err);
      return;
    }
    console.log("JSON file has been saved with the array of objects.");
  });

  await browser.close();
})();
