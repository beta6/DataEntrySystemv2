/*! imgareaselect 1.0.0-rc.1 */
(function(e) {
    function t() {
        return e("<div/>")
    }
    var o = Math.abs,
        n = Math.max,
        i = Math.min,
        s = Math.round;
    e.imgAreaSelect = function(a, c) {
        function r(e) {
            return e + bt.left - St.left
        }

        function d(e) {
            return e + bt.top - St.top
        }

        function u(e) {
            return e - bt.left + St.left
        }

        function h(e) {
            return e - bt.top + St.top
        }

        function f(e) {
            var t, o = m(e) || e;
            return (t = parseInt(o.pageX)) ? t - St.left : void 0
        }

        function l(e) {
            var t, o = m(e) || e;
            return (t = parseInt(o.pageY)) ? t - St.top : void 0
        }

        function m(e) {
            var t = e.originalEvent || {};
            return t.touches && t.touches.length ? t.touches[0] : !1
        }

        function p(e) {
            var t = e || G,
                o = e || J;
            return {
                x1: s(At.x1 * t),
                y1: s(At.y1 * o),
                x2: s(At.x2 * t) - 1,
                y2: s(At.y2 * o) - 1,
                width: s(At.x2 * t) - s(At.x1 * t),
                height: s(At.y2 * o) - s(At.y1 * o)
            }
        }

        function v(e, t, o, n, i) {
            var a = i || G,
                c = i || J;
            At = {
                x1: s(e / a || 0),
                y1: s(t / c || 0),
                x2: s(++o / a || 0),
                y2: s(++n / c || 0)
            }, At.width = At.x2 - At.x1, At.height = At.y2 - At.y1
        }

        function y() {
            $ && pt.width() && (bt = {
                left: s(pt.offset().left),
                top: s(pt.offset().top)
            }, Q = pt.innerWidth(), R = pt.innerHeight(), bt.top += pt.outerHeight() - R >> 1, bt.left += pt.outerWidth() - Q >> 1, V = s(c.minWidth / G) || 0, Z = s(c.minHeight / J) || 0, _ = s(i(c.maxWidth / G || 1 << 24, Q)), et = s(i(c.maxHeight / J || 1 << 24, R)), St = "fixed" == kt ? {
                left: e(document).scrollLeft(),
                top: e(document).scrollTop()
            } : /static|^$/.test(X.css("position")) ? {
                left: 0,
                top: 0
            } : {
                left: s(X.offset().left) - X.scrollLeft(),
                top: s(X.offset().top) - X.scrollTop()
            }, L = r(0), j = d(0), (At.x2 > Q || At.y2 > R) && P())
        }

        function g(t) {
            if (ot) {
                switch (vt.css({
                    left: r(At.x1),
                    top: d(At.y1)
                }).add(yt).width(ft = At.width).height(lt = At.height), yt.add(gt).add(wt).css({
                    left: 0,
                    top: 0
                }), gt.add(xt).width(n(ft - gt.outerWidth() + gt.innerWidth(), 0)).height(n(lt - gt.outerHeight() + gt.innerHeight(), 0)), xt.css({
                    left: L,
                    top: j,
                    width: ft,
                    height: lt,
                    borderStyle: "solid",
                    borderWidth: At.y1 + "px " + (Q - At.x2) + "px " + (R - At.y2) + "px " + At.x1 + "px"
                }), ft -= wt.outerWidth(), lt -= wt.outerHeight(), wt.length) {
                    case 8:
                        e(wt[4]).css({
                            left: ft >> 1
                        }), e(wt[5]).css({
                            left: ft,
                            top: lt >> 1
                        }), e(wt[6]).css({
                            left: ft >> 1,
                            top: lt
                        }), e(wt[7]).css({
                            top: lt >> 1
                        });
                    case 4:
                        wt.slice(1, 3).css({
                            left: ft
                        }), wt.slice(2, 4).css({
                            top: lt
                        })
                }
                t !== !1 && (e.imgAreaSelect.keyPress != Pt && e(document).unbind(e.imgAreaSelect.keyPress, e.imgAreaSelect.onKeyPress), c.keys && e(document)[e.imgAreaSelect.keyPress](e.imgAreaSelect.onKeyPress = Pt))
            }
        }

        function x(e) {
            y(), g(e), nt = r(At.x1), it = d(At.y1), st = r(At.x2), at = d(At.y2)
        }

        function w(e, t) {
            c.fadeDuration ? e.fadeOut(c.fadeDuration, t) : e.hide()
        }

        function b(e) {
            return ct && !/^touch/.test(e.type)
        }

        function S(e) {
            var t = u(f(e)) - At.x1,
                o = h(l(e)) - At.y1;
            U = "", c.resizable && (c.resizeMargin >= o ? U = "n" : o >= At.height - c.resizeMargin && (U = "s"), c.resizeMargin >= t ? U += "w" : t >= At.width - c.resizeMargin && (U += "e")), vt.css("cursor", U ? U + "-resize" : c.movable ? "move" : "")
        }

        function z(e) {
            b(e) || (mt || (y(), mt = !0, vt.one("mouseout", function() {
                mt = !1
            })), S(e))
        }

        function k(t) {
            ct = !1, e("body").css("cursor", ""), (c.autoHide || 0 == At.width * At.height) && w(vt.add(xt), function() {
                e(this).hide()
            }), e(document).off("mousemove touchmove", N), vt.on("mousemove touchmove", z), t && c.onSelectEnd(a, p())
        }

        function A(t) {
            return "mousedown" == t.type && 1 != t.which ? !1 : ("touchstart" == t.type ? (ct && k(), ct = !0, S(t)) : y(), U ? (nt = r(At["x" + (1 + /w/.test(U))]), it = d(At["y" + (1 + /n/.test(U))]), st = r(At["x" + (1 + !/w/.test(U))]), at = d(At["y" + (1 + !/n/.test(U))]), B = st - f(t), F = at - l(t), e(document).on("mousemove touchmove", N).one("mouseup touchend", k), vt.off("mousemove touchmove", z)) : c.movable ? (Y = L + At.x1 - f(t), q = j + At.y1 - l(t), vt.off("mousemove touchmove", z), e(document).on("mousemove touchmove", H).one("mouseup touchend", function() {
                ct = !1, c.onSelectEnd(a, p()), e(document).off("mousemove touchmove", H), vt.on("mousemove touchmove", z)
            })) : pt.mousedown(t), !1)
        }

        function I(e) {
            tt && (e ? (st = n(L, i(L + Q, nt + o(at - it) * tt * (st > nt || -1))), at = s(n(j, i(j + R, it + o(st - nt) / tt * (at > it || -1)))), st = s(st)) : (at = n(j, i(j + R, it + o(st - nt) / tt * (at > it || -1))), st = s(n(L, i(L + Q, nt + o(at - it) * tt * (st > nt || -1)))), at = s(at)))
        }

        function P() {
            nt = i(nt, L + Q), it = i(it, j + R), V > o(st - nt) && (st = nt - V * (nt > st || -1), L > st ? nt = L + V : st > L + Q && (nt = L + Q - V)), Z > o(at - it) && (at = it - Z * (it > at || -1), j > at ? it = j + Z : at > j + R && (it = j + R - Z)), st = n(L, i(st, L + Q)), at = n(j, i(at, j + R)), I(o(st - nt) < o(at - it) * tt), o(st - nt) > _ && (st = nt - _ * (nt > st || -1), I()), o(at - it) > et && (at = it - et * (it > at || -1), I(!0)), At = {
                x1: u(i(nt, st)),
                x2: u(n(nt, st)),
                y1: h(i(it, at)),
                y2: h(n(it, at)),
                width: o(st - nt),
                height: o(at - it)
            }
        }

        function K() {
            P(), g(), c.onSelectChange(a, p())
        }

        function N(e) {
            return b(e) ? void 0 : (P(), st = /w|e|^$/.test(U) || tt ? f(e) + B : r(At.x2), at = /n|s|^$/.test(U) || tt ? l(e) + F : d(At.y2), K(), !1)
        }

        function C(t, o) {
            st = (nt = t) + At.width, at = (it = o) + At.height, e.extend(At, {
                x1: u(nt),
                y1: h(it),
                x2: u(st),
                y2: h(at)
            }), g(), c.onSelectChange(a, p())
        }

        function H(e) {
            return b(e) ? void 0 : (nt = n(L, i(Y + f(e), L + Q - At.width)), it = n(j, i(q + l(e), j + R - At.height)), C(nt, it), e.preventDefault(), !1)
        }

        function M() {
            e(document).off("mousemove touchmove", M), y(), st = nt, at = it, K(), U = "", xt.is(":visible") || vt.add(xt).hide().fadeIn(c.fadeDuration || 0), ot = !0, e(document).off("mouseup touchend", W).on("mousemove touchmove", N).one("mouseup touchend", k), vt.off("mousemove touchmove", z), c.onSelectStart(a, p())
        }

        function W() {
            e(document).off("mousemove touchmove", M).off("mouseup touchend", W), w(vt.add(xt)), v(u(nt), h(it), u(nt), h(it)), this instanceof e.imgAreaSelect || (c.onSelectChange(a, p()), c.onSelectEnd(a, p()))
        }

        function D(t) {
            return "mousedown" == t.type && 1 != t.which || xt.is(":animated") ? !1 : (ct = "touchstart" == t.type, y(), Y = nt = f(t), q = it = l(t), B = F = 0, e(document).on({
                "mousemove touchmove": M,
                "mouseup touchend": W
            }), !1)
        }

        function E() {
            x(!1)
        }

        function O() {
            $ = !0, T(c = e.extend({
                classPrefix: "imgareaselect",
                movable: !0,
                parent: "body",
                resizable: !0,
                resizeMargin: 10,
                onInit: function() {},
                onSelectStart: function() {},
                onSelectChange: function() {},
                onSelectEnd: function() {}
            }, c)), c.show && (ot = !0, y(), g(), vt.add(xt).hide().fadeIn(c.fadeDuration || 0)), setTimeout(function() {
                c.onInit(a, p())
            }, 0)
        }

        function T(o) {
            if (o.parent && (X = e(o.parent)).append(vt).append(xt), e.extend(c, o), y(), null != o.handles) {
                for (wt.remove(), wt = e([]), ut = o.handles ? "corners" == o.handles ? 4 : 8 : 0; ut--;) wt = wt.add(t());
                wt.addClass(c.classPrefix + "-handle").css({
                    position: "absolute",
                    fontSize: 0,
                    zIndex: zt + 1 || 1
                }), !parseInt(wt.css("width")) >= 0 && wt.width(5).height(5)
            }
            for (G = c.imageWidth / Q || 1, J = c.imageHeight / R || 1, null != o.x1 && (v(o.x1, o.y1, o.x2, o.y2), o.show = !o.hide), o.keys && (c.keys = e.extend({
                    shift: 1,
                    ctrl: "resize"
                }, o.keys)), xt.addClass(c.classPrefix + "-outer"), yt.addClass(c.classPrefix + "-selection"), ut = 0; 4 > ut++;) e(gt[ut - 1]).addClass(c.classPrefix + "-border" + ut);
            vt.append(yt.add(gt)).append(wt), Kt && ((ht = (xt.css("filter") || "").match(/opacity=(\d+)/)) && xt.css("opacity", ht[1] / 100), (ht = (gt.css("filter") || "").match(/opacity=(\d+)/)) && gt.css("opacity", ht[1] / 100)), o.hide ? w(vt.add(xt)) : o.show && $ && (ot = !0, vt.add(xt).fadeIn(c.fadeDuration || 0), x()), tt = (dt = (c.aspectRatio || "").split(/:/))[0] / dt[1], pt.add(xt).off("mousedown touchstart", D), c.disable || c.enable === !1 ? (vt.off({
                "mousemove touchmove": z,
                "mousedown touchstart": A
            }), e(window).off("resize", E)) : ((c.enable || c.disable === !1) && ((c.resizable || c.movable) && vt.on({
                "mousemove touchmove": z,
                "mousedown touchstart": A
            }), e(window).resize(E)), c.persistent || pt.add(xt).on("mousedown touchstart", D)), c.enable = c.disable = void 0
        }
        var $, L, j, Q, R, X, Y, q, B, F, G, J, U, V, Z, _, et, tt, ot, nt, it, st, at, ct, rt, dt, ut, ht, ft, lt, mt, pt = e(a),
            vt = t(),
            yt = t(),
            gt = t().add(t()).add(t()).add(t()),
            xt = t(),
            wt = e([]),
            bt = {
                left: 0,
                top: 0
            },
            St = {
                left: 0,
                top: 0
            },
            zt = 0,
            kt = "absolute",
            At = {
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 0,
                width: 0,
                height: 0
            },
            It = navigator.userAgent,
            Pt = function(e) {
                var t, o, s = c.keys,
                    a = e.keyCode;
                if (t = isNaN(s.alt) || !e.altKey && !e.originalEvent.altKey ? !isNaN(s.ctrl) && e.ctrlKey ? s.ctrl : !isNaN(s.shift) && e.shiftKey ? s.shift : isNaN(s.arrows) ? 10 : s.arrows : s.alt, "resize" == s.arrows || "resize" == s.shift && e.shiftKey || "resize" == s.ctrl && e.ctrlKey || "resize" == s.alt && (e.altKey || e.originalEvent.altKey)) {
                    switch (a) {
                        case 37:
                            t = -t;
                        case 39:
                            o = n(nt, st), nt = i(nt, st), st = n(o + t, nt), I();
                            break;
                        case 38:
                            t = -t;
                        case 40:
                            o = n(it, at), it = i(it, at), at = n(o + t, it), I(!0);
                            break;
                        default:
                            return
                    }
                    K()
                } else switch (nt = i(nt, st), it = i(it, at), a) {
                    case 37:
                        C(n(nt - t, L), it);
                        break;
                    case 38:
                        C(nt, n(it - t, j));
                        break;
                    case 39:
                        C(nt + i(t, Q - u(st)), it);
                        break;
                    case 40:
                        C(nt, it + i(t, R - h(at)));
                        break;
                    default:
                        return
                }
                return !1
            };
        this.remove = function() {
            T({
                disable: !0
            }), vt.add(xt).remove()
        }, this.getOptions = function() {
            return c
        }, this.setOptions = T, this.getSelection = p, this.setSelection = v, this.cancelSelection = W, this.update = x;
        var Kt = (/msie ([\w.]+)/i.exec(It) || [])[1],
            Nt = /webkit/i.test(It) && !/chrome/i.test(It);
        for (rt = pt; rt.length;) zt = n(zt, isNaN(rt.css("z-index")) ? zt : rt.css("z-index")), c.parent || "fixed" != rt.css("position") || (kt = "fixed"), rt = rt.parent(":not(body)");
        zt = c.zIndex || zt, e.imgAreaSelect.keyPress = Kt || Nt ? "keydown" : "keypress", vt.add(xt).hide().css({
            position: kt,
            overflow: "hidden",
            zIndex: zt || "0"
        }), vt.css({
            zIndex: zt + 2 || 2
        }), yt.add(gt).css({
            position: "absolute",
            fontSize: 0
        }), a.complete || "complete" == a.readyState || !pt.is("img") ? O() : pt.one("load", O), !$ && Kt && Kt >= 7 && (a.src = a.src)
    }, e.fn.imgAreaSelect = function(t) {
        return t = t || {}, this.each(function() {
            e(this).data("imgAreaSelect") ? t.remove ? (e(this).data("imgAreaSelect").remove(), e(this).removeData("imgAreaSelect")) : e(this).data("imgAreaSelect").setOptions(t) : t.remove || (void 0 === t.enable && void 0 === t.disable && (t.enable = !0), e(this).data("imgAreaSelect", new e.imgAreaSelect(this, t)))
        }), t.instance ? e(this).data("imgAreaSelect") : this
    }
})(jQuery);