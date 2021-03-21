// Credits: https://github.com/umluizlima/flask-pwa/blob/master/app/static/js/app.js

(function() {
  if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
          navigator.serviceWorker.register('/service-worker.js')
              .then(function(registration) {
                  console.log('Service Worker Registered');
                  return registration;
              })
              .catch(function(err) {
                  console.error('Unable to register service worker.', err);
              });
          navigator.serviceWorker.ready.then(function(registration) {
              console.log('Service Worker Ready');
          });
      });
  }
})();
