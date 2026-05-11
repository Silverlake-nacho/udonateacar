/** @format */

import $ from "jquery";
import "jquery-validation";
import "../extra_validators";
import Cookies from "js-cookie";
import { check_response, NotOkResponseError } from "../toolkit";

export class Signup {
    form: JQuery<HTMLFormElement>;
    vrmInput: JQuery<HTMLElement>;
    postcodeInput: JQuery<HTMLElement>;
    submitElem: JQuery<HTMLElement>;

    endpoint: string = "/api/v0/create-lead";

    constructor(form: HTMLFormElement) {
        this.form = $(form) as JQuery<HTMLFormElement>;
        this.vrmInput = this.form.find("[name=vrm]");
        this.postcodeInput = this.form.find("[name=postcode]");
        this.submitElem = this.form.find("[data-submit]");

        this.validate();
        this.setupListeners();
    }

    validate(): void {
        (this.form as any).validate({
            onKeyup: true,
            rules: {
                vrm: {
                    required: true,
                    vrm: true,
                },
                postcode: {
                    required: true,
                    postcode: true,
                },
            },
        });
    }

    setupListeners(): void {
        this.submitElem.on("click", () => {
            this.submit();
        });

        this.form.on("keydown", event => {
            if (event.key === "ENTER") {
                this.submit();
            }
        });
    }

    async submit(): Promise<void> {
        if (!(<any>this.form).valid()) {
            return;
        }

        if (this.submitElem.find(".loader").length) {
            return;
        }

        let beforeButtonHTML = this.submitElem.html();
        this.submitElem.html("<div class='loader'></div>");

        let vrm = this.vrmInput.val() as string;
        let postcode = this.postcodeInput.val() as string;

        try {
            await this.apiRequest(vrm, postcode);
        } catch (e) {
            alert("Please check the registration and postcode, then retry");
            this.submitElem.html(beforeButtonHTML);
            return;
        }

        this.submitElem.html(beforeButtonHTML);
        location.href = "/capture/contact";
    }

    async apiRequest(vrm: string, postcode: string): Promise<Response> {
        let data = {
            vrm: vrm.toUpperCase(),
            postcode: postcode.toUpperCase(),
        };

        return fetch(this.endpoint, {
            method: "post",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify(data),
            credentials: "same-origin",
        }).then(check_response);
    }
}
