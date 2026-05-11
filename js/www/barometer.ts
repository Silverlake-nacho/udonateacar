/** @format */

import $ from "jquery";
import { getContext } from "../toolkit";

export function setup(elem: HTMLElement) {
    let total = parseInt($(elem).attr("data-barometer"));
    let value = getContext()["total_raised"];
    let percentage = (value / total) * 100;

    let stalk = $("[data-barometer-stalk]");

    stalk.animate({ width: `${percentage}%` }, { duration: 2000 });
}
