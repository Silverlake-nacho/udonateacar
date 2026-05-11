/** @format */

import $ from "jquery";

export class Question {
    element: HTMLElement;
    questions: Array<Question>;

    answer_element: HTMLElement;

    constructor(element: HTMLElement, questions: Array<Question>) {
        this.element = element;
        this.questions = questions;

        this.answer_element = element.querySelector(
            "[data-faq-question-answer]"
        );

        this.element.addEventListener("click", event => {
            this.click(event);
        });
    }

    get active(): boolean {
        return this.element.classList.contains("active");
    }
    set active(value: boolean) {
        this.element.classList.toggle("active", value);

        if (value) {
            // Show the body of the question
            $(this.answer_element).slideDown();

            let url = this.element.dataset.url;

            if (url) {
                // Set the address bar for URL positive reasons
                history.replaceState({}, "", url);
            }

            // Close all other "active" questions when a new
            // one becomes active.
            for (const question of this.questions) {
                if (question === this) {
                    continue;
                }

                question.active = false;
            }
        } else {
            // Hide the body of the question
            $(this.answer_element).slideUp();
        }
    }
    click(event: MouseEvent) {
        this.active = !this.active;
    }
}

export function setup() {
    let questions = [];
    let elements = $("[data-faq-question]");

    elements.each(function() {
        let q = new Question(this, questions);
        questions.push(q);
    });
}
