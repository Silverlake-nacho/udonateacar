/** @format */

import $ from "jquery";
import "jquery-validation";
import "../extra_validators";
import Cookies from "js-cookie";
import { check_response } from "../toolkit";

export function setup(form: HTMLElement) {
    validateForm(form);
    setupListeners(form);
}

function validateForm(form: HTMLElement) {
    (<any>$(form)).validate({
        onKeyup: true,
        rules: {
            name: {
                required: true,
                fullname: true,
            },
            phone: {
                required: true,
                ukPhone: true,
            },
            email: {
                required: true,
                email: true,
            },
            street: {
                required: true,
                minlength: 5,
            },
            house_flat_number: {
                required: true,
            },
            town: {
                required: true,
                minlength: 3,
            },
            postcode: {
                required: true,
                postcode: true,
            },
        },
    });
}

function setupListeners(form: HTMLElement) {
    $("[data-continue]").on("click", async event => {
        if (!(<any>$(form)).valid()) {
            return;
        }

        let clicked = $(event.target) as JQuery<HTMLElement>;

        if (clicked.find(".loader").length) {
            return;
        }

        let beforeButtonHTML = clicked.html();
        clicked.html("<div class='loader'></div>");

        let answers = {};

        $("input, select").each((index, element) => {
            answers[$(element).attr("name")] = $(element).val();
        });

        try {
            await apiRequest(answers);
        } catch (e) {
            alert("Sorry, there was an error. Please try again later.");
            clicked.html(beforeButtonHTML);
            return;
        }

        let nextUrl = "/capture/collection";

        if (window.location.pathname == nextUrl) {
            nextUrl = "/capture/thank-you";
        }

        location.href = nextUrl;
    });

    $("[data-back]").on("click", () => {
        let previousUrl = "/capture/contact";

        if (window.location.pathname == previousUrl) {
            previousUrl = "/";
        }

        location.href = previousUrl;
    });
}

async function apiRequest(answers: object) {
    let data = {
        url: window.location.pathname,
        answers: answers,
    };

    await fetch("/api/v0/save-answers", {
        method: "post",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(data),
        credentials: "same-origin",
    }).then(check_response);
}
