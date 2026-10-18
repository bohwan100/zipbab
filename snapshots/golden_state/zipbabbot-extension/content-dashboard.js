// ZipbabBot Chrome Extension - Dashboard Bridge
(function() {
  // 1. Mark DOM attribute for immediate detection
  try {
    document.documentElement.setAttribute('data-zipbabbot-extension', 'true');
    window.postMessage({ type: 'ZIPBABBOT_EXTENSION_READY' }, '*');
  } catch(e) {}

  // 2. Listen for batch add request from webpage
  window.addEventListener('message', function(event) {
    if (event.source !== window || !event.data) return;
    
    if (event.data.type === 'ZIPBABBOT_START_BATCH') {
      const items = event.data.items || [];
      chrome.runtime.sendMessage({
        action: 'START_BATCH_ADD',
        items: items
      });
    } else if (event.data.type === 'ZIPBABBOT_STOP_BATCH') {
      chrome.runtime.sendMessage({
        action: 'STOP_BATCH_ADD'
      });
    }
  });

  // 3. Relay messages from extension background to webpage
  chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg && msg.type && msg.type.startsWith('ZIPBABBOT_')) {
      window.postMessage(msg, '*');
    }
  });
})();
