"use strict"

document.addEventListener("DOMContentLoaded", document_init);

function document_init() {
    let map_container = document.getElementById("map");

    let parent_width = parseInt(map_container.parentNode.offsetWidth);
    map_container.setAttribute('style', `width: ${parent_width}px; height: ${parent_width}px`);
}

ymaps.ready(map_init);

function map_init() {
    let map_container = document.getElementById("map");
    let address_latitude = Number(map_container.getAttribute('address_latitude'));
    let address_longitude = Number(map_container.getAttribute('address_longitude'));
    let platform_name = map_container.getAttribute('platform_name');

    let map = new ymaps.Map('map', {
        center: [address_latitude, address_longitude],
        zoom: 13,
        controls: ['zoomControl', 'geolocationControl', 'fullscreenControl']
    });

    let placemark = new ymaps.Placemark([address_latitude, address_longitude], {
        iconCaption: platform_name,
    }, {
        preset: 'islands#blueDotIconWithCaption'
    });
    map.geoObjects.add(placemark);
}
