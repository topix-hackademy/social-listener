module.exports.flashcontroller = ['$scope', 'toastr', ($scope, toastr) => {
    $scope.initToastr = (flash_message, flash_status) => {

        if(flash_message==undefined || flash_message=="" || flash_message==null) return;
        switch (flash_status){
            case 'success':
                toastr.success(flash_message, "Yeah!");
                break;
            case 'warning':
                toastr.warning(flash_message, "Warning!");
                break;
            case 'danger':
                toastr.error(flash_message, "Error!");
                break;
        }
    };
}];
