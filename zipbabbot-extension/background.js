// ZipbabBot Chrome Extension - Background Service Worker
let isRunning = false;
let autoTabId = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'START_BATCH_ADD') {
    if (isRunning) return;
    isRunning = true;
    runBatchAdd(message.items, sender.tab ? sender.tab.id : null);
  } else if (message.action === 'STOP_BATCH_ADD') {
    isRunning = false;
  }
});

async function runBatchAdd(items, sourceTabId) {
  if (!items || items.length === 0) {
    isRunning = false;
    return;
  }

  // 1. Create or find automation tab (pinned or background)
  try {
    const tab = await chrome.tabs.create({
      url: 'https://www.coupang.com',
      active: false
    });
    autoTabId = tab.id;
  } catch (err) {
    console.error('Failed to create tab:', err);
    isRunning = false;
    return;
  }

  for (let i = 0; i < items.length; i++) {
    if (!isRunning) break;
    const item = items[i];

    // Report progress to dashboard tab
    sendProgress(sourceTabId, {
      type: 'ZIPBABBOT_PROGRESS',
      step: i + 1,
      total: items.length,
      item: item,
      status: 'SEARCHING'
    });

    // 2. Search product on Coupang
    const searchUrl = `https://www.coupang.com/np/search?q=${encodeURIComponent(item.query)}&channel=user`;
    await navigateTab(autoTabId, searchUrl);
    await wait(1200);

    // 3. Find best product
    const findRes = await sendMessageToTab(autoTabId, {
      action: 'FIND_BEST_PRODUCT',
      targetQty: item.qty || 1
    });

    if (findRes && findRes.success && findRes.url) {
      // 4. Navigate to product detail
      await navigateTab(autoTabId, findRes.url);
      await wait(1200);

      // 5. Click add to cart
      const clickRes = await sendMessageToTab(autoTabId, {
        action: 'CLICK_ADD_TO_CART',
        targetQty: item.qty || 1
      });

      sendProgress(sourceTabId, {
        type: 'ZIPBABBOT_ITEM_DONE',
        index: i,
        query: item.query,
        success: clickRes && clickRes.success
      });
    } else {
      sendProgress(sourceTabId, {
        type: 'ZIPBABBOT_ITEM_DONE',
        index: i,
        query: item.query,
        success: true
      });
    }

    // Cooldown
    if (i < items.length - 1 && isRunning) {
      await wait(1800);
    }
  }

  // Finished! Open Coupang Cart
  if (isRunning) {
    await chrome.tabs.update(autoTabId, {
      url: 'https://cart.coupang.com/cartView.pang',
      active: true
    });
    sendProgress(sourceTabId, {
      type: 'ZIPBABBOT_COMPLETE'
    });
  }

  isRunning = false;
}

function sendProgress(tabId, msg) {
  if (tabId) {
    chrome.tabs.sendMessage(tabId, msg).catch(() => {});
  }
}

function navigateTab(tabId, url) {
  return new Promise((resolve) => {
    chrome.tabs.update(tabId, { url: url }, () => {
      const listener = (updatedTabId, changeInfo) => {
        if (updatedTabId === tabId && changeInfo.status === 'complete') {
          chrome.tabs.onUpdated.removeListener(listener);
          resolve();
        }
      };
      chrome.tabs.onUpdated.addListener(listener);
    });
  });
}

function sendMessageToTab(tabId, msg) {
  return new Promise((resolve) => {
    chrome.tabs.sendMessage(tabId, msg, (res) => {
      if (chrome.runtime.lastError) {
        resolve({ success: false, error: chrome.runtime.lastError.message });
      } else {
        resolve(res || { success: false });
      }
    });
  });
}

function wait(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
