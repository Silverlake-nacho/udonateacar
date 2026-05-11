/** @format */

const lake = { lat: 50.918563, lng: -1.23246 };

export function setup() {
    const map = new google.maps.Map(
        document.getElementById("google-map") as HTMLElement,
        {
            zoom: 10,
            center: lake,
        }
    );

    new google.maps.Marker({
        position: lake,
        map: map,
    });
}
