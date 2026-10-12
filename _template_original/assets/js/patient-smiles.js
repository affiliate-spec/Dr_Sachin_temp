(function () {
  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function cleanLine(value) {
    return String(value ?? "").replace(/\s+/g, " ").trim();
  }

  function stripMatch(text, fullMatch) {
    if (!fullMatch) return text;
    var idx = text.toLowerCase().indexOf(fullMatch.toLowerCase());
    if (idx === -1) return text;
    var before = text.slice(0, idx);
    var after = text.slice(idx + fullMatch.length);
    return cleanLine(
      (before + " " + after)
        .replace(/\(\s*\)/g, " ")
        .replace(/\s*[,;]\s*$/g, "")
        .replace(/^\s*[,;.\-–]\s*/g, "")
    );
  }

  function titleCase(value) {
    return cleanLine(value).replace(/\b([a-z])/g, function (_, ch) {
      return ch.toUpperCase();
    });
  }

  var NAME_STOPWORDS = {
    mother: 1, father: 1, baby: 1, child: 1, son: 1, daughter: 1,
    dob: 1, date: 1, year: 1, born: 1, age: 1,
    thank: 1, thanks: 1, with: 1,
    my: 1, i: 1, we: 1, you: 1, your: 1, they: 1, she: 1, he: 1, it: 1,
    is: 1, was: 1, am: 1, are: 1, were: 1, be: 1, been: 1,
    a: 1, an: 1, the: 1, and: 1, but: 1, or: 1, of: 1, for: 1, to: 1,
    in: 1, on: 1, at: 1, this: 1, that: 1, these: 1, those: 1,
    no: 1, words: 1, dr: 1, doctor: 1, mam: 1, madam: 1, ma: 1, sir: 1,
    hi: 1, hello: 1
  };

  function extractAfterLabel(text, labelPattern, maxWords) {
    var labelRe = new RegExp(labelPattern + "\\s*[:\\-\\u2013]\\s*", "i");
    var labelMatch = text.match(labelRe);
    if (!labelMatch) return null;
    var afterIdx = labelMatch.index + labelMatch[0].length;
    var rest = text.slice(afterIdx);
    var wordRe = /^\s*([A-Z][A-Za-z'.]*)/;
    var collected = [];
    var consumed = 0;

    while (collected.length < maxWords) {
      var slice = rest.slice(consumed);
      var m = slice.match(wordRe);
      if (!m) break;
      var word = m[1];
      if (NAME_STOPWORDS[word.toLowerCase()]) break;
      consumed += m[0].length;
      collected.push(word);
    }
    if (collected.length === 0) return null;

    var capturedText = rest.slice(0, consumed).replace(/^\s+/, "");
    return {
      value: collected.join(" "),
      fullMatch: text.slice(labelMatch.index, afterIdx + consumed).replace(/\s+$/, ""),
    };
  }

  function extractFields(joinedText) {
    var fields = { babyName: "", dob: "", motherName: "", year: "" };
    var remaining = joinedText;

    var dobLabelRegex = /(?:date\s*of\s*birth|date\s*of\s*delivery|d\.?o\.?b\.?|born\s*on)\s*[:\-–]?\s*((?:[0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})|(?:[0-9]{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+[0-9]{2,4}))/i;
    var dobMatch = remaining.match(dobLabelRegex);
    if (dobMatch) {
      fields.dob = cleanLine(dobMatch[1]);
      remaining = stripMatch(remaining, dobMatch[0]);
    }

    var babyResult = extractAfterLabel(
      remaining,
      "(?:baby(?:'?s)?(?:\\s+name)?|child(?:'?s)?(?:\\s+name)?|son(?:'?s\\s+name)?|daughter(?:'?s\\s+name)?)",
      3
    );
    if (babyResult) {
      fields.babyName = cleanLine(babyResult.value);
      remaining = stripMatch(remaining, babyResult.fullMatch);
    }

    var motherResult = extractAfterLabel(remaining, "mother(?:'?s)?\\s+name", 2);
    if (motherResult) {
      fields.motherName = cleanLine(motherResult.value);
      remaining = stripMatch(remaining, motherResult.fullMatch);
    }

    var yearRegex = /year\s*of\s*delivery\s*[:\-–]?\s*(\d{4})/i;
    var yearMatch = remaining.match(yearRegex);
    if (yearMatch) {
      fields.year = yearMatch[1];
      remaining = stripMatch(remaining, yearMatch[0]);
    }

    if (!fields.dob) {
      var standaloneDate = remaining.match(/\b([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})\b/);
      if (standaloneDate) {
        fields.dob = standaloneDate[1];
        remaining = stripMatch(remaining, standaloneDate[0]);
      }
    }

    return { fields: fields, message: remaining };
  }

  function prepareEntry(entry) {
    var allLines = [entry.subtitle]
      .concat(entry.paragraphs || [])
      .concat(entry.meta_lines || [])
      .map(cleanLine)
      .filter(Boolean);

    var seen = new Set();
    var deduped = [];
    allLines.forEach(function (line) {
      var key = line.toLowerCase();
      if (!seen.has(key)) {
        seen.add(key);
        deduped.push(line);
      }
    });

    var combined = deduped.join(" ");
    var extracted = extractFields(combined);
    var fields = extracted.fields;
    var message = extracted.message;

    if (
      fields.motherName &&
      fields.motherName.toLowerCase() === cleanLine(entry.title).toLowerCase()
    ) {
      fields.motherName = "";
    }

    var images = Array.isArray(entry.images) ? entry.images : [];
    var trimmedMessage = cleanLine(message).replace(/^[\-–—:.,;]+\s*/, "").trim();
    var caption = "";
    var quotedMessage = "";

    if (trimmedMessage.length >= 60) {
      quotedMessage = trimmedMessage;
    } else if (trimmedMessage.length > 0) {
      var captionWordCount = trimmedMessage.split(/\s+/).length;
      var titleNorm = cleanLine(entry.title || "").toLowerCase();
      var msgNorm = trimmedMessage.toLowerCase();
      var isEchoOfTitle = msgNorm === titleNorm || titleNorm.indexOf(msgNorm) !== -1;
      var tooThin = trimmedMessage.length < 18 || captionWordCount < 2;
      if (!isEchoOfTitle && !tooThin) {
        caption = trimmedMessage;
      }
    }

    return {
      title: titleCase(entry.title || ""),
      images: images,
      babyName: fields.babyName,
      dob: fields.dob,
      motherName: fields.motherName,
      year: fields.year,
      caption: caption,
      message: quotedMessage,
      hasMessage: Boolean(quotedMessage),
      hasCaption: Boolean(caption),
    };
  }

  function renderHiddenImages(images, title) {
    return images
      .slice(1)
      .map(function (imagePath) {
        return (
          '<a href="' +
          escapeHtml(imagePath) +
          '" class="popup-image jyoti-lightbox-hidden" aria-label="View additional photo of ' +
          escapeHtml(title) +
          '"></a>'
        );
      })
      .join("");
  }

  function renderPhotoBadge(images) {
    if (!Array.isArray(images) || images.length < 2) {
      return "";
    }
    return (
      '<span class="jyoti-story-photo-count">' +
      escapeHtml(images.length) +
      ' Photos</span>'
    );
  }

  function renderFacts(prepared) {
    // Baby name and DOB/date chips intentionally hidden per request.
    return "";
    /* eslint-disable no-unreachable */
    var items = [];
    if (prepared.babyName) {
      items.push({ label: "Baby", value: prepared.babyName });
    }
    if (prepared.dob) {
      items.push({ label: "DOB", value: prepared.dob });
    }
    if (prepared.year && !prepared.dob) {
      items.push({ label: "Year", value: prepared.year });
    }
    if (prepared.motherName) {
      items.push({ label: "Mother", value: prepared.motherName });
    }
    if (items.length === 0) {
      return "";
    }
    return (
      '<dl class="jyoti-story-facts">' +
      items
        .map(function (item) {
          return (
            '<div class="jyoti-story-fact">' +
            '<dt>' +
            escapeHtml(item.label) +
            '</dt>' +
            '<dd>' +
            escapeHtml(item.value) +
            '</dd>' +
            '</div>'
          );
        })
        .join("") +
      '</dl>'
    );
  }

  function renderQuote(prepared) {
    var parts = [];
    if (prepared.hasCaption) {
      parts.push(
        '<p class="jyoti-story-caption">' +
          escapeHtml(prepared.caption) +
          '</p>'
      );
    }
    if (prepared.hasMessage) {
      parts.push(
        '<blockquote class="jyoti-story-quote"><p>' +
          escapeHtml(prepared.message) +
          '</p></blockquote>'
      );
    }
    if (parts.length === 0) {
      return "";
    }
    return parts.join("");
  }

  function renderStoryMedia(prepared) {
    var imagePath = prepared.images[0] || "";
    if (!imagePath) {
      return "";
    }
    return (
      '<div class="jyoti-lightbox-group jyoti-story-media">' +
      '<a href="' +
      escapeHtml(imagePath) +
      '" class="jyoti-story-cover popup-image" aria-label="View patient photo of ' +
      escapeHtml(prepared.title) +
      '">' +
      '<img loading="lazy" src="' +
      escapeHtml(imagePath) +
      '" alt="Patient smile of ' +
      escapeHtml(prepared.title) +
      '">' +
      renderPhotoBadge(prepared.images) +
      "</a>" +
      renderHiddenImages(prepared.images, prepared.title) +
      "</div>"
    );
  }

  function renderRailMedia(prepared) {
    var imagePath = prepared.images[0] || "";
    if (!imagePath) {
      return "";
    }
    return (
      '<div class="jyoti-lightbox-group jyoti-gallery-rail-media">' +
      '<a href="' +
      escapeHtml(imagePath) +
      '" class="popup-image" aria-label="View patient photo of ' +
      escapeHtml(prepared.title) +
      '">' +
      '<img loading="lazy" src="' +
      escapeHtml(imagePath) +
      '" alt="Patient smile of ' +
      escapeHtml(prepared.title) +
      '">' +
      "</a>" +
      renderHiddenImages(prepared.images, prepared.title) +
      "</div>"
    );
  }

  function renderFeatureMedia(prepared) {
    var imagePath = prepared.images[0] || "";
    if (!imagePath) {
      return "";
    }
    return (
      '<div class="jyoti-lightbox-group jyoti-gallery-feature-media">' +
      '<a href="' +
      escapeHtml(imagePath) +
      '" class="popup-image" aria-label="View patient photo of ' +
      escapeHtml(prepared.title) +
      '">' +
      '<img loading="lazy" src="' +
      escapeHtml(imagePath) +
      '" alt="Featured patient smile of ' +
      escapeHtml(prepared.title) +
      '">' +
      renderPhotoBadge(prepared.images) +
      "</a>" +
      renderHiddenImages(prepared.images, prepared.title) +
      "</div>"
    );
  }

  function renderStoryCard(entry) {
    var prepared = prepareEntry(entry);
    var textOnlyClass = prepared.images.length ? "" : " jyoti-story-card--text-only";

    return (
      '<article class="jyoti-story-card' +
      textOnlyClass +
      '">' +
      renderStoryMedia(prepared) +
      '<div class="jyoti-story-content">' +
      '<h3 class="jyoti-story-name">' +
      escapeHtml(prepared.title) +
      "</h3>" +
      renderFacts(prepared) +
      renderQuote(prepared) +
      "</div>" +
      "</article>"
    );
  }

  function renderRailCard(entry) {
    var prepared = prepareEntry(entry);
    var textOnlyClass = prepared.images.length ? "" : " jyoti-gallery-rail-card--text-only";
    var snippet = "";
    if (prepared.hasMessage) {
      snippet = prepared.message;
    } else if (prepared.hasCaption) {
      snippet = prepared.caption;
    } else if (prepared.babyName && prepared.dob) {
      snippet = "Baby " + prepared.babyName + " · " + prepared.dob;
    } else if (prepared.babyName) {
      snippet = "Baby " + prepared.babyName;
    } else if (prepared.dob) {
      snippet = "Born " + prepared.dob;
    }

    return (
      '<article class="jyoti-gallery-rail-card' +
      textOnlyClass +
      '">' +
      renderRailMedia(prepared) +
      '<div class="jyoti-gallery-rail-copy">' +
      "<h4>" +
      escapeHtml(prepared.title) +
      "</h4>" +
      (snippet
        ? (
      '<p>' +
      escapeHtml(snippet) +
          "</p>"
        )
        : "") +
      "</div>" +
      "</article>"
    );
  }

  function renderFeatureCard(entry) {
    var prepared = prepareEntry(entry);
    var textOnlyClass = prepared.images.length ? "" : " jyoti-gallery-feature-card--text-only";

    return (
      '<article class="jyoti-gallery-feature-card' +
      textOnlyClass +
      '">' +
      renderFeatureMedia(prepared) +
      '<div class="jyoti-gallery-feature-copy">' +
      "<h3>" +
      escapeHtml(prepared.title) +
      "</h3>" +
      renderFacts(prepared) +
      renderQuote(prepared) +
      "</div>" +
      "</article>"
    );
  }

  function renderSpotlight(entries) {
    if (!Array.isArray(entries) || entries.length === 0) {
      return "";
    }
    var rail = entries.slice(1, 4).map(renderRailCard).join("");
    return (
      '<div class="jyoti-gallery-spotlight-grid">' +
      renderFeatureCard(entries[0]) +
      '<div class="jyoti-gallery-spotlight-rail">' +
      rail +
      "</div>" +
      "</div>"
    );
  }

  function setupQuoteToggles(root) {
    var scope = root || document;
    var quotes = scope.querySelectorAll(".jyoti-story-quote");
    Array.prototype.forEach.call(quotes, function (quote) {
      if (quote.getAttribute("data-toggle-ready")) {
        return;
      }
      var para = quote.querySelector("p");
      if (!para) {
        return;
      }
      quote.setAttribute("data-toggle-ready", "1");
      // Only add a toggle when the text is actually clamped/overflowing.
      if (para.scrollHeight <= para.clientHeight + 2) {
        return;
      }
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "jyoti-story-readmore";
      btn.textContent = "Read more";
      btn.setAttribute("aria-expanded", "false");
      btn.addEventListener("click", function () {
        var expanded = quote.classList.toggle("is-expanded");
        btn.textContent = expanded ? "Read less" : "Read more";
        btn.setAttribute("aria-expanded", expanded ? "true" : "false");
      });
      quote.appendChild(btn);
    });
  }

  function setupRailToggles(root) {
    var scope = root || document;
    var copies = scope.querySelectorAll(".jyoti-gallery-rail-copy");
    Array.prototype.forEach.call(copies, function (copy) {
      if (copy.getAttribute("data-toggle-ready")) {
        return;
      }
      var para = copy.querySelector("p");
      if (!para) {
        return;
      }
      copy.setAttribute("data-toggle-ready", "1");
      // Only add a toggle when the text is actually clamped/overflowing.
      if (para.scrollHeight <= para.clientHeight + 2) {
        return;
      }
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "jyoti-story-readmore";
      btn.textContent = "Read more";
      btn.setAttribute("aria-expanded", "false");
      btn.addEventListener("click", function () {
        var expanded = copy.classList.toggle("is-expanded");
        btn.textContent = expanded ? "Read less" : "Read more";
        btn.setAttribute("aria-expanded", expanded ? "true" : "false");
      });
      copy.appendChild(btn);
    });
  }

  function initImagePopup() {
    if (!window.jQuery || !jQuery.fn || !jQuery.fn.magnificPopup) {
      return;
    }
    jQuery(".jyoti-lightbox-group").each(function () {
      var group = jQuery(this);
      if (group.data("mfp-bound")) {
        return;
      }
      group.magnificPopup({
        delegate: "a.popup-image",
        type: "image",
        gallery: { enabled: true },
        removalDelay: 180,
        mainClass: "mfp-fade",
      });
      group.data("mfp-bound", true);
    });
  }

  function setStat(id, value) {
    var node = document.getElementById(id);
    if (node) {
      node.textContent = value;
    }
  }

  function columnCountForWidth() {
    var w = window.innerWidth || document.documentElement.clientWidth || 0;
    if (w <= 767) return 1;
    if (w <= 991) return 2;
    return 3;
  }

  // Balanced-column masonry built in JS. CSS multi-column (column-count) was
  // leaving a large phantom gap at the bottom of the wall because the browser
  // over-reserves balanced-column height when cards use break-inside: avoid.
  // Here we place each card (in order) into the currently shortest column, so
  // the columns stay tight and the section ends right where the cards end.
  function buildMasonry(container, cards) {
    var colCount = columnCountForWidth();
    if (container.getAttribute("data-cols") === String(colCount)) {
      return;
    }
    container.setAttribute("data-cols", String(colCount));
    container.innerHTML = "";

    var columns = [];
    var i;
    for (i = 0; i < colCount; i++) {
      var col = document.createElement("div");
      col.className = "jyoti-gallery-masonry-col";
      container.appendChild(col);
      columns.push({ el: col, height: 0 });
    }

    cards.forEach(function (card) {
      var shortest = columns[0];
      columns.forEach(function (c) {
        if (c.height < shortest.height) {
          shortest = c;
        }
      });
      shortest.el.appendChild(card);
      // offsetHeight is reliable here: card images carry aspect-ratio, so their
      // height is reserved immediately even before the image bytes load.
      shortest.height += card.offsetHeight || 0;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var grid = document.getElementById("patientSmilesGrid");
    var spotlight = document.getElementById("patientSmilesSpotlight");
    if (!grid) {
      return;
    }

    fetch("assets/data/patient-smiles.json")
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Failed to load patient smiles data");
        }
        return response.json();
      })
      .then(function (entries) {
        if (!Array.isArray(entries) || entries.length === 0) {
          var empty =
            '<div class="jyoti-patient-empty">Patient stories will be added here shortly.</div>';
          if (spotlight) {
            spotlight.innerHTML = empty;
          }
          grid.innerHTML = empty;
          return;
        }

        var preparedEntries = entries.map(prepareEntry);
        var totalPhotos = preparedEntries.reduce(function (sum, entry) {
          return sum + entry.images.length;
        }, 0);
        var notesCount = preparedEntries.filter(function (entry) {
          return entry.hasMessage;
        }).length;

        setStat("patientSmilesEntryCount", preparedEntries.length + "+");
        setStat("patientSmilesPhotoCount", totalPhotos + "+");
        setStat("patientSmilesNoteCount", notesCount + "+");

        var hasSpotlight = Boolean(spotlight);
        if (hasSpotlight) {
          spotlight.innerHTML = renderSpotlight(entries.slice(0, 4));
        }

        // When there's no spotlight section, the wall holds every story.
        var wallEntries =
          hasSpotlight && entries.length > 4 ? entries.slice(4) : entries;

        // Build the card elements once, then distribute them across balanced
        // columns. Reused on resize so the column count can adapt without
        // re-rendering the cards.
        var temp = document.createElement("div");
        temp.innerHTML = wallEntries.map(renderStoryCard).join("");
        var cards = Array.prototype.slice.call(temp.children);

        grid.innerHTML = "";
        var masonry = document.createElement("div");
        masonry.className = "jyoti-gallery-masonry-cols";
        grid.appendChild(masonry);

        function layout() {
          buildMasonry(masonry, cards);
        }
        layout();

        var resizeTimer = null;
        window.addEventListener("resize", function () {
          if (resizeTimer) {
            window.clearTimeout(resizeTimer);
          }
          resizeTimer = window.setTimeout(layout, 150);
        });

        initImagePopup();
        if (hasSpotlight) {
          setupQuoteToggles(spotlight);
          setupRailToggles(spotlight);
        }
        setupQuoteToggles(grid);
      })
      .catch(function () {
        var fallback =
          '<div class="jyoti-patient-empty">Patient stories are temporarily unavailable. Please try again shortly.</div>';
        if (spotlight) {
          spotlight.innerHTML = fallback;
        }
        grid.innerHTML = fallback;
      });
  });
})();
