/**
 * Created by huipo on 17-3-23.
 */
var _ = require('underscore')
// console.log(_)
mapResult=_.map([1,2,3],function (num) {
    return num*3
})
console.log(mapResult)