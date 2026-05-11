/** @format */

export function check_response(response: Response): Response {
    if (!response.ok) {
        throw new NotOkResponseError(response);
    } else {
        return response;
    }
}

export function getContext(): object {
    let element = document.getElementById("js-context");
    if (!element) {
        return {};
    } else {
        return JSON.parse(element.textContent);
    }
}

export class NotOkResponseError extends Error {
    response: Response;

    constructor(response: Response) {
        let url = response.url;
        let code = response.status;
        let description = response.statusText;
        super(`Response (${url}) was ${code} - ${description}`);

        this.response = response;
        this.name = "NotOkResponseError";
    }
}
