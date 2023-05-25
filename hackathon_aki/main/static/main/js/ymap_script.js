ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 10,
        controls: ['smallMapDefaultSet']
    });

    myMap.controls.remove('searchControl');
    myMap.controls.remove('typeSelector');
    myMap.controls.remove('fullscreenControl');

    myMap.geoObjects.add(new ymaps.Placemark([55.684758, 37.738521], {}, {
        preset: 'islands#blueDotIcon'
    }));
}
