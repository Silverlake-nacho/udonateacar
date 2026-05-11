/** @format */
const { src, dest, series, parallel, watch } = require("gulp");
const child_process = require("child_process");

const rename = require("gulp-rename");
const sourcemaps = require("gulp-sourcemaps");
const sass = require('gulp-sass')(require('sass'));
sass.compiler = require("sass");

const { spawn } = require("child_process");

const SCSS_GLOB = "style/*/*.scss";
const SCSS_COMPONENTS = "style/*/components/*.scss";

// Compile SCSS into CSS
function scss_into_css() {
    return src(SCSS_GLOB)
        .pipe(sourcemaps.init())
        .pipe(
            sass({
                includePaths: ["./node_modules"],
            })
        )
        .pipe(
            rename({
                dirname: ".",
                suffix: ".min",
            })
        )
        .pipe(sourcemaps.write("./maps"))
        .pipe(dest("output/style/"));
}
exports.css = scss_into_css;

function webpack() {
    return new Promise((resolve, reject) => {
        let args = ["webpack"];
        if (process.env.NODE_ENV === "development") {
            args.push("--mode=development");
        }

        let proc = child_process.spawn("npx", args, {
            stdio: "inherit",
        });

        proc.on("exit", (code, signal) => {
            if (code === 0) {
                resolve();
            } else if (signal === null) {
                reject(new Error(`webpack exited with code: ${code}`));
            } else {
                reject(new Error(`webpack killed by signal: ${signal}`));
            }
        });

        proc.on("error", error => {
            reject(error);
        });
    });
}

exports.webpack = webpack;

function watch_js() {
        watch(["js/**/*.js", "js/**/*.ts"], webpack);
}

function watch_css() {
    watch([SCSS_GLOB, SCSS_COMPONENTS], scss_into_css);

}

exports.watch_css = watch_css;

function fa_fonts() {
    return src("node_modules/@fortawesome/fontawesome-pro/webfonts/**/*").pipe(
        dest("output/webfonts/")
    );
}

function fa_scss() {
    return src("node_modules/@fortawesome/fontawesome-pro/scss/**/*").pipe(
        dest("style/fontawesome/")
    );
}

exports.fontawesome = parallel(fa_fonts, fa_scss);

exports.build = parallel(
    series(exports.fontawesome, exports.css),
    webpack,
);

exports.default = exports.build;
exports.watch = series(exports.build, parallel(watch_css, watch_js));
