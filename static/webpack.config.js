const webpack = require('webpack');


const config = {
    entry: __dirname + '/js/index.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',

    },
    resolve: {
        extensions: ['.js', ',jsx', '.css']
    },
};

module.exports = config;

module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        } 
      }
    ]
}