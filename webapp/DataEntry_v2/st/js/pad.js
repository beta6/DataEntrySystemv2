function pad(n, l) {
    var padding = Array(l).join("0");
    var str = n.toString();
    return (padding + str).slice(-l);
}
