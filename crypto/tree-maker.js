var treeMaker;
(() => {
    "use strict"; var t = {
        d: (e, n) => { for (var r in n) t.o(n, r) && !t.o(e, r) && Object.defineProperty(e, r, { enumerable: !0, get: n[r] }) },
        o: (t, e) => Object.prototype.hasOwnProperty.call(t, e), r: t => {
            "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
                Object.defineProperty(t, "__esModule", { value: !0 })
        }
    }, e = {}; (() => {
        t.r(e), t.d(e, { default: () => d }); let n, r = 1, o = [], i = "5px", c = "#000000"; function d(t, e) {
            const d = document.getElementById(e.id); d.querySelector("#tree__svg-container") && (d.innerHTML = ""), n = void 0 === e.treeParams ? {} :
                e.treeParams, void 0 !== e.link_width && (i = e.link_width), void 0 !== e.link_color && (c = e.link_color), r = 1, o = []; const l = document.createElement("div"); l.id = "tree__svg-container",
                    d.appendChild(l); const f = document.createElementNS("http://www.w3.org/2000/svg", "svg"); f.id = "tree__svg-container__svg", l.appendChild(f);
            const u = document.createElement("div");
            u.id = "tree__container", d.appendChild(u);
            const p = document.createElement("div");
            p.classList = "tree__container__step__card", p.id = "tree__container__step__card__first", u.appendChild(p);
            const g = void 0 !== n[Object.keys(t)[0]] && void 0 !== n[Object.keys(t)[0]].trad ? n[Object.keys(t)[0]].trad :
                Object.keys(t)[0].trad;
            p.innerHTML = `<p class="tree__container__step__card__p" id="card_${Object.keys(t)[0]}">${g} 
            <br><a href=${n[Object.keys(t)[0]].href} target="_blank">tearsheet</a>
                </p>`,
                a(n[Object.keys(t)[0]], Object.keys(t)[0]), _(t[Object.keys(t)[0]], !0, "tree__container__step__card__first"), s(), document.querySelectorAll(".tree__container__step__card__p").forEach((t => {
                    t.addEventListener("click", (function (t) { "function" == typeof e.card_click && e.card_click(t.target) }))
                })), window.onresize = function () { l.setAttribute("height", "0"), l.setAttribute("width", "0"), s() }
        }
        function s() {
            const t = document.getElementById("tree__svg-container__svg"); for (let e = 0; o.length > e; e++)u(t, document.getElementById(o[e][0]), document.getElementById(o[e][1]),
                document.getElementById(o[e][2]))
        } function _(t, e, d) {
            const s = document.getElementById("tree__svg-container__svg"), l = document.createElement("div"); l.classList.add("tree__container__branch", `from_${d}`),
                document.getElementById(d).after(l);
            for (const f in t) {
                const u = void 0 !== n[f] && void 0 !== n[f].trad ? n[f].trad : f;
                const hr = void 0 !== n[f] && void 0 !== n[f].href ? n[f].href : "";
                if (document.getElementById(`card_${f}`) || (l.innerHTML += `<div class="tree__container__step"><div class="tree__container__step__card" id="${f}">
                    <p id="card_${f}" class="tree__container__step__card__p">${u}
                    <br><a href=${hr} target="_blank">tearsheet</a></p></div></div>`, a(n[f], f)), d && !e || e) {
                    const t = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    t.id = "path" + r, t.setAttribute("stroke", c),
                        t.setAttribute("fill", "none"),
                        t.setAttribute("stroke-width", i),
                        s.appendChild(t),
                        o.push(["path" + r, d || "tree__container__step__card__first", f]), r++
                } Object.keys(t[f]).length > 0 && _(t[f], !1, f)
            }
        } function a(t, e) {
            if (void 0 !== t && void 0 !== t.styles) {
                const r = document.getElementById("card_" + e);
                for (const o in n[e].styles) r.style[o] = t.styles[o]
            }
        } function l(t) { return t < 0 ? -1 : 1 } function f(t) { return t < 0 ? -t : t } function u(t, e, n, r) {
            const o = document.getElementById("tree__svg-container");
            if (n.offsetTop > r.offsetTop) { const t = n; n = r, r = t } const i = o.offsetTop, c = o.offsetLeft; !function (t, e, n, r, o, i) {
                let c = parseFloat(e.getAttribute("stroke-width")); t.getAttribute("height") < i && t.setAttribute("height", i), t.getAttribute("width") < n + c && t.setAttribute("width", n + c),
                    t.getAttribute("width") < o + c && t.setAttribute("width", o + c); let d = .15 * (o - n), s = .15 * (i - r), _ = s < f(d) ? s : f(d), a = 0, u = 1; n > o && (a = 1, u = 0),
                        e.setAttribute("d", "M" + n + " " + r + " V" + (r + _) + " A" + _ + " " + _ + " 0 0 " + a + " " + (n + _ * l(d)) + " " + (r + 2 * _) + " H" + (o - _ * l(d)) + " A" + _ + " " + _ + " 0 0 " + u + " " + o + " " + (r + 3 * _) + " V" + i)
            }(t, e, n.offsetLeft + .5 * n.offsetWidth - c, n.offsetTop + n.offsetHeight - i, r.offsetLeft + .5 * r.offsetWidth - c, r.offsetTop - i)
        }
    })(), treeMaker = e
})();