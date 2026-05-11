/** @format */

import $ from "jquery";
import Cookies from "js-cookie";
import Dropzone from "dropzone";

let uploadedFiles = {};

export function setup() {
    let dropper = new Dropzone("[data-dropzone]", {
        url: "/api/v0/save-vehicle-image",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
        acceptedFiles: "image/jpeg,image/png,.bmp",
        autoProcessQueue: true,
        maxFiles: 12,
        addRemoveLinks: true,
        maxFilesize: 4,
    });

    dropper.on("addedfile", file => {
        $("[data-dropzone-content]").hide();
        uploadedFiles[file.name] = file;
    });

    $("[data-dropzone]").on("click", ".dz-error-mark", event => {
        let clicked = $(event.target) as JQuery<HTMLElement>;
        let image = clicked.closest(".dz-preview").find("[data-dz-thumbnail]");
        let name = image.attr("alt");

        fetch("/api/v0/delete-vehicle-image", {
            method: "POST",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify({
                image: name,
            }),
        });

        dropper.removeFile(uploadedFiles[name]);
        delete uploadedFiles[name];

        if (Object.keys(uploadedFiles).length == 0) {
            $("[data-dropzone-content]").show();
        }
    });

    $("[data-dropzone-upload]").on("click", () => {
        $("[data-dropzone]").click();
    });
}
