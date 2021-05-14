// Put all the javascript code here, that you want to execute in background.
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.getflag == "true")
      sendResponse({flag: "OOO{}"});
  }
);