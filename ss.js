function hexToArray(e){
    const t = [];
    let o = e.length;
    o % 2 != 0 && (e = Jr(e, o + 1)),
        o = e.length;
    for (let l = 0; l < o; l += 2)
        t.push(parseInt(e.substr(l, 2), 16));
    return t
}
function utf8ToHex(e){
    const t = (e = unescape(encodeURIComponent(e))).length
        , o = [];
    for (let i = 0; i < t; i++)
        o[i >>> 2] |= (255 & e.charCodeAt(i)) << 24 - i % 4 * 8;
    const l = [];
    for (let i = 0; i < t; i++) {
        const e = o[i >>> 2] >>> 24 - i % 4 * 8 & 255;
        l.push((e >>> 4).toString(16)),
            l.push((15 & e).toString(16))
    }
    return l.join("")
}
function getGlobalCurve() {
    return Yr
}
function doEncrypt (e, t, o=1){
    e = "string" == typeof e ? hexToArray(utf8ToHex(e)) : Array.prototype.slice.call(e),
        t = getGlobalCurve().decodePointHex(t);
    const l = ha.generateKeyPairHex()
        , i = new sa(l.privateKey,16);
    let r = l.publicKey;
    r.length > 128 && (r = r.substr(r.length - 128));
    const a = t.multiply(i)
        , c = ha.hexToArray(ha.leftPad(a.getX().toBigInteger().toRadix(16), 64))
        , n = ha.hexToArray(ha.leftPad(a.getY().toBigInteger().toRadix(16), 64))
        , s = ha.arrayToHex(ma([].concat(c, e, n)));
    let p = 1
        , d = 0
        , h = [];
    const m = [].concat(c, n)
        , b = ()=>{
            h = ma([...m, p >> 24 & 255, p >> 16 & 255, p >> 8 & 255, 255 & p]),
                p++,
                d = 0
        }
    ;
    b();
    for (let f = 0, g = e.length; f < g; f++)
        d === h.length && b(),
            e[f] ^= 255 & h[d++];
    const u = ha.arrayToHex(e);
    return 0 === o ? r + u + s : r + s + u
}
e='{"platformCode":"","noticeName":"","tradeType":"0","link":"ALL","pageSize":10,"page":49,"important":"","remote":""}'
t='03702057B53C16031D786D9E06D839163F3DD5867E6E161292F61E1340FDF6DE24'
console.log(doEncrypt(e,t,1))