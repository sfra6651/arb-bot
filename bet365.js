// index.js
const fs = require("fs");
const puppeteer = require("puppeteer");

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

  await page.goto("https://www.bet365.com/#/HO/", {
    waitUntil: "networkidle0",
    headless: true,
  });

  console.log("hakljakghja");

  await page.setViewport({ height: 1080, width: 780 });

  // await page.screenshot({ path: `bet365.png` });
  await new Promise((resolve) => setTimeout(resolve, 10000));
  await page.screenshot({ path: `bet365.png` });

  // await page.waitForSelector(".sm-SplashMarketGroup.sm-SplashMarketGroup_Cn2 ");

  console.log("hakljakghja");

  const tabsToOpen = await page.$$(
    ".sm-SplashMarketGroup.sm-SplashMarketGroup_Cn2 "
  );

  var count = tabsToOpen.length;

  console.log(tabsToOpen.length);

  for (i = 0; 1 < count; i++) {
    const targetElement = await element.evaluate(() => {
      const target = tabsToOpen[i].find(
        (el) => el.textContent.trim() === "Game Betting 3-Way"
      );
      return targetElement ? targetElement.textContent : null;
    });
    await targetElement.click();

    await page.waitForSelector(".gl-MarketGroupContainer");

    page.screenshot("bet365");
  }

  // console.log(tabsToOpen.length);

  // const jsonString = JSON.stringify(rugbyOdds, null, 2);
  // fs.writeFile("TAB.json", jsonString, (err) => {
  //   if (err) {
  //     console.error("An error occurred:", err);
  //     return;
  //   }
  //   console.log("JSON file has been saved with the array of objects.");
  // });

  await browser.close();
})();
