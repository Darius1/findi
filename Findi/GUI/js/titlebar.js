(function () {
      
    const remote = require('electron').remote; 
    const {webFrame}  = require('electron');
    const {webContents}  = require('electron');
    
    function init() { 
      document.getElementById("min-btn").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.minimize(); 
      });
      
      document.getElementById("max-btn").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        if (!window.isMaximized()) {
          window.maximize();
        } else {
          window.unmaximize();
        }	 
      });
      
      document.getElementById("menu-min").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.unmaximize();
      });
      
      document.getElementById("close-btn").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.close();
      }); 

      document.getElementById("menu-exit").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.close();
      });

      document.getElementById("menu-close").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.close();
      });

      document.getElementById("menu-reload").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.reload();
      });

      document.getElementById("menu-zi").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        let currentZoomFactor = webFrame.getZoomFactor();
        webFrame.setLayoutZoomLevelLimits(0, 2)
        webFrame.setZoomFactor(currentZoomFactor + .1);
      });

      document.getElementById("menu-zo").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        webFrame.setLayoutZoomLevelLimits(-1, 0)
        let currentZoomFactor = webFrame.getZoomFactor();
        webFrame.setZoomFactor(currentZoomFactor - .1);
      });

      document.getElementById("menu-tas").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        webFrame.setZoomFactor(1);
      });

      document.getElementById("menu-fs").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        if (!window.isFullScreen()) {
          window.setFullScreen(true);
        } else {
          window.setFullScreen(false);
        }
        
      });

      document.getElementById("menu-undo").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.undo();
      });

      document.getElementById("menu-redo").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.redo();

      });

      document.getElementById("menu-cut").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.cut();
      });

      document.getElementById("menu-copy").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.copy();
      });

      document.getElementById("menu-paste").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.paste();
      });

      document.getElementById("menu-delete").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.delete();
      });

      document.getElementById("menu-sa").addEventListener("click", function (e) {
        const window = remote.getCurrentWindow();
        window.webContents.selectAll();
      });
    }; 
    
    document.onreadystatechange = function () {
      if (document.readyState == "complete") {
        init(); 
      }
    };
})();
