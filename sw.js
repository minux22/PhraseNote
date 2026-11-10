const CACHE='phrasenote-v0.29.0';
const FILES=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
// Cache first, so the app opens at once even on a weak signal; the network copy is fetched in the background
// and saved for next time (a new version therefore shows on the next launch).
self.addEventListener('fetch',e=>{
  const req=e.request;
  const u=new URL(req.url);
  // the built-in SoundFont is kept by the app itself (IndexedDB), not in this cache
  if(req.method!=='GET'||u.origin!==self.location.origin||u.pathname.endsWith('.sf2'))return;
  e.respondWith(caches.open(CACHE).then(c=>c.match(req,{ignoreSearch:true}).then(hit=>{
    const net=fetch(req).then(r=>{if(r&&r.ok)c.put(req,r.clone());return r;}).catch(()=>null);
    if(hit){e.waitUntil(net);return hit;}
    return net.then(r=>r||c.match('./index.html'));
  })));
});
