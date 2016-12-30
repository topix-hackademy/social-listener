function tagConfig($interpolateProvider) {
    $interpolateProvider.startSymbol("{[{");
    $interpolateProvider.endSymbol("}]}");
}

tagConfig.$inject = ["$interpolateProvider"];
module.exports = tagConfig;
