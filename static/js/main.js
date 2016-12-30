/**
 * Created by andreafspeziale on 29/12/16.
 */
window.$ = window.jQuery = require('jquery');
require('bootstrap-loader');
var angular = require('angular');
require('../style/main.scss');
require('angular-toastr');


var tagConfig = require("./config/angular.config");

var app = angular.module("SocialListener", ['toastr']);
app.config(tagConfig);

require('./controller');
