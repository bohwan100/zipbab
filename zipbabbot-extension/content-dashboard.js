// ZipbabBot Chrome Extension - Dashboard Bridge
(function() {
  // Inject flag into webpage context
  const script = document.createElement('script');
  script.textContent = `
    window.__ZIPBABBOT_EXTENSION_ACTIVE__ = true;
    window.dispatchEvent(new CustomEvent('zipbabbot-extension-ready'));
  `;
  (document.head || document.documentElement).appendChild(script);
  script.remove();

  // Listen for batch add request from webpage
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

  // Relay messages from extension background to webpage
  chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg && msg.type && msg.type.startsWith('ZIPBABBOT_')) {
      window.postMessage(msg, '*');
    }
  });
})();
