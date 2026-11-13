/* Casa Abadia site. No build step, no dependencies.
   Galleries read window.MANIFEST, written by tools/build_manifest.py into media/manifest.js. */
(function () {
  // Pages live in sources_public/ or sources_private/. The two entry pages
  // (index_public.html, index_private.html) sit one level up and set data-root.
  var NAVS = {
    partners: {
      home: ["index_public.html", "Overview"],
      pages: [
        ["plans.html", "Plans and 3D"],
        ["woodhome.html", "Wood Home"],
        ["technical.html", "Technical choices"],
        ["team.html", "Team"],
        ["photos.html", "Photos"],
        ["journal.html", "Journal"],
        ["materials.html", "Materials"]
      ],
      extra: []
    },
    private: {
      home: ["index_private.html", "Private index"],
      pages: [
        ["decisions.html", "Decisions"],
        ["invoices.html", "Invoices"],
        ["mortgage.html", "Mortgage"],
        ["iva.html", "IVA structure"]
      ],
      extra: [["index_public.html", "Partner site"]]
    }
  };

  var body = document.body;
  var navKey = body.getAttribute("data-nav") || "partners";
  var rootAttr = body.getAttribute("data-root");
  var atRoot = rootAttr !== null;
  var root = rootAttr || "";
  var up = atRoot ? "" : "../";
  var mediaBase = body.getAttribute("data-media-base") || (root + "media/");
  var M = window.MANIFEST || {};
  var here = location.pathname.split("/").pop() || "";
  var nav = NAVS[navKey];
  var NAV = [[up + nav.home[0], nav.home[1], atRoot]]
    .concat(nav.pages.map(function (n) { return [root + n[0], n[1], !atRoot && n[0] === here]; }))
    .concat(nav.extra.map(function (n) { return [up + n[0], n[1], false]; }));

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function label(file) {
    return file.replace(/\.[^.]+$/, "").replace(/[_]+/g, " ");
  }
  function url(dir, file) {
    return mediaBase + dir.split("/").map(encodeURIComponent).join("/") + "/" + encodeURIComponent(file);
  }

  // Header and navigation
  var header = document.createElement("header");
  header.className = "site";
  var links = NAV.map(function (n) {
    return '<a href="' + n[0] + '"' + (n[2] ? ' class="on"' : "") + ">" + n[1] + "</a>";
  }).join("");
  header.innerHTML =
    (navKey === "private" ? '<div class="private-banner">Private. Local only. Do not publish.</div>' : "") +
    '<div class="inner"><div class="brand">Casa Abadia</div>' +
    '<div class="sub">Timber frame house, Abadia, Ericeira</div>' +
    '<nav class="site">' + links + "</nav></div>";
  body.insertBefore(header, body.firstChild);

  // Render one folder of files
  function renderFiles(dir, entry) {
    var files = (entry && entry.files) || [];
    if (!files.length) return '<div class="empty" title="media/' + esc(dir) + '">No files published yet.</div>';
    var imgs = [], vids = [], docs = [], previews = {};
    // "<document>.preview.jpg" next to a document is its picture, not a photo of its own
    files.forEach(function (f) {
      var m = /^(.*)\.preview\.(jpe?g|png|webp)$/i.exec(f);
      if (m) previews[m[1]] = f;
    });
    files.forEach(function (f) {
      if (/\.preview\.(jpe?g|png|webp)$/i.test(f)) return;
      if (/\.(jpe?g|png|webp|gif|avif)$/i.test(f)) imgs.push(f);
      else if (/\.(mp4|webm|mov)$/i.test(f)) vids.push(f);
      else docs.push(f);
    });
    var html = "";
    if (imgs.length) {
      html += '<div class="thumbs">' + imgs.map(function (f) {
        var u = url(dir, f);
        return '<figure><img loading="lazy" src="' + u + '" alt="' + esc(label(f)) + '" data-full="' + u + '">' +
          "<figcaption>" + esc(label(f)) + "</figcaption></figure>";
      }).join("") + "</div>";
    }
    vids.forEach(function (f) {
      html += '<p><video controls preload="metadata" src="' + url(dir, f) + '"></video><br><span class="note">' + esc(label(f)) + "</span></p>";
    });
    var cards = docs.filter(function (f) { return previews[f]; });
    docs = docs.filter(function (f) { return !previews[f]; });
    if (cards.length) {
      html += '<div class="doccards">' + cards.map(function (f) {
        var ext = (f.split(".").pop() || "").toLowerCase();
        return '<a class="doccard" href="' + url(dir, f) + '" target="_blank" rel="noopener">' +
          '<img loading="lazy" src="' + url(dir, previews[f]) + '" alt="">' +
          '<span class="t">' + esc(label(f)) + '</span><span class="ext">' + esc(ext) + "</span></a>";
      }).join("") + "</div>";
    }
    if (docs.length) {
      html += '<ul class="files">' + docs.map(function (f) {
        var ext = (f.split(".").pop() || "").toLowerCase();
        return '<li><span class="ext">' + esc(ext) + '</span><a href="' + url(dir, f) + '" target="_blank" rel="noopener">' + esc(label(f)) + "</a></li>";
      }).join("") + "</ul>";
    }
    return html;
  }

  // <div data-gallery="plans/floor-plans"></div>
  Array.prototype.forEach.call(document.querySelectorAll("[data-gallery]"), function (el) {
    var dir = el.getAttribute("data-gallery");
    var entry = M[dir];
    var html = "";
    if (entry && entry.note) html += "<p>" + esc(entry.note).replace(/\n\s*\n/g, "</p><p>").replace(/\n/g, "<br>") + "</p>";
    el.innerHTML = html + renderFiles(dir, entry);
  });

  // <div data-journal="progress"></div>  one post per subfolder named YYYY-MM-DD_title
  Array.prototype.forEach.call(document.querySelectorAll("[data-journal]"), function (el) {
    var prefix = el.getAttribute("data-journal") + "/";
    var keys = Object.keys(M).filter(function (k) {
      return k.indexOf(prefix) === 0 && k.slice(prefix.length).indexOf("/") < 0;
    }).sort().reverse();
    if (!keys.length) { el.innerHTML = '<div class="empty">No journal entries yet.</div>'; return; }
    el.innerHTML = keys.map(function (k) {
      var name = k.slice(prefix.length);
      var m = /^(\d{4}-\d{2}-\d{2})[_ ]?(.*)$/.exec(name);
      var date = m ? m[1] : "";
      var title = (m ? m[2] : name).replace(/[_]+/g, " ") || "Update";
      var e = M[k];
      var note = e.note ? "<p>" + esc(e.note).replace(/\n\s*\n/g, "</p><p>").replace(/\n/g, "<br>") + "</p>" : "";
      return '<article class="post"><div class="date">' + esc(date) + "</div><h3>" + esc(title) + "</h3>" +
        note + (e.files && e.files.length ? renderFiles(k, e) : "") + "</article>";
    }).join("");
  });

  // Lightbox
  var lb = document.createElement("div");
  lb.id = "lightbox";
  lb.innerHTML = '<img alt="">';
  body.appendChild(lb);
  document.addEventListener("click", function (ev) {
    var t = ev.target;
    if (t.tagName === "IMG" && t.getAttribute("data-full")) {
      lb.firstChild.src = t.getAttribute("data-full");
      lb.className = "on";
    } else if (lb.className === "on") {
      lb.className = "";
    }
  });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") lb.className = ""; });
})();
