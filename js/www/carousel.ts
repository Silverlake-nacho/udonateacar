/** @format */

import $ from "jquery";

export function setup(container: HTMLElement) {
    /** Attaches "carousel-like" behaviour to a given element.
     *
     * <section>
     *   <div data-carousel-container>
     *     <p data-carousel-item style="display: block;">First</p>
     *     <p data-carousel-item style="display: none;">Second</p>
     *     <p data-carousel-item style="display: none;">Third</p>
     *   </div>
     *   <span data-carousel-controls="right">FORWARD</span>
     *   <span data-carousel-controls="left">BACKWARD</span>
     * </section>
     *
     * When an element with "[data-carousel-controls="right|left"]" is clicked,
     * the current element displayed is hidden, and then the next/previous
     * element in the set of "[data-carousel-container] [data-carousel-item]"
     * is displayed with inline style attributes. Going backwards and
     * forwards at the start and end of the collection of items is handled.
     *
     */
    let items = $(container).find("[data-carousel-item]");
    let index = 0;
    let inProgress = false;

    $(container).on("click", "[data-carousel-controls]", event => {
        if (inProgress) {
            return;
        }
        inProgress = true;
        let direction = event.currentTarget.dataset.carouselControls;
        let adjustment = 0;
        if (direction == "left") {
            adjustment = -1;
        } else if (direction == "right") {
            adjustment = 1;
        }

        let new_index = index + adjustment;
        if (new_index >= items.length) {
            new_index = 0;
        }
        if (new_index < 0) {
            new_index = items.length - 1;
        }

        $(items).fadeOut(500);

        $(items)
            .eq(new_index)
            .delay(500)
            .fadeIn(500, () => {
                inProgress = false;
                index = new_index;
            });
    });

    $(container).height($(container).height());
}
