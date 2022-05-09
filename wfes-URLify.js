// @name URLify
// @version 1.2.0
// @description detect links in supporting information
// @author AlterTobi

(function() {
  "use strict";

  const myCssId = "urlifyCSS";
  const myStyle = `.externalLinkButton{
        border: 2pt solid white;
        border-radius: 2pt;
        width: 17pt;
        font-size: 14px;
        background-color: white;
        color: black;
        display: block;
        float: left;
        margin-right: 3pt;
        height: 17pt;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        margin-bottom: 5pt;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill-rule='evenodd' d='M10.604 1h4.146a.25.25 0 01.25.25v4.146a.25.25 0 01-.427.177L13.03 4.03 9.28 7.78a.75.75 0 01-1.06-1.06l3.75-3.75-1.543-1.543A.25.25 0 0110.604 1zM3.75 2A1.75 1.75 0 002 3.75v8.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0014 12.25v-3.5a.75.75 0 00-1.5 0v3.5a.25.25 0 01-.25.25h-8.5a.25.25 0 01-.25-.25v-8.5a.25.25 0 01.25-.25h3.5a.75.75 0 000-1.5h-3.5z'/%3E%3C/svg%3E");
        box-shadow: 0 0 2px grey;
      }
  `;

  const myReg = /((https?:\/\/)[-\w@:%_+.~#?,&/=]+)/g;
  let maxtries = 10;

  // Button setzen
  function setSmallButton(url, elem) {
    const externalLinkButton = document.createElement("a");
    externalLinkButton.setAttribute("target", "_blank");
    externalLinkButton.setAttribute("class", "externalLinkButton");
    externalLinkButton.href = url;
    elem.appendChild(externalLinkButton);
  }

  function detectURL() {
    const candidate = window.wfes.g.reviewPageData();
    window.wfes.f.addCSS(myCssId, myStyle);

    if (undefined !== candidate.statement) {
      const urls = candidate.statement.match(myReg);
      const elem = document.querySelector("app-supporting-info > wf-review-card > div.wf-review-card__body > div > div.mt-2.bg-gray-200.px-4.py-2.ng-star-inserted");

      urls.forEach(function(url) {
        setSmallButton(url, elem);
      });
    }
  }

  window.addEventListener("WFESReviewPageNewLoaded", detectURL);

  console.log("Script loaded:", GM_info.script.name, "v" + GM_info.script.version);
})();