"use strict"

let suggest_view;

$(document).ready(function() {
    $("#address_suggest_form").keydown(function(event) {
        if (suggest_view.options.get('provider', 'yandex#map') == 'none') {
            suggest_view.options.set('provider', 'yandex#map');
        }

        if (event.keyCode == 13) {
            $("#adders_check_button").click();
        }
    });

    document.getElementById("platform_creating_form_submit_button").onclick = function() {
        document.getElementById("platform_creating_form").submit();
    };
});

ymaps.ready(init);

function init() {
    suggest_view = new ymaps.SuggestView('address_suggest_form');

    let map;
    let placemark;

    set_default_map();

    $('#adders_check_button').bind('click', function (e) {
        let request = $('#address_suggest_form').val();

        ymaps.geocode(request).then(update_map_from_geocode, function (e) {
            console.log(e)
        });
    });

    map.events.add('click', function (e) {
        update_map_from_placemark_event(e.get('coords'));
    });

    function set_default_map() {
        if (!map) {
            map = new ymaps.Map('map', {
                center: [55.76, 37.64],
                zoom: 10,
                controls: ['zoomControl']
            });

            placemark = new ymaps.Placemark(map.center, {}, {
                draggable: true
            });
            placemark.events.add('dragend', function () {
                update_map_from_placemark_event(placemark.geometry.getCoordinates());
            });
        } else {
            map.remove(placemark);
            map.setCenter([55.76, 37.64]);
            map.setZoom(10);
        }
    }

    function update_map_from_placemark_event(coords) {
        placemark.geometry.setCoordinates(coords);
        placemark.properties.set('iconCaption', 'поиск...');
        placemark.properties.set('balloonContent', 'поиск...');
        placemark.options.set('preset', 'islands#violetDotIconWithCaption');

        map.panTo(coords);

        document.getElementById("address_suggest_form").value = '';

        ymaps.geocode(coords).then(update_map_from_geocode, function (e) {
            console.log(e)
        });
    }

    function update_map_from_geocode(res) {
        let obj = res.geoObjects.get(0);
        let error;

        if (obj) {
            switch (obj.properties.get('metaDataProperty.GeocoderMetaData.precision')) {
                case 'exact':
                    break;
                case 'number':
                    error = 'Не найден адрес с таким номером строения/корпуса, показан похожий адрес.';
                    break;
                case 'near':
                    error = 'Не найден адрес с таким номером дома, показан похожий адрес.';
                    break;
                case 'range':
                    error = 'Неточный адрес, уточните номер дома.';
                    break;
                case 'street':
                    error = 'Неточный адрес, уточните номер дома.';
                    break;
                case 'other':
                    error = 'Неточный адрес, уточните улицу и номер дома.';
                    break;
                default:
                    error = 'Уточните адрес.';
            }
        } else {
            $('#adders_check_result').text("Адрес не найден.");
            set_default_map();
        }

        if (obj) {
            show_result(obj, error);
        }
    }

    function show_result(obj, error) {
        $('#map').css('display', 'block');

        let map_container = $('#map');
        let map_state = ymaps.util.bounds.getCenterAndZoom(
            obj.properties.get('boundedBy'),
            [map_container.width(), map_container.height()]
        );
        map.panTo(obj.geometry.getCoordinates(), map_state.zoom);

        let address = [obj.getCountry(), obj.getAddressLine()].join(', ');

        updaate_placemark(obj, error);

        if ($('#address_suggest_form').val() == '') {
            suggest_view.options.set('provider', 'none');
            document.getElementById("address_suggest_form").value = address;
        }

        if (error) {
            $('#adders_check_result').text(error + ` (найдено: ${address})`);
        } else {
            $('#adders_check_result').text("Адрес вашей площадки: " + address);
        }
    }

    function updaate_placemark(obj, error) {
        let placemark_preset = 'islands#greenDotIconWithCaption';
        if (error) {
            placemark_preset = 'islands#redDotIconWithCaption';
        }

        map.geoObjects.add(placemark);

        placemark.geometry.setCoordinates(obj.geometry.getCoordinates());
        placemark.options.set('preset', placemark_preset);
        placemark.properties.set({
            iconCaption: [
                obj.getLocalities().length ? obj.getLocalities() : obj.getAdministrativeAreas(),
                obj.getThoroughfare() || obj.getPremise()
            ].filter(Boolean).join(', '),

            balloonContent: obj.getAddressLine()
        });
    }
}


//<script src="//api-maps.yandex.ru/2.1/?lang=ru_RU&amp;onload=onLoad"></script>
//<script>
//    function onLoad (ymaps) {
//        var suggestView = new ymaps.SuggestView('suggest', {
//            boundedBy: [[48.215401, 43.823443], [49.032926, 45.196734]],
//            provider: {
//                suggest: (function(request, options) {
//                    request = "Россия, Волгоградская область, " + request;
//                    return (suggestView.state.get('open') ? ymaps.suggest(request) : ymaps.vow.resolve([])).then(function (res) {
//                        suggestView.events.fire('requestsuccess', {
//                            target: suggestView,
//                        });
//                        return res;
//                    })
//                })
//            }
//        });
//        suggestView.state.set('open', true);
//        suggestView.events.add('select', function (e) {
//            var value = e.get('item').value;
//            var streets = [
//                'Россия, Волгоградская область, ',
//                'Россия, Волгоград, '
//            ];
//            for (var i = 0; i < streets.length; i++) {
//                value = value.replace(streets[i], '');
//            }
//            var house = value.substring(value.indexOf(", ") + 2);
//            var firstLetter = parseInt(house[0]);
//            suggestView.state.set({open: false});
//            if(!_.isNaN(firstLetter) && _.isNumber(firstLetter)) {
//                $('[data-js-basket-form-house]').val(house);
//                $('[data-js-basket-form-street]').val(value.replace(', ' + house, ''));
//            } else {
//                $('[data-js-basket-form-street]').val(value);
//            }
//            suggestView.events.once('requestsuccess', function () {
//                suggestView.state.set('open', true);
//            });
//        });
//    }
//</script>