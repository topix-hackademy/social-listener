var WebpackBuildNotifierPlugin = require('webpack-build-notifier');

module.exports = {

  entry: {
    main: './static/js/main.js'
  },

  output: {
    filename: "build.js",
    path: __dirname + "/static/build/"
  },

  module : {

    loaders: [

      { test: /\.html$/, loader: 'to-string!html-loader' },
      { test: /\.css$/, loader: 'to-string!style-loader!css-loader!postcss-loader' },
      { test: /\.scss$/, loader: 'to-string!style-loader!css-loader!postcss-loader!sass-loader' }
      ,
      {
        test: /\.js(x?)$/, loader: 'babel-loader' ,
        exclude:  /(node_modules|vendor)/,
        query: {
          presets: [ 'es2015' , 'stage-0' ],
        }
      }
      ,
      { test: /\.(png|woff|woff2|eot|ttf|svg|json)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader?limit=100000&name=../fonts/[hash].[ext]' }
    ]

  },

  resolve: {
    extensions: ['', '.webpack.js', '.web.js', '.ts', '.tsx', '.js', '.css', '.scss', '.sass']
  },


  plugins: [
    new WebpackBuildNotifierPlugin({
      suppressWarning: true,
      activateTerminalOnError :true
    })
  ]

};