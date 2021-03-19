// Credits: https://flaskpwa.com/#_initialSetupJS
'use strict';

let deferredInstallPrompt = null;
const installButton = document.getElementById('butInstall');
if (installButton !== null) {
  installButton.addEventListener('click', installPWA);
}

window.addEventListener('beforeinstallprompt', saveBeforeInstallPromptEvent);

function saveBeforeInstallPromptEvent(evt) {
  deferredInstallPrompt = evt;
  if (installButton !== null) {
    installButton.removeAttribute('hidden');
  }

function installPWA(evt) {
  deferredInstallPrompt.prompt();
  if (installButton !== null) {
    installButton.setAttribute('hidden', true);
  }
  deferredInstallPrompt.userChoice
  .then((choice) => {
    if (choice.outcome === 'accepted') {
      console.log('User accepted the add to homescreen prompt', choice);
    } else {
      console.log('User dismissed the add to homescreen prompt', choice);
    }
    deferredInstallPrompt = null;
  });
}

window.addEventListener('appinstalled', logAppInstalled);

function logAppInstalled(evt) {
  console.log('App was installed.', evt);
}
