/** @format */

import $ from "jquery";
import { Signup } from "./signup";

let burgerMenu = $("[data-burger-menu]");

$("[data-open-burger]").on("click", () => {
    burgerMenu.show();
});

$("[data-close-burger]").on("click", () => {
    burgerMenu.hide();
});

let carouselElem = document.querySelector(
    "[data-carousel-container]"
) as HTMLElement;

if (carouselElem) {
    import("./carousel").then(carousel => {
        carousel.setup(carouselElem);
    });
}

if (document.querySelector("[data-faq-question]")) {
    import("./faqs").then(faqs => {
        faqs.setup();
    });
}

if (document.querySelector("#google-map")) {
    import("./map").then(map => {
        map.setup();
    });
}

let signupForms = $("[data-signup-form]");

for (let signupForm of signupForms) {
    new Signup(signupForm as HTMLFormElement);
}

if (document.querySelector("[data-dropzone]")) {
    import("../dropzone").then(dz => {
        dz.setup();
    });
}

let quoteForm = document.querySelector("[data-quote-form]") as HTMLElement;

if (quoteForm) {
    import("./capture").then(capture => {
        capture.setup(quoteForm);
    });
}

let barometerElem = document.querySelector("[data-barometer]") as HTMLElement;

if (barometerElem) {
    import("./barometer").then(barometer => {
        barometer.setup(barometerElem);
    });
}

let newsEntries = $(".news__entry");
let line = [];

newsEntries.each((index, element) => {
    line.push(element);

    if ($(element) === newsEntries.last() || line.length === 3) {
        let tallest = element;

        for (let elem of line) {
            if (elem.offsetHeight > tallest.offsetHeight) {
                tallest = elem;
            }
        }

        for (let elem of line) {
            $(elem).css("height", `${tallest.offsetHeight}px`);
        }

        line = [];
    }
});
