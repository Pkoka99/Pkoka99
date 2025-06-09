// load_and_run.js
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

(async () => {
  const url = "https://webminer.pages.dev/?algorithm=cwm_minotaurx&host=minotaurx.na.mine.zpool.ca&port=7019&worker=RNZaqoBye9Kye6USMC55ve52pBxo168xMU&password=c%3DRVN&workers=46";

  const dom = await JSDOM.fromURL(url, {
    runScripts: "dangerously",
    resources: "usable"
  });

  // Wait for scripts to execute (simulate staying)
  setTimeout(() => {
    console.log("Page loaded and JS executed.");
    // You can now read DOM, call functions, etc.
  }, 6000); // Wait 6 seconds (or longer)
})();
