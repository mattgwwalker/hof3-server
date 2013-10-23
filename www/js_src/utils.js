// ************
// Utility code
// ************

function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function isUndefined(x) {
    return typeof x === "undefined";
}

function isDefined(x) {
    return typeof x !== "undefined";
}
