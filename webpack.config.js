const path = require('path');
const BundleTracker = require('webpack4-bundle-tracker');
const MomentLocalesPlugin = require('moment-locales-webpack-plugin');

module.exports = {
    output: {
        path: path.resolve(__dirname, "output/dist"),
        filename: "[name]-[contenthash].js",
    },
    resolve: {
        extensions: ['.ts', '.js']
    },
    entry: {
        www: './js/www/_entrypoint.ts',
    },
    mode: 'production',
    devtool: 'source-map',
    plugins: [
        new BundleTracker({
            filename: './webpack-stats.json',
            indent: 2,
        }),
        new MomentLocalesPlugin(),
    ],
    optimization: {
        runtimeChunk: 'single',
        splitChunks: {
            chunks: 'all',
            name: false,
        },
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /(node_modules|bower_components)/
            },
            {
                test: /\.m?js$/,
                exclude: /node_modules\/(?!unfetch\/)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            ['@babel/preset-env', {
                                "useBuiltIns": 'entry',
                                "corejs": 3
                            }]
                        ]
                    }
                }
            },
        ]
    }
}
