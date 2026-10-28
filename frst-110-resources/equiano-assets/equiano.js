'use strict';
(() => {
  const buttons = [...document.querySelectorAll('[data-view]')];
  buttons.forEach(button => { button.disabled = true; });
  const views = {
    atlantic: {
      bounds: [[-5, -82], [35, 17]],
      title: 'Africa to Barbados',
      copy: '<p>Chapter 1 describes a homeland in Eboe, associated with Igbo-speaking country in present-day southeastern Nigeria. Chapter 2 narrates captivity within Africa, an unnamed embarkation port, and an Atlantic crossing to Barbados.</p><p>The journey stops here for this reading. Virginia and England enter in chapter 3.</p>',
      image: 'equiano-map-atlantic.png'
    },
    africa: {
      bounds: [[2.6, 1.4], [10.5, 11.8]],
      title: 'The African geography is uncertain',
      copy: '<p><strong>Eboe</strong> is the narrative’s designation associated with Igbo people and country. The dashed oval gives broad regional orientation; it is not a historical boundary.</p><p><strong>Essaka and Tinmah are not pinned.</strong> Modern identifications depend on disputed scholarship. The large river and departure port are unnamed.</p><p>Benin City, the Niger, and the Benue provide context. The city is not a journey stop; neither named river is identified here as the river in chapter 2.</p>',
      image: 'equiano-map-nigeria.png'
    },
    barbados: {
      bounds: [[12.98, -59.82], [13.37, -59.37]],
      title: 'Barbados and Bridgetown',
      copy: '<p>The narrative names <strong>Barbadoes</strong> and <strong>Bridge Town</strong>: Barbados and Bridgetown. The marker gives the town’s approximate location, not a specific anchorage or sale yard.</p><p>Chapter 2 ends with a sale that separates families. The opening of chapter 3 explains that Equiano himself was among those <strong>not sold in Barbados</strong> and was sent to Virginia.</p>',
      image: 'equiano-map-barbados.png'
    }
  };

  async function start() {
    if (typeof L === 'undefined') return;
    const files = ['countries-50m.geojson', 'niger-benue-50m.geojson', 'barbados-10m.geojson'];
    const [countries, rivers, barbados] = await Promise.all(files.map(async file => {
      const response = await fetch('equiano-assets/map-data/' + file);
      if (!response.ok) throw new Error('Map data unavailable');
      return response.json();
    }));
    document.documentElement.classList.add('map-ready');
    const map = L.map('journey-map', {scrollWheelZoom: false, dragging: !L.Browser.mobile, minZoom: 2, maxZoom: 13, zoomSnap: 0.1, attributionControl: true});
    map.attributionControl.setPrefix(false);
    map.attributionControl.addAttribution('Geography: <a href="https://www.naturalearthdata.com/">Natural Earth</a> · modern borders');
    L.control.scale({imperial: false, maxWidth: 130}).addTo(map);
    const landStyle = {color: '#8b9d9f', weight: 0.8, fillColor: '#e3e8dd', fillOpacity: 1};
    L.geoJSON(countries, {style: landStyle, filter: f => f.properties.ADM0_A3 !== 'BRB', interactive: false}).addTo(map);
    L.geoJSON(barbados, {style: {...landStyle, color: '#6a8082', weight: 1.4}, interactive: false}).addTo(map);
    const layers = {atlantic: L.layerGroup(), africa: L.layerGroup(), barbados: L.layerGroup()};
    const rust = '#a44127', blue = '#245a8d';
    function label(group, point, text, extra = '') {
      L.circleMarker(point, {radius: 0, opacity: 0, fillOpacity: 0, interactive: false})
        .bindTooltip(text, {permanent: true, direction: 'center', className: 'place-label ' + extra}).addTo(group);
    }
    function pin(group, point, name, description, color, direction = 'right') {
      L.circleMarker(point, {radius: 6, color: '#fff', weight: 2, fillColor: color, fillOpacity: 1})
        .bindTooltip(name, {permanent: true, direction, className: 'place-label', offset: [4,0]})
        .bindPopup('<strong>' + name + '</strong><br>' + description).addTo(group);
    }
    label(layers.atlantic, [25, -41], 'ATLANTIC OCEAN');
    label(layers.atlantic, [22, 9], 'AFRICA');
    label(layers.atlantic, [-1, -64], 'SOUTH AMERICA');
    label(layers.atlantic, [31, -70], 'NORTH AMERICA');
    pin(layers.atlantic, [13.1,-59.6167], 'Barbados', 'Named arrival in chapter 2. Choose the Barbados view for the island and Bridgetown.', rust, 'left');
    L.rectangle([[2.6,1.4],[10.5,11.8]], {color:blue, weight:1.3, fill:false, dashArray:'5 5', interactive:false}).addTo(layers.atlantic);
    L.polyline([[2,0],[2,-12],[5,-29],[9,-45],[12.8,-57]], {color:rust,weight:2.5,dashArray:'8 7',interactive:false}).addTo(layers.atlantic);
    // The arrowhead indicates direction only. Its endpoint is offshore, not a port.
    L.polyline([[13.4,-55.9],[12.8,-57],[12.1,-56.1]], {color:rust,weight:2.5,interactive:false}).addTo(layers.atlantic);
    label(layers.atlantic, [-1,-29], 'Narrated crossing · schematic', 'region-label crossing-label');
    L.geoJSON(rivers, {style:{color:'#4384a3',weight:2.1},interactive:false}).addTo(layers.africa);
    const oval = Array.from({length:61}, (_,i) => {const a=i*Math.PI/30;return [5.95+1.15*Math.sin(a),7.3+0.9*Math.cos(a)];});
    L.polygon(oval,{color:blue,weight:1.3,dashArray:'5 5',fillOpacity:0.07,fillColor:blue,interactive:false}).addTo(layers.africa);
    label(layers.africa,[9.5,8.8],'NIGERIA');
    label(layers.africa,[8.3,2.2],'BENIN','region-label');
    label(layers.africa,[3.3,5.4],'GULF OF GUINEA');
    label(layers.africa,[5.9,7.4],'Igbo-speaking region','region-label');
    label(layers.africa,[8.1,5.9],'Niger','region-label');
    label(layers.africa,[8.3,9.1],'Benue','region-label');
    pin(layers.africa,[6.3167,5.6833],'Benin City','Context for the historical kingdom, not a narrated journey stop.',blue,'left');
    pin(layers.barbados,[13.1,-59.6167],'Bridgetown','Approximate town-centre locator. The historical anchorage and sale yard are not identified.',rust,'left');
    label(layers.barbados,[13.22,-59.55],'BARBADOS');
    label(layers.barbados,[13.30,-59.73],'ATLANTIC OCEAN','region-label');
    let selected = 'atlantic';
    function show(view) {
      selected = view;
      Object.values(layers).forEach(layer => map.removeLayer(layer));
      layers[view].addTo(map);
      map.fitBounds(views[view].bounds,{padding:[18,18],animate:false});
      buttons.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.view === view)));
      document.getElementById('map-view-title').textContent = views[view].title;
      document.getElementById('map-view-copy').innerHTML = views[view].copy;
      document.getElementById('static-map-link').href = 'equiano-assets/' + views[view].image;
      map.closePopup();
    }
    buttons.forEach(button => {button.disabled=false;button.addEventListener('click',()=>show(button.dataset.view));});
    show('atlantic');
    let resizeTimer;
    window.addEventListener('resize', () => {clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{map.invalidateSize();map.fitBounds(views[selected].bounds,{padding:[18,18],animate:false});},150);});
  }
  start().catch(() => {
    document.documentElement.classList.remove('map-ready');
    buttons.forEach(button => {button.disabled=true;});
    document.getElementById('map-view-copy').insertAdjacentHTML('beforeend','<p>The interactive map could not load. Use the map image or PDF links.</p>');
  });
})();
