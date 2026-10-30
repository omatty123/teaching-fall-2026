'use strict';
(() => {
  const buttons = [...document.querySelectorAll('[data-view]')];
  const prefix = 'equiano-3-4-assets/';
  const fallback = document.getElementById('map-fallback');
  buttons.forEach(button => { button.disabled = true; });
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  async function json(url) {
    const result = await fetch(url);
    if (!result.ok) throw new Error('Map data could not load');
    return result.json();
  }
  async function start() {
    if (typeof L === 'undefined') return;
    const [views, countries, detail, thames] = await Promise.all([
      json(prefix + 'map-config.json'),
      json(`${prefix}map-data/atlantic-50m.geojson`),
      json(prefix + 'map-data/europe-islands-10m.geojson'),
      json(prefix + 'map-data/thames-natural-earth.geojson')
    ]);
    const map = L.map('journey-map', {scrollWheelZoom:false, dragging:!L.Browser.mobile, minZoom:2, maxZoom:12, zoomSnap:0.1});
    map.attributionControl.setPrefix(false);
    map.attributionControl.addAttribution('Geography: <a href="https://www.naturalearthdata.com/">Natural Earth</a> · modern outlines');
    L.control.scale({imperial:false,maxWidth:120}).addTo(map);
    const layer = L.layerGroup().addTo(map);
    const landStyle = {color:'#899b9d',weight:0.8,fillColor:'#e3e8dd',fillOpacity:1};
    let selected = 'atlantic';
    function label(point, text, extra = '', direction = 'center') {
      L.circleMarker(point, {radius:0,opacity:0,fillOpacity:0,interactive:false})
        .bindTooltip(escape(text),{permanent:true,direction,className:'place-label region-label '+extra,offset:[0,0]}).addTo(layer);
    }
    function fit() {
      map.invalidateSize();
      map.fitBounds(views[selected].bounds,{padding:[26,24],animate:false});
    }
    function show(view) {
      if (!views[view]) return;
      selected = view;
      layer.clearLayers();
      const settings = views[view];
      if (view === 'atlantic') {
        L.geoJSON(countries,{style:landStyle,interactive:false,filter:f=>f.properties.ADM0_A3!=='BRB'}).addTo(layer);
        L.geoJSON(detail,{style:landStyle,interactive:false,filter:f=>f.properties.ADM0_A3==='BRB'}).addTo(layer);
      } else {
        L.geoJSON(detail,{style:landStyle,interactive:false}).addTo(layer);
      }
      if (view === 'thames') {
        L.geoJSON(thames,{style:{color:'#4384a3',weight:4,opacity:0.95},interactive:false}).addTo(layer);
      }
      settings.labels.forEach(item => label([item.lat,item.lon],item.text,'map-context-label'));
      settings.points.forEach(point => {
        if (point.kind === 'region') {
          label([point.lat,point.lon],point.label,'map-region-label',point.direction);
          return;
        }
        const icon = L.divIcon({className:'equiano-map-pin',html:'<span></span>',iconSize:[14,14],iconAnchor:[7,7]});
        L.marker([point.lat,point.lon],{icon,title:point.name,alt:point.name,keyboard:true})
          .bindTooltip(escape(point.label),{permanent:true,direction:point.direction,className:'place-label',offset:[0,0]})
          .bindPopup('<strong>'+escape(point.name)+'</strong><p>'+escape(point.note)+'</p>').addTo(layer);
      });
      buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.view===view)));
      document.getElementById('map-view-title').textContent = settings.title;
      document.getElementById('map-view-copy').innerHTML = settings.copy;
      document.getElementById('static-map-link').href = prefix + settings.image;
      document.getElementById('journey-map').setAttribute('aria-label',settings.title+'. Selected place locators; use the place list below for geographic limits.');
      map.closePopup();
      fit();
    }
    document.documentElement.classList.add('map-ready');
    if (fallback) fallback.setAttribute('aria-hidden','true');
    buttons.forEach(button => {button.disabled=false;button.addEventListener('click',()=>show(button.dataset.view));});
    show(selected);
    let timer;
    window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(fit,120);});
  }
  start().catch(() => {
    document.documentElement.classList.remove('map-ready');
    if (fallback) fallback.removeAttribute('aria-hidden');
    buttons.forEach(button => {button.disabled=true;});
    document.getElementById('map-view-copy').insertAdjacentHTML('beforeend','<p>The interactive map is unavailable. The static maps and place list below remain available.</p>');
  });
})();
